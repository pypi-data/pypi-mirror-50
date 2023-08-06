import re
import socket
import time

import docker
from docker import errors

from anna_worker import job


class Worker:
	"""
	This module handles communication between the job queue and docker
	"""

	def __init__(self, max_concurrent=2):
		self.client = docker.from_env()
		self.max_concurrent = max_concurrent
		self.hub = None
		self.jobs = []
		self.container_options = {'links': {'hub': 'hub'}, 'shm_size': '2G', 'detach': True}
		self.last_job_request = 0

	def __del__(self):
		self.prune()
		self.client.close()

	def update(self):
		self.keep_hub_alive()  # Make sure the hub is running
		self.update_jobs()  # Retrieve logs & handle containers
		if self.can_run_more():  # Check if we can run more concurrent containers
			self.start_next_job()  # Get the next job in the queue and fire up a container

	def keep_hub_alive(self):
		"""
		Makes sure the selenium hub is running & removes any stopped hub containers
		:return:
		"""
		try:
			try:
				self.hub = self.client.containers.get('hub')
				if self.hub.status != 'running':
					self.hub.remove()
					self.keep_hub_alive()
			except docker.errors.NotFound:
				try:
					self.hub = self.client.containers.run('selenium/hub', name='hub', ports={'4444/tcp': 4444},
														  detach=True)
				except docker.errors.APIError:
					self.hub.stop()
					self.keep_hub_alive()
		except docker.errors.APIError:
			pass

	def update_jobs(self):
		for job in self.jobs:
			self.update_job(job)

	def is_running(self, job):
		"""
		Check if the job's container is running
		:param job:
		:return:
		"""
		if job.container is not None:
			container = self.get_container(job)
			if container is not False:
				return container.status in ('starting', 'running')
		return False

	def get_running(self):
		return [job for job in self.jobs if self.is_running(job)]

	def update_job(self, job):
		job.log = self.get_logs(job)
		if not self.is_running(job) and job.container is not None:
			container = self.get_container(job)
			if container.status == 'exited' and container.attrs['State']['ExitCode'] == 0:
				job.status = 'DONE'
			else:
				job.status = 'FAILED'

		job.changed = True

	def stop_container(self, job):
		container = self.get_container(job)
		if container is not False:
			job.log = self.get_logs(job)
			if container.status == 'running':
				container.stop()
			container.remove()

	def get_container(self, job):
		if job.container is None:
			return False
		try:
			return self.client.containers.get(job.container)
		except docker.errors.NotFound:
			return False
		except docker.errors.NullResource:
			return False

	def prune(self):
		try:
			for job in self.jobs:
				if job.log is None and job.container is not None and job.status in (
						'STOPPED', 'ERROR', 'DONE'):
					self.stop_container(job)
		except docker.errors.APIError as e:
			return False

	def get_logs(self, job):
		container = self.get_container(job)
		if container is not False:
			return re.sub("\\x1b\[0m|\\x1b\[92m|\\x1b\[91m|\\x1b\[93m", '', container.logs().decode('utf-8'))  # colorless
		else:
			return 'unable to get logs from container'

	def can_run_more(self):
		"""
		Just a simple check against max_concurrent
		"""
		queue_length = len(self.jobs)
		if queue_length == 0:
			return False
		running = len(self.get_running())
		return queue_length - running > 0 and running < self.max_concurrent

	def start_next_job(self):
		"""
		Starts the next pending job in the queue
		"""
		job = self.get_next_job()
		if job is not None:
			self.start_job(job)
			return job
		return False

	@staticmethod
	def before_start(job):
		"""
		Make sure we can run the job, set the status & report to slack
		:param job:
		:return:
		"""
		if job.driver not in ('chrome', 'firefox'):
			raise TypeError('desired driver(s) not supported: ' + job.driver)

		job.status = 'STARTING'
		job.changed = True

	def __start__(self, job):
		job.container = str(self.run_container(job).short_id)
		job.changed = True

	@staticmethod
	def after_start(job):
		"""
		Set the status & report to slack
		:param job:
		:return:
		"""
		job.status = 'RUNNING'
		job.changed = True

	def start_job(self, job):
		"""
		Starts the next pending job in the queue
		"""
		self.before_start(job)
		self.__start__(job)
		self.after_start(job)

	def run_container(self, job):
		"""
		Attempt to start the container
		:param job:
		:return:
		"""
		image, volumes, command = job.get_image_volumes_and_command()
		return self.client.containers.run(
			image=image,
			links=self.container_options['links'],
			shm_size=self.container_options['shm_size'],
			detach=self.container_options['detach'],
			command=command)

	def get_next_job(self):
		for job in self.jobs:
			if job.status in ('PENDING', 'RESERVED'):
				return job

	def should_request_work(self):
		if time.time() - self.last_job_request < 3:
			return False
		if len([job for job in self.jobs if
				job.status in ('PENDING', 'STARTING', 'RUNNING', 'RESERVED')]) < self.max_concurrent:
			self.last_job_request = time.time()
			return True
		return False

	def append(self, new_job):
		if not isinstance(new_job, dict) or any(attribute not in new_job for attribute in job.attributes):
			raise TypeError
		self.jobs.append(
			job.Job(id=new_job['id'], container=new_job['container'], driver=new_job['driver'], site=new_job['site'],
					status=new_job['status'], worker=socket.gethostname(), log=new_job['log']))

	def remove(self, job):
		self.stop_container(job=job)
		self.jobs.remove(tuple(j for j in self.jobs if j['id'] == job['id'])[0])

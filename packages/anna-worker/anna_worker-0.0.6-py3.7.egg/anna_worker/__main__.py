import os
import time

from docker import errors
from worker import Worker

from anna_client.client import Client

#if not ('ANNA_HOST' in os.environ and 'ANNA_TOKEN' in os.environ):
#        print('Please set both ANNA_HOST and ANNA_TOKEN in your env')
#        exit(0)
#client = Client(host=os.environ['ANNA_HOST'], token=os.environ['ANNA_TOKEN'])
client = Client(host='http://localhost:5000', token='eyJhbGciOiJIUzUxMiIsImlhdCI6MTU1MTkwMDM1NywiZXhwIjoxNTgzNDM2MzU3fQ.eyJpZCI6MSwiZW1haWwiOiJwYXRyaWsucGlobHN0cm9tQGdtYWlsLmNvbSJ9.la4yZWqPCIUhH5LWaNILYj_1aBhlKVC-hgiGQgw9EiBFooUxOWjPtFgVoYkdeJSwN-TAR2cS4oAL2x9W8Zp3-g')
worker = Worker(max_concurrent=4)
last_status_check = 0


def update():
	global last_status_check
	try:
		worker.prune()
	except errors.APIError:
		pass
	if time.time() - last_status_check >= 3:
		remove_manually_stopped_jobs_from_host()
		last_status_check = time.time()
	worker.update()
	if len(worker.jobs) > 0:
		client.update([job.dict() for job in worker.jobs if job.changed])
		for job in worker.jobs:
			if job.changed:
				if job.status in ('done', 'failed', 'error', 'rm'):
					worker.stop_container(job)
					worker.jobs.remove(job)
				else:
					job.changed = False


def remove_manually_stopped_jobs_from_host():
	jobs = client.query({'id': [job.id for job in worker.jobs]})
	if isinstance(jobs, list):
		for job in jobs:
			if job is None or job['status'] == 'rm':
				job.status = 'rm'


def request_work():
	if worker.should_request_work():
		job = client.request_job(worker.max_concurrent - len(worker.get_running()))
		if isinstance(job, list) and len(job) > 0:
			worker.append(job[0])
		remove_manually_stopped_jobs_from_host()


if __name__ == '__main__':
	while True:
		update()
		request_work()

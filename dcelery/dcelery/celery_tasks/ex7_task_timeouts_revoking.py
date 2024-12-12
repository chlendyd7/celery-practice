import time
from celery import chain, group
from dcelery.celery_config import app
import traceback
'''
    from dcelery.celery_tasks.ex7_task_timeouts_revoking import long_running_task
    long_running_task()
'''

@app.task(queue='tasks', time_limit=5)
def long_running_task():
    time.sleep(6)
    return "Task completed successfully"
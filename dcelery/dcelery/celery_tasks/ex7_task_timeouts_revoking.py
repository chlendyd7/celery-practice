import sys
import time
from celery import chain, group
from dcelery.celery_config import app
import traceback
'''
    from dcelery.celery_tasks.ex7_task_timeouts_revoking import long_running_task
    long_running_task()
'''

@app.task(queue='tasks', time_limit=10)
def long_running_task():
    time.sleep(6)
    return "Task completed successfully"

@app.task(queue='tasks', bind=True)
def process_task_result(self, result):
    if result is None:
        return "Task was revoked, skipping result processing"
    else:
        return f'Task result: {result}'


def execute_task_exaples():
    result = long_running_task.delay()
    try:
        task_result = result.get(timeout=40)
    except TimeoutError:
        print("Task timed out")
    
    task = long_running_task.delay()
    
    # 지정된 태스크를 취소(취소 요청)합니다, terminate는 강제종료
    task.revoke(terminate=True)
    
    time.sleep(3)
    sys.stdout.write(task.status)

    if task.status == 'REVOKED':
        process_task_result.delay(None)
    else:
        process_task_result.delay(task.result)

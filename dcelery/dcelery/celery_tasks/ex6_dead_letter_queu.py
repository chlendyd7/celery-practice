from celery import chain, group
from dcelery.celery_config import app
import traceback
'''
    from dcelery.celery_tasks.ex6_dead_letter_queu import run_task_group
    handle_failed_task.delay()
'''
# task가 실패 시 완료 될 때 까지 대기열에 남아있음 안정성 증가
app.conf.task_acks_late = True

# worker 손실 시 task를 거부
app.conf.task_reject_on_worker_lost = True

@app.task(queue='tasks')
def my_task(z):
    try:
        if z == 2:
            raise ValueError("Error wrong number")
    except Exception as e:
        traceback_str = traceback.format_exc() 
        task_id = my_task.request.id
        handle_failed_task.apply_async(args=(z, str(e),traceback_str, task_id))
        raise

@app.task(queue='dead_letter')
def handle_failed_task(z, task_id, exception, traceback_str):
    print(f"Task failed: task_id={task_id}, z={z}, exception={exception}")
    print(traceback_str)
    return "Custom logic to process"

def run_task_group():
    task_group = group(
        my_task.s(1),
        my_task.s(2),
        my_task.s(3),
    )
    task_group.apply_async()

import time
from celery import shared_task

@shared_task
def tp1(task_rate_limit='10/m'):
    time.sleep(3)
    return
@shared_task
def tp2(queue='celery:1'):
    time.sleep(3)
    return
@shared_task
def tp3(queue='celery:2'):
    time.sleep(3)
    return
@shared_task
def tp4(queue='celery:3'):
    time.sleep(3)
    return
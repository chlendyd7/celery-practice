import os
import time
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')
app = Celery("dcelery")
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.conf.task_routes = {
#     'newapp.tasks.task1':{'queue':'queue1'},
#     'newapp.tasks.task2':{'queue':'queue2'}
#     }

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={
        'x-max-priority': 10
    }),
]

app.conf.task_acks_late = True
app.conf.task_default_priority = 5

# worker 가 작업을 가져올 수 있는 갯수 네트워크 및 오버헤드를 줄일 수 있음
app.conf.worker_prefetch_multiplier = 1

# worker 동시성 설정, 한번에 일을 할 수 있는 갯수
app.conf.worker_concurrency = 1

@app.task(queue='tasks')
def t1(a,b, message=None):
    time.sleep(3)
    result = a + b
    if message:
        result = f'{message}: {result}'
    return result

@app.task(queue='tasks')
def t2():
    time.sleep(3)
    return
@app.task(queue='tasks')
def t3():
    time.sleep(3)
    return

def execute_sync():
    result = t1.apply_async(args=[5,10], kwargs={"message":"The sum is"})
    task_result = result.get()
    print("Task is running synchronously")
    print(task_result)

def execute_async():
    result = t1.apply_async(args=[5,10], kwargs={"message":"The sum is"})
    print("Task is running synchronously")
    print(result)

# app.conf.task_default_rate_limit = '1/m'

# app.conf.broker_transport_options = {
#     'priority_steps': list(range(10)),
#     'sep':':',
#     'queue_order_strategy':'priority',
# }
# 모든 모듈에 들어가서 celery task를 찾음
app.autodiscover_tasks()

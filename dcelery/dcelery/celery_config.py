import os
import time
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')
app = Celery("dcelery")
app.config_from_object("django.conf:settings", namespace="CELERY")
sentry_dsn = "https://74a9d0cae2746017d251dc7f1c324d0d@o4508471159554048.ingest.de.sentry.io/4508471292330064"
sentry_sdk.init(dsn=sentry_dsn, integrations=[CeleryIntegration()])

# app.conf.task_routes = {
#     'newapp.tasks.task1':{'queue':'queue1'},
#     'newapp.tasks.task2':{'queue':'queue2'}
#     }

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={
        'x-max-priority': 10
    }),
    Queue('dead_letter', routing_key='dead_letter'),
]

app.conf.task_acks_late = True
app.conf.task_default_priority = 5

# worker 가 작업을 가져올 수 있는 갯수 네트워크 및 오버헤드를 줄일 수 있음
app.conf.worker_prefetch_multiplier = 1

# worker 동시성 설정, 한번에 일을 할 수 있는 갯수
app.conf.worker_concurrency = 1

base_dir = os.getcwd()
task_folder = os.path.join(base_dir, 'dcelery', 'celery_tasks')

if os.path.exists(task_folder) and os.path.isdir(task_folder):
    task_modules = []
    for filename in os.listdir(task_folder):
        if filename.startswith('ex') and filename.endswith('.py'):
            module_name = f'dcelery.celery_tasks.{filename[:-3]}'

            module = __import__(module_name, fromlist=['*'])

            for name in dir(module):
                obj = getattr(module, name)
                if callable(obj):
                    task_modules.append(f'{module_name}.{name}')

    app.autodiscover_tasks(task_modules)

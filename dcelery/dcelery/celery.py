import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcelery.settings')
app = Celery("dcelery")
app.config_from_object("django.conf:settings", namespace="CELERY")

@app.task
def add_numbers():
    return

# 모든 모듈에 들어가서 celery task를 찾음
app.autodiscover_tasks()

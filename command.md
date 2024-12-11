pip freeze > requirements.txt
docker-compose up -d --build
docker exec -it django /bin/sh

from celery import group
from newapp.tasks import tp1,tp2,tp3,tp4
tasks_group = group(tp1.s(), tp2.s(), tp3.s(), tp4.s())
task_group.apply_async()

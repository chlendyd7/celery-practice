pip freeze > requirements.txt
docker-compose up -d --build
docker exec -it django /bin/sh


#Run on django to inspect task
celery inspect active
celery inspect active_queues

# remove all docker
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -aq)

# powershell
docker stop (docker ps -aq) && docker rm (docker ps -aq) && docker rmi (docker images -aq)


# cmd
for /f "tokens=*" %i in ('docker ps -aq') do docker stop %i && for /f "tokens=*" %i in ('docker ps -aq') do docker rm %i && for /f "tokens=*" %i in ('docker images -aq') do docker rmi %i


from celery import group
from newapp.tasks import tp1,tp2,tp3,tp4
tasks_group = group(tp1.s(), tp2.s(), tp3.s(), tp4.s())
task_group.apply_async()

from celery import chain
task_chain = chain(tp1.s(), tp2.s(), tp3.s())
task_chain.apply_asnyc()

from dcelary.celary import t1,t2,t3
t2.apply_async(priority=5)
t1.apply_async(priority=6)
t3.apply_async(priority=7)

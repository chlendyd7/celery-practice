from celery import shared_task

@shared_task
def sharedtask():
    # 작업 내용
    return "Task Completed"

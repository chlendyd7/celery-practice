import logging
from dcelery.celery_config import app
from celery import Task
'''
    from dcelery.celery_tasks.ex1_try_except import my_task
    my_task.delay()
'''


logging.basicConfig(filename='app.log',
    level=logging.ERROR,
    format='%(actime)s %(levelname)s %(message)s'
)

class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, ConnectionError):
            logging.error('Connection error occurred....')
        else:
            print('{0!r} failed: {1!r}'.format(task_id, exc))

app.Task = CustomTask

@app.task(queue='tasks')
def my_task():
    try:
        raise ConnectionError("Connection Error Occurred..")
    except ConnectionError:
        logging.error('Connection')
        raise ConnectionError()
    except ValueError:
        logging.error('Value error occurred...')
        notify_admins()
        perform_specific_error_handling()

def perform_specific_error_handling():
    
    pass

def notify_admins():
    pass

import logging
from dcelery.celery_config import app
'''
    from dcelery.celery_tasks.ex1_try_except import my_task
    my_task.delay()
'''


logging.basicConfig(filename='app.log',
    level=logging.ERROR,
    format='%(actime)s %(levelname)s %(message)s'
)



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

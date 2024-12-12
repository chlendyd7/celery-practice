from celery import chain, group
from dcelery.celery_config import app
'''
    from dcelery.celery_tasks.ex5_error_handling_chain import run_task_chain
    my_task.delay()
'''


@app.task(queue='tasks')
def add(x, y):
    return x + y

@app.task(queue='tasks')
def multiply(result):
    if result == 5:
        raise ValueError('Error: Division by zero.')
    return result*2

def run_task_chain():
    task_chain = chain(add.s(2,3), multiply.s())
    result = task_chain.apply_async()
    result.get()

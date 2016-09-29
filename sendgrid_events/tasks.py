from celery import task

from .models import Event


@task()
def event_process_batch_task(body):
    return Event.process_batch(data=body)

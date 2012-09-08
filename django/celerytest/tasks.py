from celery.task import periodic_task
from celery.task.schedules import crontab

from datetime import timedelta

@periodic_task(run_every=crontab(minute="*/1"))
def add(x = 4, y = 10):
    return x + y

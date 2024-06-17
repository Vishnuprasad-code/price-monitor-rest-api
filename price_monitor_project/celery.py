import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_monitor_project.settings')

app = Celery('price_monitor_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'add-every-30-minutes': {
        'task': "pm_api.tasks.update_price_tables",
        'schedule': 900.0,
        # 'args': (16, 16)
    },
}
app.conf.timezone = 'UTC'


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

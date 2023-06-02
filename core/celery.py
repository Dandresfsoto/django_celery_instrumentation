import os

from celery import Celery
from celery.signals import worker_init
from klym_telemetry.instrumenters import instrument_app

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('django_celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@worker_init.connect()
def init_celery_tracing(*args, **kwargs):
    instrument_app(app_type='celery', service_name="celery", endpoint="http://collector:4317")
    instrument_app(app_type='psycopg2', service_name="database", endpoint="http://collector:4317")
    instrument_app(app_type='requests', service_name="requests", endpoint="http://collector:4317")

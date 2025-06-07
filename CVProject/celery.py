import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CVProject.settings")

app = Celery("CVProject")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Redis configuration
app.conf.broker_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
app.conf.result_backend = os.environ.get("REDIS_URL", "redis://redis:6379/0")

app.autodiscover_tasks()

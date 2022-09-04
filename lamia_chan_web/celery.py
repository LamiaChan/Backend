import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lamia_chan_web.settings")
app = Celery("lamia_chan_web")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

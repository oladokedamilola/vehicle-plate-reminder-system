from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Use the correct project name here
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_reminder.settings')

app = Celery('vehicle_reminder')

# Using a string here means the worker doesn’t have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

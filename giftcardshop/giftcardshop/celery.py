import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giftcardshop.settings')

app = Celery('giftcardshop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = 'redis://redis:6379/0'

app.conf.beat_schedule = {
    'filter_outdated_orders': {
        'task': 'orders.tasks.make_unpaid_orders_outdated',
        'schedule': crontab(hour=3, minute=0),
    }
}
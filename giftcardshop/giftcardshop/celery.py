import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giftcardshop.settings')

app = Celery('giftcardshop')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_url = 'redis://localhost:6379/0'

app.conf.beat_schedule = {
    #'update_everyday': {
    #    'task': 'tracker.tasks.update_all_trackers',
    #    'schedule': crontab(hour=3, minute=0),
    #},
    #'send_mail_every_2_days': {
    #    'task': 'tracker.tasks.send_mails',
    #    'schedule': crontab(hour=15, minute=30, day_of_week='1,3,5,6'),
    #}
}
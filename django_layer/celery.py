import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('django_bot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    # Сохраняем данные о кликах по ссылкам каждый час одним большим запросом bulk_create
    'saver_info': {
        'task': 'service.tasks.saver_info',
        'schedule': crontab(minute='0', hour='*/1'),
    },
}
app.conf.timezone = 'UTC'

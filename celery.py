import os
from celery import Celery

# Установи переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Создай экземпляр Celery
app = Celery('your_project')

# Загрузи настройки из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживай задачи в приложениях
app.autodiscover_tasks()
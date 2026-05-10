from celery import Celery

from app.core.config.settings import settings

celery_app = Celery("adaptive_workflow_system", include=["app.workers.ai_tasks"])


celery_app.conf.broker_url = settings.REDIS_URL

celery_app.conf.result_backend = settings.REDIS_URL

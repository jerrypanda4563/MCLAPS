from celery import Celery
from app import settings
from app.redis_config import cache

simulator=Celery('mclaps', broker=settings.REDIS_URI)


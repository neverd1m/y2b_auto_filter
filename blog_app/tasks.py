# from .models import Filter, Video
from celery import shared_task, app

"""
Асинхронная задача, обрабатывающая регулярные запросы
по каждому фильтру к Ютубу.
"""


@shared_task
def hello():
    print('Hello there!')

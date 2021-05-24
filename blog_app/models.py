from django.db import models
from django.db.models.aggregates import Max
from django.db.models.fields import CharField, DateTimeField
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.urls import reverse
from .secrets import youtube_api

# сторонняя библиотека, чтобы транслировать кириллицу.
from slugify import slugify

from datetime import datetime
import requests

# https://developers.google.com/youtube/v3/docs/search/list

# статические параметры запроса.
# part = models.CharField(max_length=100, default='snippet')
# type = models.CharField(max_length=100, default='video')
# order = models.CharField(max_length=100, default='viewCount')


class Filter(models.Model):
    name = models.CharField('Наименование фильтра', max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE, related_name='created_filters')
    created_at = models.DateTimeField(auto_now_add=True)
    text_request = models.CharField('Поисковый запрос', max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=False)

    # дату отсчета для поиска указывать буду во вьюхах,
    # чтобы сделать несколько разных вариантов - за день, за неделю.
    time_interval = models.DurationField(blank=True, null=True)
    # published_after = models.DateTimeField(blank=True, null=True)

    # категория фильтра, исходя из списка категорий youtube.
    # запрос на стадии перехода к странице создания фильтра?
    # https://developers.google.com/youtube/v3/docs/videoCategories/list
    category = models.CharField(max_length=200, blank=True)

    # Подписчики фильтра.
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='sub_filters', blank=True)

    videos = models.ManyToManyField(
        'Video', related_name='filters', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("filter_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.name + '-' + str(timezone.now().date()))
        super().save(*args, **kwargs)

    def add_subscriber(self, user):
        self.subscribers.add(user)
        return self

    def remove_subscriber(self, user):
        self.subscribers.remove(user)
        return self

    def get_videos(self):
        payload = {
            'part': 'snippet',
            'type': 'video',
            'order': 'viewCount',
            'key': f'{youtube_api}',
            'maxResults': 5,
            'videoCategoryId': self.category,
            'published_after': datetime.now() - self.time_interval
        }
        videos = requests.get(
            'https://www.googleapis.com/youtube/v3/search', params=payload).json()
        return videos


class Video(models.Model):
    name = models.CharField(("Имя видео"), max_length=100)
    youtube_id = models.CharField(("Идентификатор видео"), max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)

    # сохранившие видео к себе.
    subscriber = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=("videos"))

    category = models.CharField(max_length=200)

    def __str__(self):
        return self.name

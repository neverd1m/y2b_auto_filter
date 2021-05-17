from django.forms import widgets
from django.forms.widgets import HiddenInput, RadioSelect
import requests

from django.contrib.auth.models import User

from django import forms
from django.db.models import fields
from .models import Filter, Video

from .secrets import youtube_api


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ('name', 'author', 'text_request',
                  'published_after', 'category', 'subscribers')
        # скрываю поля из формы, которые косвенно зависят от ввода.
        widgets = {'category': forms.HiddenInput(),
                   'author': forms.HiddenInput(),
                   'subscribers': forms.HiddenInput(),
                   'published_after': forms.HiddenInput()
                   }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'youtube_id', 'created_at', 'category')
        # skipped subs


class VideoCategoriesForm(forms.Form):

    publish_filter = forms.ChoiceField(label='Интервал поиска', choices=[
                                       (1, 'За 5 минут'), (2, 'За день'), (3, 'За неделю')])

    # создание поля с динамически изменяемым параметром choices
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = requests.get(
            'https://www.googleapis.com/youtube/v3/videoCategories', params={
                'part': 'snippet',
                'key': f'{youtube_api}',
                'regionCode': 'RU'
            }).json()

        # доступ к нужным полям согласно документации.
        # https://developers.google.com/youtube/v3/docs/videoCategories/list
        categories = ((item['id'], item['snippet']['title'])
                      for item in categories['items'])
        some_choices = list(categories)
        # print(some_choices)
        self.fields['category'] = forms.ChoiceField(
            label='Категория видео', choices=some_choices)


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('name',)

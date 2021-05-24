from django.core.files.base import File
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView

from .forms import FilterForm, VideoForm, VideoCategoriesForm
from .models import Filter, Video
from datetime import date, timedelta, datetime

from .secrets import youtube_api


class FilterCreateView(LoginRequiredMixin, View):

    """
    Представление, создающее новый фильтр из двух форм.
    Возвращает детальный вью на созданный фильтр.
    """

    interval = {'1': 1, '2': 7, '4': 30, '4': 5}
    model = Filter

    def get(self, request):
        form = VideoCategoriesForm()
        model_form = FilterForm()
        return render(request, 'blog_app/filter_create.html', context={'form': form, 'model_form': model_form})

    def post(self, request):
        form = VideoCategoriesForm(request.POST)
        model_form = FilterForm(request.POST)
        if model_form.is_valid() and form.is_valid():
            filter_object = model_form.save(commit=False)
            filter_object.author = request.user
            filter_object.category = form.cleaned_data['category']
            time_interval = form.cleaned_data['publish_filter']
            time_interval = self.interval[time_interval]

            # проверяю какой интервал указан в форме.
            # вариант с 5 минут, чтобы дальше тестить.
            if time_interval == 5:
                filter_object.time_interval = timedelta(minutes=5)
            else:
                filter_object.time_interval = timedelta(days=time_interval)

            filter_object.save()
            filter_object.add_subscriber(request.user)
            return redirect(filter_object)
        return render(request, 'blog_app/filter_create.html', context={'form': form, 'model_form': model_form})


class VideoCreateView(View):
    template_name = 'blog_app/video_create.html'

    def get(request, self):
        pass

    def post(request, self):
        pass


class FilterListView(LoginRequiredMixin, ListView):

    """
    Представление отображающее список всех фильтров в базе
    """

    model = Filter
    template_name = 'blog_app/filter_list.html'
    paginate_by = 5
    context_object_name = 'filters'
    ordering = ['-created_at']


class MySubsListView(LoginRequiredMixin, ListView):

    """
    Представление, отображающее список фильтров, 
    на которые подписан пользователь.
    """

    model = Filter
    template_name = 'blog_app/filter_list.html'
    paginate_by = 5
    context_object_name = 'filters'
    ordering = ['-created_at']

    def get_queryset(self):
        return Filter.objects.filter(subscribers=self.request.user).order_by("-created_at")


class FilterDetailView(LoginRequiredMixin, DetailView):

    """
    Представление с деталями конкретного фильтра
    """

    model = Filter
    template_name = 'blog_app/filter_detail.html'
    context_object_name = 'filter'


class FilterSubscribeToView(LoginRequiredMixin, View):

    """
    Представление, обрабатывающее запрос при нажатии кнопки Подписаться.
    Возвращает представление последнего фильтра.
    """

    model = Filter

    def get(self, request):
        return redirect(self)

    def post(self, request, slug):
        filter = Filter.objects.get(slug=slug)
        filter.add_subscriber(request.user)
        return redirect(filter)

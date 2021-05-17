import requests
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView

from .forms import FilterForm, VideoForm, VideoCategoriesForm
from .models import Filter, Video

from .secrets import youtube_api


class FilterCreateView(LoginRequiredMixin, View):
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
            filter_object.save()
            return render(redirect(filter_object))
        return render(request, 'blog_app/filter_create.html', context={'form': form, 'model_form': model_form})


class VideoCreateView(View):
    template_name = 'blog_app/video_create.html'

    def get(request, self):
        pass

    def post(request, self):
        pass


class FilterListView(LoginRequiredMixin, ListView):
    model = Filter
    template_name = 'blog_app/filter_list.html'
    paginate_by = 5
    context_object_name = 'filters'

# payload = {
#             'part': 'snippet',
#             'type': 'video',
#             'order': 'viewCount',
#             'key': f'{youtube_api}'
#         }
#         categories = requests.get(
#             'https://developers.google.com/youtube/v3/docs/search/list', params=payload).json()


class FilterDetailView(LoginRequiredMixin, DetailView):
    model = Filter

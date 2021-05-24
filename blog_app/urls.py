"""you_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views


urlpatterns = [
    path('filters/subscribed/', views.MySubsListView.as_view(),
         name='filter_subscribed'),
    path('filters/create/', views.FilterCreateView.as_view(),
         name='filter_create'),
    path('filters', views.FilterListView.as_view(), name='filter_list'),
    path('filters/<slug:slug>/',
         views.FilterDetailView.as_view(), name='filter_detail'),
    path('filters/<slug:slug>/subscribe/',
         views.FilterSubscribeToView.as_view(), name='subscribe_to'),
]

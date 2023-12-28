"""Drone URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url
from . import search, Astar, getRealLandmark

urlpatterns = [
    url(r'^search/$', search.search),
    url(r'^search-pos-info/$', search.search_pos_info),
    url(r'^search-path/$', Astar.search_path),
    url(r'^search-all-path/$', search.search_all_path),
    url(r'^find-target-multiPath/$', search.find_target_multiPath),
    url(r'^find-shortest-path/$', search.find_shortest_path),
    url(r'^add-new-pos/$', getRealLandmark.add_new_pos),
    url(r'^delete-pos/$', getRealLandmark.delete_pos),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/search/')),
]

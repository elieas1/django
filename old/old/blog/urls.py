from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blog.as_view(), name='blog'),
    path('<slug>', views.entry.as_view(), name='entry'),
]

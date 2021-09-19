from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Blog
# Create your views here.


class blog(ListView):
    template_name = 'blog/blog.html'
    model = Blog
    context_object_name = 'blogs'


class entry(DetailView):
    template_name = 'blog/entry.html'
    model = Blog
    context_object_name = 'blog'

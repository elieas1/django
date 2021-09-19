from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name="index/home.html"), name='index'),
    path('jobs', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.jobListing, name='jobListing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

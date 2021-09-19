from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("newentry", views.newentry, name = "newentry"),
    path("randomentry",views.randomentry, name = "random"),
    path("edit", views.editentry, name = "editentry"),  
    path("<str:link>", views.entry, name = "entry"),
]

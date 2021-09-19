
from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("asd/<str:profile>",views.asd,name="asd"),
    path("un", views.un, name="un"),
    path("following",views.following,name = "following"),
    path("<str:name>", views.profile, name="profile"),
    path("post/<int:id>",views.postid, name = "postid"),

]

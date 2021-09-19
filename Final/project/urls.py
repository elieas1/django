from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login",views.loginuser,name="login"),
    path("logout",views.logoutuser, name = "logout"),
    path("profile/<slug:account>",views.profile,name="profile"),
    path("page/<slug:page>",views.page,name="page"),
    path("register",views.register,name="register"),
    path("post/<slug:postslug>",views.postview.as_view(),name="post"),
    path("following",views.following.as_view(),name = "following"),
    path("api/<str:button>/<slug:account>",views.api,name = "api"),
    path('api/comment/<slug:postname>/<str:user>',views.addcomment,name='addcomment'),
    path("api/<str:mailbox>", views.mailbox.as_view(), name="mailbox"),
    path('api1/<slug:title>',views.postupvote,name = 'postupvote')
]   + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

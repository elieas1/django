import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import math

from .models import User,Post,Following,Likes


def index(request):
    if request.method == "POST":
        textarea = request.POST.get("textarea")
        add = Post(name = request.user,posts = textarea)
        add.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        likes = Likes.objects.filter(user = request.user)
        posts = Post.objects.all().order_by('-date')
        postcount = Post.objects.all().order_by('-date').count()
        number = math.ceil(postcount/10)
        qwerty = []
        if likes:
            for like in likes:
                qwerty.append(like.like.id)

        paginator = Paginator(posts,10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html",{
            'page_obj': page_obj,
            'qwerty':qwerty,
            'number':range(1,number+1)
        })

@csrf_exempt
@login_required
def profile(request,name):

    if request.method == "GET":
        user = User.objects.filter(username = name)
        following = Following.objects.filter(followinguser = request.user)

        posts = Post.objects.filter(name = name).order_by('-date')
        postcount = posts.count()
        number = math.ceil(postcount/10)
        paginator = Paginator(posts,10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        qwerty = []
        if following:
            for i in following:
                qwerty.append(i.followeduser)

            for n in qwerty:
                if name == n:
                    qwe = True
                    break
                else:
                    qwe = False
        else:
            qwe = False  
        if user:
            return render(request, "network/profile.html",{
                'page_obj':page_obj,
                'user1': user,
                "profile":name,
                'following':qwerty,
                'qwe':qwe,
                'number':range(1,number+1),
                'count':postcount
            })

        else:
            return HttpResponse(status=404)

    elif request.method == "POST":
        data = json.loads(request.body)
        followeduser = data.get("followeduser","")
        data = Following.objects.filter(followinguser = request.user,followeduser = followeduser)
        if data:
            data.delete()
        else:
            add = Following(followinguser = request.user,followeduser = followeduser)
            add.save()
        return HttpResponse(status=204)

@csrf_exempt
@login_required
def asd(request,profile):
    if request.method == "GET":
        profiles = User.objects.filter(username = profile)
        return JsonResponse([profile.serialize() for profile in profiles], safe=False)
    elif request.method == "PUT":
        user = User.objects.get(username = profile)
        data = json.loads(request.body)
        if data.get("followers") is not None:
            user.followers = data["followers"]
        user.save()
        return HttpResponse(status=204)
    
@csrf_exempt
@login_required
def un(request):
    if request.method == "PUT":
        myprofile = User.objects.get(username = request.user)
        data = json.loads(request.body)
        if data.get("following") is not None:
            myprofile.following = data["following"]
        myprofile.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)

@login_required
def following(request):
    likes = Likes.objects.filter(user = request.user)
    qwerty = []
    if likes:
        for like in likes:
            qwerty.append(like.like.id)
    following = Following.objects.values_list('followeduser',flat=True).filter(followinguser=request.user)
    list=[]
    for i in following:
        list.append(i)
    
    following = Post.objects.filter(name__in=list).order_by('-date')
    postcount = Post.objects.filter(name__in=list).order_by('-date').count()
    number = math.ceil(postcount/10)

    paginator = Paginator(following,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html",{
        'page_obj':page_obj,
        'qwerty':qwerty,
        'number':range(1,number+1),
        'list':list,
    })

@csrf_exempt
@login_required
def postid(request,id):
    if request.method == "GET":
        post = Post.objects.get(id = id)
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        post = Post.objects.get(id = id)
        data = json.loads(request.body)
        if data.get("posts") is not None:
            post.posts = data["posts"]
        if data.get("likes") is not None:
            post.likes = data["likes"]
        post.save()
        return HttpResponse(status=204)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        like = data.get("like","")
        like = Post.objects.get(id = like)
        data = Likes.objects.filter(user = request.user,like = like)
        if data:
            data.delete()
        else:
            add = Likes(user = request.user,like = like)
            add.save()
        return HttpResponse(status=204)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "network/register.html")

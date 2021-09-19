from django.shortcuts import render, HttpResponse, Http404, reverse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Post, Page, Comment, Email
from .forms import registeruser
from django.db.models import F
import json
from django.views import View
from django.http import JsonResponse
from slugify import slugify


from .forms import postform
# Create your views here.


def index(request):

    if request.user.is_authenticated:
        if request.method == "POST" and request.POST.get("submitpost"):
            data = postform(request.POST)
            if data.is_valid():
                f = Post(username=request.user, category=Page.objects.get(
                    id=request.POST["category"]), title=request.POST["title"], body=request.POST["body"])
                f.slug = slugify(request.POST.get("title"))
                f.save()
            else:
                return HttpResponse(status=404)
            return render(request, "project/post.html")
        return render(request, "project/home.html", {
            "posts": Post.objects.all(),
            "category": Page.objects.order_by("pagename"),
        })
    else:
        return redirect("login")


def profile(request, account):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        if request.method == "GET":
            return render(request, "project/profile.html", {
                "profile": User.objects.get(username=account),
                "account": account,
                "userinfo": User.objects.get(username=request.user)
            })

        elif request.method == "PUT":
            data = json.loads(request.body)
            q = User.objects.get(username=request.user)
            a = User.objects.get(username=account)
            if not q.following.all():
                q.following.add(a)
            else:
                list = []
                for f in q.following.all():
                    list.append(f.username)
                if account in list:
                    q.following.remove(a)
                else:
                    q.following.add(a)

            if not a.followers.all():
                a.followers.add(q)
            else:
                list2 = []
                for f in a.followers.all():
                    list2.append(f.username)
                if request.user.username in list2:
                    a.followers.remove(q)
                else:
                    a.followers.add(q)
            return HttpResponse(status=204)

        elif request.method == "POST" and request.POST.get("submitdesc"):
            user = User.objects.get(username=request.user.username)
            user.description = request.POST.get("description")
            user.save()
            return HttpResponseRedirect(reverse("profile", kwargs={
                "account": request.user.username
            }))


def loginuser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "project/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "project/login.html")


def api(request, button, account):
    if button == "posts":
        query = Post.objects.filter(username__username=account)
    elif button == "followers":
        query = User.objects.filter(username=account)
    elif button == "following":
        query = User.objects.filter(username=account)
    elif button == "comments":
        query = Comment.objects.filter(username__username=account)

    return JsonResponse({"query": [q.serialize() for q in query], "user": [user.serialize() for user in User.objects.filter(username=request.user.username)]}, safe=False)


def logoutuser(request):
    logout(request)
    return render(request, "project/login.html")


def register(request):
    form = registeruser()
    if request.method == "POST":
        form = registeruser(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data["password1"] != data["password2"]:
                return HttpResponseRedirect(reverse('register'))
            else:
                user = User.objects.create_user(
                    username=data["username"], password=data["password1"], email=data["email"])
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "project/register.html", {"form": form})
    else:
        return render(request, "project/register.html", {"form": form})


def page(request, page):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        pageposts = Post.objects.filter(category__pagename=page)
        return render(request, "project/page.html", {
            "pageposts": pageposts,
            "page": Page.objects.get(pagename=page),
            "category": Page.objects.order_by("pagename"),
        })


class postview(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, postslug):
        request.session['username'] = request.user.username
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
        post = Post.objects.filter(slug=postslug)
        return render(request, "project/post.html", {
            "postinfo": post
        })


class following(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "project/following.html", {
                "posts": Post.objects.filter(username__in=User.objects.filter(username=request.user.username).values_list("following")),
                "category": Page.objects.order_by("pagename"),
            })
        else:
            return redirect("login")


class mailbox(View):
    def get(self, request, mailbox):
        if mailbox == 'inbox':
            emails = Email.objects.filter(
                recipient=request.user, archived=False
            )
        elif mailbox == 'sent':
            emails = Email.objects.filter(
                sender=request.user
            )
        elif mailbox == 'archived':
            emails = Email.objects.filter(
                recipient=request.user, archived=True
            )

        return JsonResponse({'mail': [mail.serialize() for mail in emails]})

    def POST(self, request, mailbox):
        data = json.loads(request.body)
        if data:
            recipients = [name.strip()
                          for name in data.get("recipients").split(",")]
        else:
            return JsonResponse({
                "error": "At least one recipient required."
            }, status=400)
        if recipients == [""]:
            return JsonResponse({
                "error": "At least one recipient required."
            }, status=400)
        for name in recipients:
            if name not in User.objects.values_list('username'):
                return JsonResponse({
                    "error": "recipient does not exist."
                }, status=400)
        mail = Email(sender=request.user, subject=data.get(
            "subject"), body=data.get("body"))
        mail.save()
        for name in recipients:
            mail.recipient.add(User.objects.get(username=name))
            mail.save()
        return JsonResponse('sent', safe=False)


def addcomment(request, postname, user):
    if request.method == "GET":
        comments = Comment.objects.filter(
            post=Post.objects.get(username__username=user, slug=postname)).order_by('-date')
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        title = slugify(data.get('post'))
        comment = data.get('comment')
        if comment:
            add = Comment(username=request.user, comm=data.get(
                'comment'), post=Post.objects.get(slug=title))
            add.save()
            return JsonResponse('sent', safe=False)
        else:
            return JsonResponse('failed', safe=False)


def postupvote(request, title):
    if request.method == 'GET':
        likes = Post.objects.get(slug=title)
        return JsonResponse({'array': [user.title for user in request.user.upvotedposts.all()], "likes": likes.likes}, safe=False)
    elif request.method == "PUT":
        data = json.loads(request.body)
        title = data.get('post')
        name = data.get('user')
        print(data)
        user = request.user
        try:
            post = user.upvotedposts.get(slug=title)
            user.upvotedposts.remove(Post.objects.get(
                slug=title, username__username=name))
            like = Post.objects.get(slug=title, username__username=name)
            like.likes = F('likes')-1
        except Post.DoesNotExist:
            user.upvotedposts.add(Post.objects.get(
                slug=title, username__username=name))
            like = Post.objects.get(slug=title, username__username=name)
            like.likes = F('likes')+1

        user.save()
        like.save()
        return HttpResponse(200)
    else:
        return HttpResponse(403)

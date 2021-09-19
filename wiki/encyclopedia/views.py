from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from markdown2 import Markdown
from django.urls import path

from . import util


def index(request):

    if request.method == "POST":
        page = request.POST.get("q")
        if util.get_entry(page):
            return HttpResponseRedirect(reverse('entry', args={page}))
        else:
            return render(request, "encyclopedia/like.html", {
                "entries": util.list_entries(),"name":page.capitalize(),"name1":page.upper(),"name2":page.lower()})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request,link):

    if request.method == "POST":
        page = request.POST.get("q")
        if util.get_entry(page):
            return HttpResponseRedirect(reverse('entry', args={page}))
        else:
            return render(request, "encyclopedia/like.html", {
                "entries": util.list_entries(),"name":page.capitalize(),"name1":page.upper(),"name2":page.lower()})
    else:

        if util.get_entry(link):
            markdowner = Markdown()
            text = markdowner.convert(util.get_entry(link))
            return render(request, "encyclopedia/links.html", {
                "link": text,"name":link})
        else:
            return render(request, "encyclopedia/links.html", {
                    "link": util.get_entry(link),"name":link})

def newentry(request):
    if request.method == "POST" and request.POST.get("q"):
        page = request.POST.get("q")
        if util.get_entry(page):
            return HttpResponseRedirect(reverse('entry', args={page}))
        else:
            return render(request, "encyclopedia/like.html", {
                "entries": util.list_entries(),"name":page.capitalize(),"name1":page.upper(),"name2":page.lower()})
    else:
        if request.method == "POST" and not request.POST.get("zxc"):
            title = request.POST.get("title")
            desc = request.POST.get("desc")
            for c in util.list_entries():
                if c.lower() == title.lower():
                    return render(request, "encyclopedia/error.html")
            util.save_entry(title,desc)
            return HttpResponseRedirect(reverse('entry', args={title}))
        elif request.method == "POST" and request.POST.get("zxc"):
            nf = request.POST.get("zxc")
            return render(request, "encyclopedia/new.html",{"nf":nf})
        else:
            return render(request, "encyclopedia/new.html")

def randomentry(request):
    if request.method == "POST":
        page = request.POST.get("q")
        if util.get_entry(page):
            return HttpResponseRedirect(reverse('entry', args={page}))
        else:
            return render(request, "encyclopedia/like.html", {
                "entries": util.list_entries(),"name":page.capitalize(),"name1":page.upper(),"name2":page.lower()})
    else:
        list = []
        entries = util.list_entries()
        for entry in entries:
            list.append(entry)

        rand = random.choice(list)
        return HttpResponseRedirect(reverse('entry', args={rand}))

def editentry(request):
    if request.method == "POST" and request.POST.get("q"):
        page = request.POST.get("q")
        if util.get_entry(page):
            return HttpResponseRedirect(reverse('entry', args={page}))
        else:
            return render(request, "encyclopedia/like.html", {
                    "entries": util.list_entries(),"name":page.capitalize(),"name1":page.upper(),"name2":page.lower()})
    else:
        if request.method == "POST" and request.POST.get("qwe"):
            title = request.POST.get("qwe")
            return render(request, "encyclopedia/edit.html", {
                "link": util.get_entry(title),"title":title.upper()})
        else:
            title = request.POST.get("asd")
            desc = request.POST.get("editdesc")
            util.save_entry(title,desc)
            return HttpResponseRedirect(reverse('entry', args={title}))
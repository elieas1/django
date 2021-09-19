from django.shortcuts import render
from django.shortcuts import render, HttpResponse, Http404, reverse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.contrib import messages


from django_email_verification import send_email
from django.core.mail import EmailMessage

from .models import User

from .forms import registeruser


# def register_view(request):
#     if request.user.is_authenticated:
#         return(HttpResponseRedirect(reverse('index')))
#     else:
#         form = registeruser()
#         if request.method == "POST":
#             form = registeruser(request.POST)
#             if form.is_valid():
#                 data = form.cleaned_data
#                 if data["password"] != data["password_conf"]:
#                     return HttpResponseRedirect(reverse('register'))
#                 else:
#                     try:
#                         user = User.objects.create_user(
#                             data['email'], data['email'], data['password'])
#                         user.first_name = data['firstname']
#                         user.last_name = data['lastname']
#                         user.is_active = False
#                         send_email(user)
#                         messages.info(
#                             request, f"An email has been sent to {data['email']}.If you didn't recieve the email, please click here to resend")
#                         return HttpResponseRedirect(reverse('register'))
#                     except IntegrityError:
#                         try:
#                             user = User.objects.get(email=data['email'])
#                             if user and user.is_active == False:
#                                 send_email(user)
#                                 messages.info(
#                                     request, f"An email has been sent to {data['email']}.If you didn't recieve the email, please click here to resend")
#                                 return HttpResponseRedirect(reverse('register'))
#                             # user is confirmed
#                             else:
#                                 return HttpResponseRedirect(reverse('register'))
#                         except:
#                             messages.info(
#                                 request, f"something went wrong")
#                             return HttpResponseRedirect(reverse('register'))
#             else:
#                 return render(request, "accounts/register.html", {"form": form})
#         else:
#             return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        print('authenticated')
        return(HttpResponseRedirect(reverse('index')))
    else:
        print('not auth')
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user = User.objects.get(email=email)
                passw = user.check_password(password)

                if passw:
                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')
                    return HttpResponseRedirect(reverse("index"))
                else:
                    messages.warning(
                        request, 'Invalid username and/or password.')
                    return redirect('accounts:login')

            except:
                print('error')
                return redirect('magiclink:login')
        else:
            return redirect('magiclink:login')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def profile(request):
    if request.user.is_authenticated:
        if request.method =='GET':
            return render(request,'accounts/profile.html')
        elif request.method == 'POST':
            print(request.POST)
            return redirect('accounts:profile')
    else:
        return(HttpResponseRedirect(reverse('accounts:login')))

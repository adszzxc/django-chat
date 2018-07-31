from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from . import forms
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.db import IntegrityError

def main_login(request):
    if request.method == "POST":
        if "nickname" in str(request.POST):
            form = forms.RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                nickname = cd["nickname"]
                password = cd["password"]
                email = cd["email"]
                avatar = cd["avatar"]
                try:
                    new_user, created = User.objects.get_or_create(email=email,
                                    nickname=nickname,
                                    avatar=avatar)
                    new_user.set_password(password)
                    new_user.is_active = False
                    new_user.save()
                except IntegrityError:
                    return render(request, "infostring.html", {"infostring":"There's already a user with this email!"})
                current_site = get_current_site(request)
                message = render_to_string("acc_activate_email.html", {
                    "user":new_user,
                    "domain":current_site.domain,
                    "usercode":new_user.usercode,
                    "token": account_activation_token.make_token(new_user),
                    })
                mail_subject = "Django chat account activation"
                to_email = email
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request, "infostring.html", {"infostring":"Please confirm your email address to complete the registration."})
        else:
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                email = cd["email"]
                password = cd["password"]
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect("index")
                    else:
                        return render(request, "infostring.html", {"infostring":"Banned or not activated"})
                else:
                    return render(request, "infostring.html", {"infostring":repr(cd)})
    else:
        register_form = forms.RegisterForm()
        login_form = forms.LoginForm()
        return render(request, "login.html", {"register_form":register_form,
                                              "login_form":login_form,})

def activate(request, usercode, token):
    try:
        user = User.objects.get(usercode=usercode)
    except Exception as E:#(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return HttpResponse(repr(E))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Token.objects.create(user=user)
        return redirect("index")
    else:
        return render(request, "infostring.html", {"infostring":"Activation link is invalid!"})

@login_required
def index(request):
    token = Token.objects.get(user=request.user)
    return render(request, "index.html", {"token":token,})

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")

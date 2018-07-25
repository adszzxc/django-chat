from django.urls import path, include
from django.shortcuts import render
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.main_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("activate/<str:usercode>/<str:token>/", views.activate, name="activate"),
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/<str:nick>/', views.profile),
]

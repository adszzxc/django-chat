from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/<str:nick>/', views.profile),
    path('auth/', include('rest_auth.urls')),
    path("messages/create/", views.create_message),
]

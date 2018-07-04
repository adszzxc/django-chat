from django.shortcuts import render
from main.models import Profile
from .serializers import ProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(["GET"])
def profile(request, nick):
    try:
        profile = Profile.objects.get(nickname=nick)
        serializer = ProfileSerializer(profile)
        if request.user.is_authenticated:
            data = serializer.data
        else:
            data = {
                "message":"User is not authenticated!"
                }
    except Exception as E:
        data = {"message":str(E)}
    return JsonResponse(data)

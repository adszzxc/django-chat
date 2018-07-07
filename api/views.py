from django.shortcuts import render
from django.contrib.auth import authenticate, login
from main.models import Profile, Message
from .serializers import ProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
import json

@api_view(["GET"])
def profile(request, nick):
    try:
        profile = Profile.objects.get(nickname=nick)
        serializer = ProfileSerializer(profile)
        if request.user.is_authenticated:
            data = serializer.data
        else:
            data = {
                "message":"user is not authenticated!"
                }
    except Exception as E:
        data = {"message":str(E)}
    return Response(data)

@api_view(["POST"])
def create_message(request):
    body_unicode = request.body.decode('utf-8')
    payload = json.loads(body_unicode)
    chat = payload["chat"]
    author = request.user.profile
    content = payload["content"]
    Message.objects.create(chat=chat,
                           author=author,
                           content=content).save()
    return Response({"message":"success"})
    
    
            
        

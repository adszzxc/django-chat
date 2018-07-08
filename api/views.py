from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from main.models import Profile, Message, Chat
from .serializers import ProfileSerializer, MessageSerializer, ChatSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
import uuid
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

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
#@permission_classes((IsAuthenticated,))
def create_message(request):
    body_unicode = request.body.decode('utf-8')
    payload = json.loads(body_unicode)
    usercode = payload["usercode"]
    
    p1 = request.user.profile
    p2 = get_object_or_404(Profile, usercode=usercode)

    query = Chat.objects.filter(participants__in=[p1]).filter(participants__in=[p2])

    if query.exists():
        chat_obj = query[0]
        Message.objects.create(chat=chat_obj,
                               author=p1,
                               content=payload["content"])
        return Response({"message":"sent message"})
    else:
        chat_obj = Chat.objects.create()
        chat_obj.participants.add(p1)
        chat_obj.participants.add(p2)
        chat_obj.save()
        Message.objects.create(chat=chat_obj,
                               author=p1,
                               content=payload["content"])
        
        return Response({"message":"created Chat, sent message"})


#
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
#

@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def register_user(request):
    body_unicode = request.body.decode('utf-8')
    payload = json.loads(body_unicode)
    username = payload["username"]
    password = payload["password"]
    email = payload["email"]

    user_obj = User.objects.create(username=username,
                                   password=password,
                                   email=email)
    while True:
        usercode = uuid.uuid4().hex[:10]
        if Profile.objects.filter(usercode=usercode).exists():
            pass
        else:
            break
    profile_obj = Profile.objects.create(user=user_obj,
                                        nickname=user_obj.username,
                                        usercode=usercode)
    return Response({"message":"User and Profile created succesfully."})

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def get_messages(request, interlocutor, amount):
    p1 = request.user.profile
    p2 = get_object_or_404(Profile, usercode=interlocutor)
    query = Chat.objects.filter(participants__in=[p1]).filter(participants__in=[p2])
    if query.exists():
        chat_obj = query[0]
        messages_objs = chat_obj.messages.all()[:int(amount)]
        serializer = MessageSerializer(messages_objs, many=True)
        return Response(serializer.data)
    else:
        return Response({"message":"cannot get messages because no such Chat exist"})
    
    

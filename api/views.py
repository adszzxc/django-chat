from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from main.models import Profile, Message, Chat
from .serializers import ProfileSerializer, MessageSerializer, FriendSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
import uuid
import json
from rest_auth.views import LogoutView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
@authentication_classes((TokenAuthentication, SessionAuthentication, BasicAuthentication,))
#@permission_classes((IsAuthenticated,))
def create_message(request):
    channel_layer = get_channel_layer()
    #decoding request.body, Python 3.5.X specific
    body_unicode = request.body.decode('utf-8')
    payload = json.loads(body_unicode)

    usercode = payload["usercode"]
    #getting users, one is authenticated and other will throw 404 if doesn't exist
    p1 = request.user.profile
    p2 = get_object_or_404(Profile, usercode=usercode)

    #creating a Chat queryset that contains both Profiles as participants
    query = Chat.objects.filter(participants__in=[p1]).filter(participants__in=[p2])

    #checking if query exists, if not then a new Chat is created
    if query.exists():
        chat_obj = query[0]
        #send message to websocket group of target Profile
        async_to_sync(channel_layer.group_send)(str(p2.usercode),
                                        {"type":"chat.message",
                                            "usercode":str(p1.usercode),
                                            "text":payload["content"]})
        Message.objects.create(chat=chat_obj,
                               author=p1,
                               content=payload["content"])
        return Response({"message":"sent message"})
    else:
        #send message to websocket group of target Profile
        async_to_sync(channel_layer.group_send)(str(p2.usercode),
                                            {"type":"chat.message",
                                            "usercode":str(p1.usercode),
                                            "text":payload["content"]})
        chat_obj = Chat.objects.create()
        chat_obj.participants.add(p1)
        chat_obj.participants.add(p2)
        chat_obj.save()
        Message.objects.create(chat=chat_obj,
                               author=p1,
                               content=payload["content"])
        return Response({"message":"created Chat, sent message"})



#a class to bypass CRSFToken authentication on registration
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication,))
@permission_classes((AllowAny,))
def register_user(request):
    #decoding body is Python 3.5.X specific
    body_unicode = request.body.decode('utf-8')
    payload = json.loads(body_unicode)
    #getting registration details
    username = payload["username"]
    password = payload["password"]
    email = payload["email"]

    #creating User object
    user_obj = User.objects.create(username=username,
                                   password=password,
                                   email=email)

    #generating secret usercode used in various places of the project
    while True:
        usercode = uuid.uuid4().hex[:10]
        if Profile.objects.filter(usercode=usercode).exists():
            pass
        else:
            break
    #creating Profile related to the previously created User
    profile_obj = Profile.objects.create(user=user_obj,
                                        nickname=user_obj.username,
                                        usercode=usercode)
    return Response({"message":"User and Profile created succesfully."})

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_messages(request, interlocutor, amount):
    #getting Profiles
    p1 = request.user.profile
    p2 = get_object_or_404(Profile, usercode=interlocutor)
    #setting query as in create_message
    query = Chat.objects.filter(participants__in=[p1]).filter(participants__in=[p2])
    if query.exists():
        chat_obj = query[0]
        #getting objects according to requested amount
        messages_objs = chat_obj.messages.all()[:int(amount)]
        serializer = MessageSerializer(messages_objs, many=True)
        return Response(serializer.data)
    else:
        return Response({"message":"cannot get messages because no such Chat exist"})
    
@api_view(["GET"])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_friends(request):
    profile = request.user.profile
    #get all friends of a Profile
    qs = profile.friends.all()
    serializer = FriendSerializer(qs, many=True)
    return Response(serializer.data)

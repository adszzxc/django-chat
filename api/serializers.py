from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Chat, Message, User

class ProfileSerializer(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
#        many=True,
        read_only=True,
        slug_field="usercode"
    )
    class Meta:
        model = Message
        fields = ("author",
                  "content",
                  "created",
                  "image",
                  "file")
    

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname",
                  "usercode",
                  "avatar",
                  "is_active")

from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)
    class Meta:
        model = Profile
        fields = "__all__"


##class ProfileSerializer(serializers.Serializer):
##    nickname = serializers.CharField(max_length=200)
##    avatar = serializers.ImageField()
##    banned = serializers.BooleanField(default=False)
##    active = serializers.BooleanField(default=False)
##    usercode = serializers.CharField(max_length=100)
##    friends = FriendSerializer(many=True, read_only=True)

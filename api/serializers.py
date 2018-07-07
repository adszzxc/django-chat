from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)
    class Meta:
        model = Profile
        fields = "__all__"

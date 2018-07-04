from rest_framework import serializers

class ProfileSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=200)
    avatar = serializers.ImageField()
    banned = serializers.BooleanField(default=False)
    active = serializers.BooleanField(default=False)

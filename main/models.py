from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    avatar = models.ImageField(upload_to="images/users/%s/avatars/" % nickname,
                               null=True, blank=True)
    banned = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return ("{}'s profile".format(self.nickname))

class Chat(models.Model):
    participants = models.ManyToManyField(Profile)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="chat/%s/images/" % chat,
                              blank=True, null=True)
    file = models.ImageField(upload_to="chat/%s/files/" % chat,
                              blank=True, null=True)    

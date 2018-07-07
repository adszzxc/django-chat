from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'images/users/{}/{}'.format(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)
    nickname = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    avatar = models.ImageField(upload_to=user_directory_path,
                               null=True, blank=True)
    banned = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    usercode = models.CharField(max_length=100)

    def __str__(self):
        return (self.nickname)

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

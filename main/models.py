from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
import uuid
from .custom_manager import UserManager

##def user_directory_path(instance, filename):
##    return 'images/users/{}/{}'.format(instance.user.username, filename)


##class Profile(models.Model):
##    user = models.OneToOneField(User, on_delete=models.CASCADE)
##    friends = models.ManyToManyField("Profile", blank=True)
##    nickname = models.CharField(max_length=200)
##    created = models.DateField(auto_now_add=True)
##    avatar = models.ImageField(upload_to=user_directory_path,
##                               null=True, blank=True)
##    banned = models.BooleanField(default=False)
##    active = models.BooleanField(default=False)
##    usercode = models.CharField(max_length=100)
##
##    def __str__(self):
##        return (self.nickname)

class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="chat/%s/images/" % chat,
                              blank=True, null=True)
    file = models.ImageField(upload_to="chat/%s/files/" % chat,
                              blank=True, null=True)

def user_directory_path(instance, filename):
    return 'images/users/{}/{}'.format(instance.usercode, filename)

def create_profile_usercode():
    while True:
        code = uuid.uuid4().hex[:10]
        if not User.objects.filter(usercode=code).exists():
            return code

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email adress",
                              max_length=255, unique=True)
    nickname = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    avatar = models.ImageField(upload_to=user_directory_path,
                               null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    usercode = models.CharField(default=create_profile_usercode,
                                max_length=100)
    friends = models.ManyToManyField("self", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return "User {}".format(self.nickname)

    def get_full_name(self):
        full_name = "User {} {}".format(self.nickname, self.usercode)

    def get_short_name(self):
        return self.nickname
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

    @property
    def is_staff(self):
        return self.is_admin



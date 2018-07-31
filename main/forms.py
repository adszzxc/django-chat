from django.forms import ModelForm, Form
from main.models import User
from django import forms


class LoginForm(Form):
    email = forms.EmailField(label="email")
    password = forms.CharField(widget=forms.PasswordInput(),
                               label="hasło")

class RegisterForm(Form):
    email = forms.EmailField(label="email")
    nickname = forms.CharField(label="nick")
    password = forms.CharField(widget=forms.PasswordInput(),
                               label="hasło")
    avatar = forms.ImageField(required=False)

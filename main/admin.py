from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib import admin
from .models import Chat, Message

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("email", "nickname", "avatar")
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'avatar', 'is_active', 'is_admin', 'nickname')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('nickname', 'usercode', 'email')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {"fields":('email', 'password', 'usercode')}),
        ("Personal info", {"fields": ("nickname", "avatar", "friends",)}),
        ("Permissions", {"fields":("is_admin",)}),
        )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','nickname','password1', 'password2')}
         ),
        )
    ordering = ("nickname",)
    search_fields = ("nickname", "email", "usercode")
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.unregister(Group)

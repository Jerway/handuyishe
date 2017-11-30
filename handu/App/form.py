# coding=utf-8

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
# from .models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

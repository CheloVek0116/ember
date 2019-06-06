from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user', 'content',)


class SignUpForm(UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
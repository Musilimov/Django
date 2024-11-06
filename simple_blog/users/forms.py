from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProfileF

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileF
        fields = ['bio', 'profile_picture']
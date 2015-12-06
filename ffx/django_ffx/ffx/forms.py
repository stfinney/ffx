from django import forms
from models import Profile
from django.contrib.auth.models import User


class RegistrationUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class RegistrationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('major', 'address', 'phone')

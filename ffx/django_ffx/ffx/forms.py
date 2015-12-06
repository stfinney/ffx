from django import forms
from models import Profile, Event
from django.contrib.auth.models import User


class RegistrationUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class RegistrationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('major', 'address', 'phone')

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title','event_type', 'description',
            'event_date', 'event_endtime', 'address',
            'map_marker', 'location_text', 'capacity',
            'public', 'requires_major'
        )

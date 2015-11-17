from datetime import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from location_field.models.plain import PlainLocationField


class EventType(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField('brief description of the event type')



class Event(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField('description of the event')
    event_date = models.DateTimeField()
    event_duration = models.DurationField(blank=True, null=True, help_text='Length of event, leave blank for no set duration.')
    created_date = models.DateTimeField(default=datetime.now(),editable=False)
    address = models.CharField('address', max_length=128, default='', help_text='Can be as specific as a street address, or as broad as a city')
    map_marker = PlainLocationField(based_fields=[address], zoom=7, blank=True, help_text='Enter an address in the Address field to center the map on that location')
    location_text = models.TextField('additional location details', max_length=256, blank=True, help_text='Useful extra description of the location, if needed. Ex: in front of the Starbucks, or in Room 415 of Building 3A')
    organizer = models.ForeignKey(User,editable=False)
    capacity = models.PositiveIntegerField(help_text='Capacity must be positive, or enter 0 for no limit.', default=0, blank=True)
    public = models.BooleanField(default=True, help_text='If unchecked, event will only be visible to registered users')
    requires_major = models.CharField(max_length=100, help_text='Major required for attendance',blank=True)

    def __unicode__(self):
        return self.title.encode('utf-8')


class Registration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    reg_date = models.DateTimeField(default=datetime.now())
    # Add any extra relationship attributes here
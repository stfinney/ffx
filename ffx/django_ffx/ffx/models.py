from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    event_date = models.DateTimeField()
    created_date = models.DateTimeField(default=datetime.now())
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    organizer = models.ForeignKey(User)

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    # Add any extra relationship attributes here

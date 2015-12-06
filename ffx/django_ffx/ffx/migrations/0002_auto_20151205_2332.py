# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import uuid
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ffx', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(verbose_name=b'brief description of the event type')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('major', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='id',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location_latitude',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location_longitude',
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.CharField(default=b'', help_text=b'Can be as specific as a street address, or as broad as a city', max_length=128, verbose_name=b'address'),
        ),
        migrations.AddField(
            model_name='event',
            name='capacity',
            field=models.PositiveIntegerField(default=0, help_text=b'Capacity must be positive, or enter 0 for no limit.', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_duration',
            field=models.DurationField(help_text=b'Length of event, leave blank for no set duration.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location_text',
            field=models.TextField(help_text=b'Useful extra description of the location, if needed. Ex: in front of the Starbucks, or in Room 415 of Building 3A', max_length=256, verbose_name=b'additional location details', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='map_marker',
            field=location_field.models.plain.PlainLocationField(help_text=b'Enter an address in the Address field to center the map on that location', max_length=63, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='public',
            field=models.BooleanField(default=True, help_text=b'If unchecked, event will only be visible to registered users'),
        ),
        migrations.AddField(
            model_name='event',
            name='requires_major',
            field=models.CharField(help_text=b'Major required for attendance', max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='reg_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 5, 23, 32, 40, 497918)),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 5, 23, 32, 40, 496748), editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name=b'description of the event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]

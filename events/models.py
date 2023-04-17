from datetime import timedelta

from django.db import models
from django.utils import timezone

# Create your models here.


def one_hour_later():
    return timezone.now() + timedelta(hours=1)


class Event(models.Model):
    """
    Model Class for the Event Object.
    
    Fields:
        -title: str
        -description: str
        -address_link: url
        -start_time: datetime
        -end_time: datetime
        -capacity: int
        -minimum_age: int

        -created: datetime
        -updated: datetime
    """
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=20,blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now, blank=True,null=True)
    end_time = models.DateTimeField(
        default=one_hour_later, blank=True, null=True)
    owner=models.ForeignKey("accounts.user", models.CASCADE, null=True)

    # Meta info
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True, blank=True, null=True,)


class EventRSVP(models.Model):
    event=models.ForeignKey("events.event",models.CASCADE)
    user=models.ForeignKey("accounts.user", models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
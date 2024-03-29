from datetime import datetime
from django.db import models
from django.urls import reverse

from my_calendar.models import EventAbstract

from store.models import Customer


class EventManager(models.Manager):

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

    def get_upcoming_events(self, user):
        upcoming_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            start_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return upcoming_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("my_calendar:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("my_calendar:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
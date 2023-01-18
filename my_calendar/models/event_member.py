from django.db import models

from store.models import Customer
from my_calendar.models import Event, EventAbstract

class EventMember(EventAbstract):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="event_members")

    class Meta:
        unique_together = ["event", "user"]

    def __str__(self):
        return str(self.user)
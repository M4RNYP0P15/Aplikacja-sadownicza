from django.views.generic import ListView

from my_calendar.models import Event
from dictionary.models import user_plants

class AllEventsListView(ListView):
    template_name = "calendar/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)


class RunningEventsListView(ListView):
    template_name = "calendar/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)

class UpcomingEventsListView(ListView):
    template_name = "calendar/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_upcoming_events(user=self.request.user)


class AllUserPlants(ListView):
    template_name="plants_list.html"
    model= user_plants.UserPlant

    def get_queryset(self):
        objects = user_plants.UserPlant.objects.filter(user=self.request.user)
        return objects
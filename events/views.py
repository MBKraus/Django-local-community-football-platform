from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import CreateForm, UpdateForm
from . import models
from braces.views import PrefetchRelatedMixin
from geopy.geocoders import Nominatim

import datetime

# Search Box

def Search(request):

    term = request.GET.get('q')
    event = models.Event.objects.filter(Q(name__icontains=term)|Q(created_by__username__icontains=term)|Q(address__icontains=term))

    return render(request, 'events/search_list.html', {'event': event})

# Create Event

class CreateEvent(LoginRequiredMixin, generic.CreateView):

    form_class = CreateForm
    template_name = "events/event_form.html"
    model = models.Event

    def form_valid(self, form):

        response = super().form_valid(form)
        self.object = form.save(commit=False)
        self.object.created_by=self.request.user
        geolocator = Nominatim()
        geolocator_location = geolocator.geocode(self.object.address)
        self.object.latitude = geolocator_location.latitude
        self.object.longitude = geolocator_location.longitude
        self.object.save()
        models.EventMember.objects.create(
            event=self.object,
            user=self.request.user,
        )
        return response

# Single Event DetailView

class SingleEvent(PrefetchRelatedMixin, generic.DetailView):

    model = models.Event
    template_name = "events/event_detail.html"
    prefetch_related = ("members",)

# Single Event UpdateView

class UpdateEvent(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateForm
    model = models.Event
    template_name_suffix = '_update_form'


    def form_valid(self, form):
        response = super().form_valid(form)
        self.object = form.save(commit=False)
        geolocator = Nominatim()
        geolocator_location = geolocator.geocode(self.object.address)
        self.object.latitude = geolocator_location.latitude
        self.object.longitude = geolocator_location.longitude
        self.object.save()
        return response

# ListViews

class AllEvents(LoginRequiredMixin, generic.ListView):

    model = models.Event
    paginate_by = 8
    queryset = models.Event.objects.order_by('date')

class EventsNextTwoWeeks(generic.ListView):

    model = models.Event
    startdate = datetime.date.today()
    enddate = startdate + datetime.timedelta(weeks=2)
    queryset = models.Event.objects.filter(date__range=[startdate, enddate])
    template_name = "events/event_list_filtered.html"

class EventsNextFourWeeks(generic.ListView):

    model = models.Event
    startdate = datetime.date.today()
    enddate = startdate + datetime.timedelta(weeks=4)
    queryset = models.Event.objects.filter(date__range=[startdate, enddate])
    template_name = "events/event_list_filtered.html"

class LocationAmsterdam(generic.ListView):

    model = models.Event
    queryset = models.Event.objects.filter(address__icontains="Amsterdam")
    template_name = "events/event_list_filtered.html"

class LocationRotterdam(generic.ListView):

    model = models.Event
    queryset = models.Event.objects.filter(address__icontains="Rotterdam")
    template_name = "events/event_list_filtered.html"

class LocationDenHaag(generic.ListView):
    model = models.Event
    queryset = models.Event.objects.filter(address__icontains="Den Haag")
    template_name = "events/event_list_filtered.html"

class LocationUtrecht(generic.ListView):
    model = models.Event
    queryset = models.Event.objects.filter(address__icontains="Utrecht")
    template_name = "events/event_list_filtered.html"

class AllEventsByDate(generic.ListView):

    model = models.Event
    queryset = models.Event.objects.order_by('date')

# Event Actions

class JoinEvent(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        return reverse("events:single",
                       kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        event = get_object_or_404(models.Event,
                                      slug=self.kwargs.get("slug"))
        try:

            models.EventMember.objects.create(
                user=self.request.user,
                event=event,
            )

        except IntegrityError:

            messages.warning(
                self.request,
                "You are already a member of <b>{}</b>".format(event.name)
            )

        else:

            messages.success(
                self.request,
                "You're now a member of <b>{}</b>".format(event.name)
            )

        return super().get(request, *args, **kwargs)

class LeaveEvent(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        return reverse("events:single",
                       kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.EventMember.objects.filter(
                user=self.request.user,
                event__slug=self.kwargs.get("slug")
            ).get()

        except models.EventMember.DoesNotExist:

            messages.warning(
                self.request,
                "You can't leave this event."
            )

        else:

            membership.delete()
            messages.success(
                self.request,
                "You've left the event."
            )

        return super().get(request, *args, **kwargs)

class DeleteEvent(LoginRequiredMixin, generic.DeleteView):

    model = models.Event
    success_url = reverse_lazy('events:list')




from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import EventForm
from .models import Event, EventRSVP
from accounts.models import User
from django.db.models import Q

# Create your views here.


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/create.html"

    def form_valid(self, form):
        resp = super().form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        messages.success(self.request, message="Event creation successful")

        return resp

    def get_success_url(self) -> str:
        return reverse("events:user_created_events")


class EditEventView(LoginRequiredMixin, UpdateView):

    def get_success_url(self) -> str:
        return reverse("events:detail", args=[self.object.id])

    def get_queryset(self):
        return Event.objects.filter(active=True, owner=self.request.user)
    form_class = EventForm
    template_name = "events/edit.html"


class ListEventView(ListView):
    def get_queryset(self):
        return (Event.objects.filter(active=True)
                .prefetch_related(
                    Prefetch("eventrsvp_set",
                             EventRSVP.objects.filter(
                                 user_id=self.request.user.id)
                             )
        )
        )
    template_name = "events/list.html"


class SearchEventView(ListView):
    def get_queryset(self):
        search_term = self.request.GET.get('search_term', '')
        return (Event.objects.filter(active=True)
                .filter(
            Q(title__icontains=search_term)
            | Q(description__icontains=search_term)
            | Q(location__icontains=search_term))
            .prefetch_related(
                    Prefetch("eventrsvp_set",
                             EventRSVP.objects.filter(
                                 user_id=self.request.user.id)
                             )
        )
        )
    template_name = "events/list.html"


class DetailEventView(DetailView):
    def get_queryset(self):
        return (Event.objects.filter(active=True)
                .prefetch_related(
                    Prefetch("eventrsvp_set",
                             EventRSVP.objects.filter(
                                 user_id=self.request.user.id)
                             )
        )
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        event: Event = kwargs['object']
        data["other_attendees"] = User.objects.filter(
            eventrsvp__event_id=event.id)
        return data
    template_name = "events/detail.html"


class DeleteEventView(UpdateView):
    queryset = Event.objects.filter(active=True)
    template_name = "events/delete.html"

    success_url = reverse_lazy("events:list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.active = False
        self.object.save()
        messages.success(request, message="Event Deleted successfully")

        return HttpResponseRedirect(self.get_success_url())


class UserEventRSVPListView(LoginRequiredMixin, ListView):
    """
    Events a current user has rsvp'd for
    """

    def get_queryset(self):
        self.user = self.request.user
        return Event.objects.filter(active=True, eventrsvp__user_id=self.user.id)
    template_name = "events/list.html"


class UserEventListView(LoginRequiredMixin, ListView):
    """
    Events a current user has created
    """

    def get_queryset(self):
        self.user = self.request.user
        return Event.objects.filter(active=True, owner_id=self.user.id)
    template_name = "events/user_event_list.html"


class RSVPEventView(LoginRequiredMixin, TemplateView):
    def get(self, request, event_id, status, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        if status not in ["add", "remove"]:
            messages.error(request, message="Operation not allowed")

            return HttpResponseRedirect(reverse("events:user_list"), status=400)
        if status == 'add':
            EventRSVP.objects.create(
                user_id=self.request.user.id, event_id=event_id)
            messages.success(request, message="Event RSVP successful")
        if status == "remove":
            EventRSVP.objects.filter(
                user__id=self.request.user.id, event_id=event_id).delete()
            messages.success(request, message="Event RSVP removal successful")

        return HttpResponseRedirect(reverse("events:detail", args=[event_id]))

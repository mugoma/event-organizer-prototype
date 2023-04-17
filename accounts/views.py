from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from . import forms,models

# Create your views here.

class UserCreationView(FormView):
    form_class=forms.EventsUserCreationForm
    template_name="accounts/register.html"
    success_url=reverse_lazy("events:list")
from .models import Event
from django import forms

class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        exclude=['active', 'owner']
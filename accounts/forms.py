from django.contrib.auth.forms import UserCreationForm
from .models import User

class EventsUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=UserCreationForm.Meta.fields
from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView

from . import forms

# Create your views here.


class UserCreationView(FormView):
    form_class = forms.EventsUserCreationForm
    template_name = "accounts/register.html"

    def form_valid(self, form: forms.EventsUserCreationForm):
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        messages.success(self.request, "User registered Successfully.")
        return reverse("accounts:login")

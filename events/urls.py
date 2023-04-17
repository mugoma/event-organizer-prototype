"""minerva_event_organizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
app_name="events"
urlpatterns = [
    path("create/", views.CreateEventView.as_view(), name="create"),
    path("search/", views.SearchEventView.as_view(), name="search"),
    path("update/<pk>/", views.EditEventView.as_view(), name="update"),
    path("detail/<pk>/", views.DetailEventView.as_view(), name="detail"),
    path("delete/<pk>/", views.DeleteEventView.as_view(), name="delete"),
    path("my-events/", views.UserEventRSVPListView.as_view(), name="user_events"),
    path("my-events/created/", views.UserEventListView.as_view(), name="user_created_events"),
    path("list", views.ListEventView.as_view(), name="list"),
    path("rvsp/<event_id>/<status>/", views.RSVPEventView.as_view(), name="change_rsvp_status"),
]

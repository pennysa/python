# apps/personal/urls.py
from django.urls import path
from . import views

app_name = "personal"

urlpatterns = [
    path("", views.personal_calendar, name="personal_calendar"),
    path("events/", views.get_events, name="get_events"),
    path("add/", views.add_event, name="add_event"),
    path("update/<int:event_id>/", views.update_event, name="update_event"),
    path("delete/<int:event_id>/", views.delete_event, name="delete_event"),
    path("toggle/<int:event_id>/", views.toggle_complete, name="toggle_complete"),
]



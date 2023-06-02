from django.urls import path

from calendar_app.views import EventList

urlpatterns = [
    path("event/", EventList.as_view()),
]

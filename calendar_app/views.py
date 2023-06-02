from klym_telemetry.utils import klym_telemetry
from rest_framework import generics
from rest_framework import mixins

from calendar_app.analyzer import EventAnalyzer
from calendar_app.models import Event
from calendar_app.serializers import UserEventSerializer


class EventList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = UserEventSerializer

    def get(self, request, *args, **kwargs):
        klym_telemetry.up(name="EVENT_GET_COUNTER", description="A counter of get Event")
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        klym_telemetry.up(name="EVENT_POST_COUNTER", description="A counter of post Event")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        EventAnalyzer(event=instance)

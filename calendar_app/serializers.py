from rest_framework import serializers

from calendar_app.models import Event


class UserEventSerializer(serializers.ModelSerializer): # noqa
    class Meta:
        model = Event
        exclude = ('id', 'is_valid', 'addresses')

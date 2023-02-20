"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event


class EventView(ViewSet):
    """Level up Events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'name', 'date', 'location', 'game')
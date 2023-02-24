"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer


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


    def create(self, request):
        """Handle POST operations
        
        returns
            Response -- JSON serialized event instance
        """
        game = Game.objects.get(pk=request.data["game"])
        organizer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.create(
            name = request.data["name"],
            date = request.data["date"],
            location = request.data["location"],
            game = game,
            organizer = organizer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    

    def update(self, request, pk):
        """Handle PUT requests for an event 
        Returns:
            Response -- Empty body with 204 status code 
        """

        event = Event.objects.get(pk=pk)
        event.name = request.data["name"]
        event.date = request.data["date"]
        event.location = request.data["location"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        gamer = Gamer.objects.get(pk=request.data["organizer"])
        event.organizer = gamer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for an event 
        Returns:
            Response -- Empty body with 204 status code 
        """
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'name', 'date', 'location', 'game')

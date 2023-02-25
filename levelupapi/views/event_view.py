"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
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
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
        
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


    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
        #the gamer is the current user
        gamer = Gamer.objects.get(user=request.auth.user)
        #an event is specified by primary key
        event = Event.objects.get(pk=pk)
        #
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""
        #the gamer is the current user
        gamer = Gamer.objects.get(user=request.auth.user)
        #an event is specified by primary key
        event = Event.objects.get(pk=pk)

        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'name', 'date', 'location', 'game', 'joined')

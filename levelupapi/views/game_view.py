"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """

        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """

        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations
        
        returns
            Response -- JSON serialized game instance
        """
        game_type = GameType.objects.get(pk=request.data["game_type"])
        gamer = Gamer.objects.get(user=request.auth.user)

        game = Game.objects.create(
            name = request.data["name"],
            description = request.data["description"],
            game_type=game_type,
            gamer=gamer
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)


class GameGamerSerializer(serializers.ModelSerializer):
    """ to serialize the gamer in GamerSerializer """
    class Meta:
        model = Gamer
        fields = ('id', 'bio', 'user_id')

class GameTypeSerializer(serializers.ModelSerializer):
    """ to serialize the gamer in GamerSerializer """
    class Meta:
        model = GameType
        fields = ('id', 'type')

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    gamer = GameGamerSerializer(many=False)
    game_type = GameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'game_type', 'gamer')
        depth: 1

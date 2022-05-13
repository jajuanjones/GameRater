"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Game
from gameraterapi.models import Player
from gameraterapi.views.review import ReviewSerializer
from django.db.models import Q

class GameView(ViewSet):
    """Game rater game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        # create a query parameter to for orderby
        order_by = self.request.query_params.get('orderby', None)
        # create a query param to search
        search_text = self.request.query_params.get('q', None)
        games = Game.objects.all()
        # whenever our resources includes 'orderby' query param
        if order_by is not None:
            # use the order by function to sort the games
            games = Game.objects.all().order_by(f'{order_by}')
        else:
            # other wise return all the games
            # we run this second to make sure we can sort the games on page load
            games = Game.objects.all()
        # create a query param to check for a designer
        designer = request.query_params.get('designer', None)
        # this conditional will filter our games by designer names
        if designer is not None:
            games = games.filter(designer_id=designer)
        # whenever our resources include 'search_text' query param
        if search_text is not None:
            # filter the game titles, descripts, and/or designers that contain our text from param
            games = Game.objects.filter(
                Q(title__contains=search_text) |
                Q(description__contains=search_text) |
                Q(designer__contains=search_text)
            )
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST requests

        Returns:
            Response -- JSON serialized event
        """ 
        gamer = Player.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests

        Returns:
            Response --  204 status code
        """
        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Hande DELETE requests for an game
        
        Returns:
            Response -- 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    # since we have a related name on 'game' prop in review model we can reference it for our game view
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'designer', 'gamer', 'year_released', 
                  'number_of_players', 'time_to_play', 'age_recommendation', 'categories', 
                  'reviews', 'average_rating', 'images')
        depth =  1

class CreateGameSerializer(serializers.ModelSerializer):
    """JSON serializer to create game
    """
    class Meta:
        model = Game
        fields = ['id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'time_to_play', 'age_recommendation', 'categories']
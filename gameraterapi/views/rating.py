"""View module for handling requests about rating"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Rating
from gameraterapi.models import Game
from gameraterapi.models import Player

class RatingView(ViewSet):
    """Level up rating view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single rating

        Returns:
            Response -- JSON serialized rating
        """
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        """Handle GET requests to get all ratings

        Returns:
            Response -- JSON serialized list of ratings
        """
        ratings = Rating.objects.all()
        player = request.query_params.get('player', None)
        if player is not None:
            ratings = ratings.filter(player_id=player)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST requests

        Returns:
            Response -- JSON serialized event
        """ 
        player = Player.objects.get(user=request.auth.user)
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests

        Returns:
            Response --  204 status code
        """
        rating = Rating.objects.get(pk=pk)
        serializer = CreateRatingSerializer(rating, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Hande DELETE requests for an rating
        
        Returns:
            Response -- 204 status code
        """
        rating = Rating.objects.get(pk=pk)
        rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for ratings
    """
    class Meta:
        model = Rating
        fields = ('id', 'rating', 'player', 'game')
        depth =  1

class CreateRatingSerializer(serializers.ModelSerializer):
    """JSON serializer to create rating
    """
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'game']
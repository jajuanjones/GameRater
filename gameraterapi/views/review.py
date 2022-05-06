"""View module for handling requests about review"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Review
from gameraterapi.models import Game
from gameraterapi.models import Player

class ReviewView(ViewSet):
    """Level up review view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized review
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        """Handle GET requests to get all reviews

        Returns:
            Response -- JSON serialized list of reviews
        """
        reviews = Review.objects.all()
        player = request.query_params.get('player', None)
        if player is not None:
            reviews = reviews.filter(player_id=player)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST requests

        Returns:
            Response -- JSON serialized event
        """ 
        player = Player.objects.get(pk=request.data['player'])
        game = Game.objects.get(pk=request.data['game'])
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(player=player)
        serializer.save(game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests

        Returns:
            Response --  204 status code
        """
        review = Review.objects.get(pk=pk)
        serializer = CreateReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Hande DELETE requests for an review
        
        Returns:
            Response -- 204 status code
        """
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews
    """
    class Meta:
        model = Review
        fields = ('id', 'review', 'player', 'game')
        depth =  1

class CreateReviewSerializer(serializers.ModelSerializer):
    """JSON serializer to create review
    """
    class Meta:
        model = Review
        fields = ['id', 'review', 'player', 'game']
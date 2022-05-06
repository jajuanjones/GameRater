"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Player


class PlayerView(ViewSet):
    """Level up players view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single players

        Returns:
            Response -- JSON serialized players
        """
        try:
            player = Player.objects.get(pk=pk)
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all player

        Returns:
            Response -- JSON serialized list of player
        """
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    
class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for players
    """
    class Meta:
        model = Player
        fields = ('id', 'user', 'bio')
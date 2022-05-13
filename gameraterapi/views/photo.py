"""View module for handling requests about photo"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gameraterapi.models import Photo
from gameraterapi.models import Game
from gameraterapi.models import Player
from django.core.files.base import ContentFile
import base64
import uuid

class PhotoView(ViewSet):
    """Level up photo view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single photo

        Returns:
            Response -- JSON serialized photo
        """
        try:
            photo = Photo.objects.get(pk=pk)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        except Photo.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        """Handle GET requests to get all photos

        Returns:
            Response -- JSON serialized list of photos
        """
        photos = Photo.objects.all()
        player = request.query_params.get('player', None)
        if player is not None:
            photos = photos.filter(player_id=player)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST requests

        Returns:
            Response -- JSON serialized event
        """ 
        # Create a new instance of the game picture model you defined
        # Example: 
        game_picture = Photo()
        format, imgstr = request.data["image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["game"]}-{uuid.uuid4()}.{ext}')

        # Give the image property of your game picture instance a value
        # For example, if you named your property `action_pic`, then
        # you would specify the following code:
        #
        #       
        player = Player.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])
        game_picture.image = data
        game_picture.player = player
        game_picture.game = game
        # Save the data to the database with the save() method
        game_picture.save()
        serializer = PhotoSerializer(game_picture)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests

        Returns:
            Response --  204 status code
        """
        photo = Photo.objects.get(pk=pk)
        serializer = CreatePhotoSerializer(photo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Hande DELETE requests for an photo
        
        Returns:
            Response -- 204 status code
        """
        photo = Photo.objects.get(pk=pk)
        photo.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class PhotoSerializer(serializers.ModelSerializer):
    """JSON serializer for photos
    """
    class Meta:
        model = Photo
        fields = ('id', 'game', 'player', 'image')
        depth =  1

class CreatePhotoSerializer(serializers.ModelSerializer):
    """JSON serializer to create photo
    """
    class Meta:
        model = Photo
        fields = ['id', 'game', 'image']
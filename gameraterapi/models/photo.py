from django.db import models

class Photo(models.Model):
    """This class will initialize a photo model
    """
    image = models.ImageField()
    player_id = models.ForeignKey("Player", on_delete=models.CASCADE)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
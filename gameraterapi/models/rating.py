from django.db import models

class Rating(models.Model):
    """This class will initialize a rating model
    """
    rating = models.IntegerField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
from django.db import models

class Review(models.Model):
    """This class will initialize a review model
    """
    review = models.TextField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="reviews")
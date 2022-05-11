from audioop import avg
from django.db import models

class Game(models.Model):
    """This class will initalize a game model
    """
    title = models.CharField(default="Word", max_length=20)
    description = models.TextField()
    designer = models.TextField(max_length=30)
    gamer = models.ForeignKey("Player", on_delete=models.CASCADE)
    year_released = models.CharField(max_length=4)
    number_of_players = models.IntegerField()
    time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    categories = models.ManyToManyField("Category", related_name="categories")
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = self.ratings.all()

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
        # Calculate the averge and return it.
            avg_rating = total_rating / len(ratings)
            return avg_rating
        # If you don't know how to calculate averge, Google it.    

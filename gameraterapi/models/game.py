from django.db import models

class Game(models.Model):
    """This class will initalize a game model
    """
    description = models.TextField()
    designer = models.ForeignKey("Player", on_delete=models.CASCADE)
    year_released = models.CharField(max_length=4)
    number_of_players = models.IntegerField()
    time_to_play = models.CharField(max_length=10)
    age_recommendation = models.CharField(max_length=10)
    categories = models.ManyToManyField("Category", related_name="categories")

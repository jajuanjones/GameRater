from django.db import models

class Photo(models.Model):
    """This class will initialize a photo model
    """
    image = models.ImageField(upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="images")
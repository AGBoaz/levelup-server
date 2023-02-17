from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)

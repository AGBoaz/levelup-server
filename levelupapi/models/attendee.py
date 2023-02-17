from django.db import models

class Attendee(models.Model):
    gamer = models.ManyToManyField("Gamer")
    event = models.ForeignKey("Event", on_delete=models.CASCADE)

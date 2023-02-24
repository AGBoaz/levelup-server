from django.db import models

class Event(models.Model):
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="organizer_event")
    attendees = models.ManyToManyField("Gamer", through="Attendee")
    name = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    location = models. CharField(max_length=100)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    
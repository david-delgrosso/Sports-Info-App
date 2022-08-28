from django.db import models

class Game(models.Model):
    home_team = models.CharField(max_length=30)
    away_team = models.CharField(max_length=30)
    time = models.CharField(max_length=20)

    def __str__(self):
        return self.home_team + " vs " + self.away_team + " @ " + str(self.time)
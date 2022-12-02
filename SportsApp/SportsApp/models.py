from django.db import models

class Schedule(models.Model):
    home_team = models.CharField(max_length=30)
    away_team = models.CharField(max_length=30)
    time = models.TimeField()
    date = models.DateField()
    sport = models.CharField(max_length=10)

    def __str__(self):
        return self.home_team + " vs " + self.away_team + " @ " + str(self.time)
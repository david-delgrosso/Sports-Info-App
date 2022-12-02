from django.db import models

class NBASchedule(models.Model):
    home_team = models.CharField(max_length=30)
    home_city = models.CharField(max_length=30)
    away_team = models.CharField(max_length=30)
    away_city = models.CharField(max_length=30)
    time = models.TimeField('%H:%M')
    date = models.DateField()
    sport = models.CharField(max_length=10)

    def __str__(self):
        return self.home_team + " vs " + self.away_team + " @ " + str(self.time)
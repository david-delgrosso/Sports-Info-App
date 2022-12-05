from django.db import models

class NBATeam(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    sport = models.CharField(max_length=10)

    def __str__(self):
        return str(self.city) + ' ' + (self.name)

class NBASchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    home_team = models.ForeignKey(NBATeam, related_name="home_team", on_delete=models.CASCADE)
    away_team = models.ForeignKey(NBATeam, related_name="away_team", on_delete=models.CASCADE)
    time = models.TimeField('%H:%M')
    date = models.DateField()
    sport = models.CharField(max_length=10)

    def __str__(self):
        return str(self.home_team) + " vs " + str(self.away_team) + " @ " + str(self.time)
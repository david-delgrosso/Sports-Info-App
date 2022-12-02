from django.shortcuts import render, redirect
from .restapis import *
from .models import NBASchedule

def home(request):
    context = {}
    context['nba_games'] = get_todays_games('NBA')
    return render(request, 'SportsApp/index.html', context)

# NBA views
def clear_nba_schedule(request):
    context = {}
    NBASchedule.objects.all().delete()
    return render(request, 'SportsApp/index.html', context)

def populate_nba_db(request):
    context = {}
    nba_games = load_nba_schedule()
    context['info_message'] = "Successfully Loaded NBA Schedule to Database"
    return render(request, 'SportsApp/index.html', context)

"""
def scrape_games(request):
    url = 'https://www.espn.com/mlb/schedule'
    games = get_games(url)

    for game in games:
        game.save()

    context = {}
    context['words'] = "scrape complete"
    context['games'] = ""
    return render(request, 'SportsApp/index.html', context)

def load_mlb(request):
    context = {}
    context['games'] = Schedule.objects.all()
    return render(request, 'SportsApp/games.html', context)

def show_games(request):
    context = {}
    context['words'] = "scrape complete"
    context['games'] = Schedule.objects.all()
    return render(request, 'SportsApp/index.html', context)
"""
from django.shortcuts import render, redirect
from .restapis import *
from .models import Schedule

def home(request):
    context = {}
    context['words'] = "Gotta populate the database my guy"
    return render(request, 'SportsApp/index.html', context)

def clear_schedule(request):
    context = {}
    Schedule.objects.all().delete()
    return render(request, 'SportsApp/index.html', context)

def load_schedule(request):
    context = {}
    nba_games = load_nba_schedule()

    return render(request, 'SportsApp/index.html', context)

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
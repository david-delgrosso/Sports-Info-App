from django.shortcuts import render, redirect
from .restapis import *
from .models import NBASchedule
from .utils import *

# Load home page
def home(request):
    context = {}
    context['nba_games'] = get_todays_games('NBA')
    return render(request, 'SportsApp/index.html', context)

# NBA views
# Clear NBA Schedule database
def clear_nba_schedule(request):
    context = {}
    NBASchedule.objects.all().delete()
    context['info_message'] = "Successfully Cleared NBA Schedule Database"
    return render(request, 'SportsApp/index.html', context)

# Populate NBA Schedule database
def populate_nba_schedule_db(request):
    context = {}
    get_nba_schedule()
    context['info_message'] = "Successfully Loaded NBA Schedule to Database"
    return render(request, 'SportsApp/index.html', context)

# Clear NBA Teams database
def clear_nba_teams_db(request):
    context = {}
    NBATeam.objects.all().delete()
    context['info_message'] = "Successfully Cleared NBA Teams Database"
    return render(request, 'SportsApp/index.html', context)

# Populate NBA Teams database
def populate_nba_teams_db(request):
    context = {}
    load_nba_teams_to_db()
    context['info_message'] = "Successfully Loaded NBA Teams to Database"
    return render(request, 'SportsApp/index.html', context)


def load_nba_game(request,id):
    context = {}
    context['game'] = NBASchedule.objects.get(id=id)
    return render(request, 'SportsApp/game.html', context)
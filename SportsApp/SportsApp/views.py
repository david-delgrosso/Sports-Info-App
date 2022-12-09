from django.shortcuts import render, redirect
from .restapis import *
from .models import NBASchedule2022
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
    NBASchedule2022.objects.all().delete()
    context['info_message'] = "Successfully Cleared NBA Schedule Database"
    return render(request, 'SportsApp/index.html', context)

# Populate NBA Schedule database
def populate_nba_schedule_db(request):
    context = {}
    years = [2017, 2018, 2019, 2020, 2021, 2022]
    for year in years:
        get_nba_schedule(year)
    #get_nba_schedule(2022)
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

# Populate NBA team stats for each game that has already been played
def populate_nba_game_stats(request):
    context = {}
    backfill_nba_stats()
    context['info_message'] = "Successfully Back-filled NBA Stats to Database"
    return render(request, 'SportsApp/index.html', context)

# Calculate NBA team stats based on previous games played
def calculate_nba_team_stats(request):
    context = {}
    update_nba_team_stats()
    context['info_message'] = "Successfully Calculated NBA Team Stats"
    return render(request, 'SportsApp/index.html', context)

# Load page displaying info for a single NBA game
def load_nba_game(request,id):
    context = {}
    context['game'] = NBASchedule2022.objects.get(id=id)
    return render(request, 'SportsApp/game.html', context)

# Load page displaying 
def load_nba_home(request):
    context = {}
    context['nba_games'] = get_todays_games('NBA')
    return render(request, 'SportsApp/nba_home.html', context)
from django.shortcuts import render, redirect
from .restapis import *
from .models import NBASchedule2022
from .utils import *
from .constants import *
from django.views import generic
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms

class DateForm(forms.Form):
    date = forms.DateField(label='',
                           widget=forms.DateInput(attrs={'class': "form-control",
                                                         'id': "date",
                                                         'type': "date"}))

# Load home page
def home(request):
    context = {}
    today = datetime.now() - timedelta(hours=5)
    context['nba_games'] = get_nba_games('NBA', today)
    return render(request, 'SportsApp/index.html', context)

# NBA views
# Clear NBA Schedule database
def clear_nba_schedule(request):
    context = {}
    clear_nba_schedule_db(NBA_SEASON)
    context['info_message'] = "Successfully Cleared NBA Schedule Database"
    return render(request, 'SportsApp/index.html', context)

# Populate NBA Schedule database
def populate_nba_schedule_db(request):
    context = {}
    get_nba_schedule(NBA_SEASON)
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
    backfill_nba_boxscores(NBA_SEASON)
    context['info_message'] = "Successfully Back-filled NBA Stats to Database"
    return render(request, 'SportsApp/index.html', context)

# Calculate NBA team stats based on previous games played
def calculate_nba_team_stats(request):
    context = {}
    update_nba_team_stats(NBA_SEASON)
    context['info_message'] = "Successfully Calculated NBA Team Stats"
    return render(request, 'SportsApp/index.html', context)

def copy_nba_stats_to_csv(request):
    context = {}
    export_nba_stats_to_csv([2017,2018,2019,2020,2021])
    context['info_message'] = "Successfully Copied NBA Stats to CSV"
    return render(request, 'SportsApp/index.html', context)

# Load page displaying info for a single NBA game
def load_nba_game(request,id):
    context = {}
    game = NBASchedule2022.objects.get(id=id)
    context['game'] = game
    context['preds'] = get_nba_game_predictions(game)
    return render(request, 'SportsApp/nba_game.html', context)

# Load page displaying 
def load_nba_home(request):
    context = {}
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['date']
    else:
        today = datetime.now() - timedelta(hours=5)
        day = str(today.strftime("%Y-%m-%d"))
        form = DateForm(initial={'date':day})

    context['day'] = day
    context['nba_games'] = get_nba_games('NBA', day)
    context['form'] = form
    context['in_past'] = False
    for game in context['nba_games']:
        if game.played:
            context['in_past'] = True
    return render(request, 'SportsApp/nba_home.html', context)

def rename_nba_logos(request):
    context = {}
    rename_nba_logos_util()
    context['info_message'] = "Successfully Copied NBA Stats to CSV"
    return render(request, 'SportsApp/index.html', context)
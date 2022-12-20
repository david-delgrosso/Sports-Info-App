from django.shortcuts import render, redirect
from SportsApp.restapis import *
from SportsApp.models import NBASchedule2022
from SportsApp.utils import *
from SportsApp.constants import *
from django.views import generic
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms
from SportsApp.NBA import NBA
from datetime import datetime, timedelta

# Class for form used to select a date
class DateForm(forms.Form):
    date = forms.DateField(label='',
                           widget=forms.DateInput(attrs={'class': "form-control",
                                                         'id': "date",
                                                         'type': "date"}),
                           required=True)

# Class for form used to generate a game prediction
class PredictionForm(forms.Form):
    model     = forms.ChoiceField(choices=NBA_MODELS_TUPLE, label='Model', required=True, widget=forms.Select(attrs={'class': "form-select"}))
    home_team = forms.ChoiceField(choices=NBA_TEAMS_TUPLE, label='Home Team', required=True, widget=forms.Select(attrs={'class': "form-select"}))
    away_team = forms.ChoiceField(choices=NBA_TEAMS_TUPLE, label='Away Team', required=True, widget=forms.Select(attrs={'class': "form-select"}))

# Load home page
def home_view(request):
    context = {}
    
    # Get today's date
    today = datetime.now() - timedelta(hours=5)

    # Create sport objects at current year
    nba = NBA(NBA_SEASON)

    # Save games to context dictionary
    context['nba_games'] = nba.get_games(today)

    return render(request, 'SportsApp/index.html', context)

# Load NBA home page
def nba_home_view(request):
    context = {}

    # Create NBA object at current year
    nba = NBA(NBA_SEASON)

    if request.method == 'POST':
        # Check for date submit
        if "date_submit" in request.POST:
            # Process date form
            date_form = DateForm(request.POST)
            if date_form.is_valid():
                day = date_form.cleaned_data['date']
            
            # Initialize prediction form
            pred_form = PredictionForm(initial={'model':'1',
                                                'away_team':'2',
                                                'home_team':'14'})
            context['pred_home_score'], context['pred_away_score'] = 0.0, 0.0

        # Check for prediction submit
        elif "pred_submit" in request.POST:
            # Process prediction form
            pred_form = PredictionForm(request.POST)
            if pred_form.is_valid():
                home_team = NBA_TEAMS_TUPLE[int(pred_form.cleaned_data['home_team']) - 1][1]
                away_team = NBA_TEAMS_TUPLE[int(pred_form.cleaned_data['away_team']) - 1][1]
                model = NBA_MODELS_TUPLE[int(pred_form.cleaned_data['model']) - 1][1]
                print(home_team, away_team, model)
                context['pred_home_score'], context['pred_away_score'] = nba.predict_single_game(model, home_team, away_team)

            # Initialize date form
            today = datetime.now() - timedelta(hours=5)
            day = str(today.strftime("%Y-%m-%d"))
            date_form = DateForm(initial={'date':day})
    else:  # Use today
        # Initialize date form
        today = datetime.now() - timedelta(hours=5)
        day = str(today.strftime("%Y-%m-%d"))
        date_form = DateForm(initial={'date':day})

        # Initialize prediction form
        pred_form = PredictionForm(initial={'model':'1',
                                            'away_team':'2',
                                            'home_team':'14'})
        context['pred_home_score'], context['pred_away_score'] = 0.0, 0.0

    # Populate context dictionary
    context['day'] = day
    context['nba_games'] = nba.get_games(day)
    context['date_form'] = date_form
    context['pred_form'] = pred_form
    context['in_past'] = True

    # If any game hasn't been played yet, set in_past to False
    for game in context['nba_games']:
        if not game.boxscore_filled:
            context['in_past'] = False
        
    return render(request, 'SportsApp/nba_home.html', context)

# Load NBA game page
def nba_game_view(request,id):
    context = {}

    # Create NBA object at current year
    nba = NBA(NBA_SEASON)

    # Save game data to context dictionary
    context['game']  = nba.sch_obj.objects.get(id=id)
    context['preds'] = nba.pred_obj.objects.get(id=id)

    return render(request, 'SportsApp/nba_game.html', context)

def nba_model_view(request,model_name):
    context = {}
    url = "SportsApp/" + str(model_name) + ".html"

    today = datetime.now() - timedelta(hours=5)
    day = str(today.strftime("%Y-%m-%d"))

    # Create NBA object at current year
    nba = NBA(NBA_SEASON)

    # Get NBA games on current day
    context['nba_games'] = nba.get_games(day)
    context['preds'] = []
    for i,game in enumerate(context['nba_games']):
        context['preds'].append(nba.pred_obj.objects.get(id=game))

    context['games_and_preds'] = zip(context['nba_games'], context['preds'])

    return render(request, url, context)
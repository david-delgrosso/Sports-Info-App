from django.shortcuts import render, redirect
from .restapis import *
from .models import NBASchedule
from .utils import *

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
    get_nba_schedule()
    context['info_message'] = "Successfully Loaded NBA Schedule to Database"
    return render(request, 'SportsApp/index.html', context)
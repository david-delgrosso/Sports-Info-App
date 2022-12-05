from datetime import *
import os
from .models import *
from .constants import *
from .restapis import *
import json

# general utilities
def convert_time(time_in):
    pass

def convert_date(date_in):
    pass

def get_todays_games(sport):
    today = str(datetime.now().strftime("%Y-%m-%d"))
    games = NBASchedule.objects.filter(sport=sport, date=today)
    return games

# NBA utilities
def load_nba_schedule_to_db():
    f = open('nba_season_2022.json')
    data = json.load(f)

    for game in data['response']:
        date_str = game['date']['start'][:-5].replace('T',' ')
        game_datetime = datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
        game_date = game_datetime.date()
        game_time = game_datetime.time()

        home_team_name = game['teams']['home']['nickname']
        try:
            home_team = NBATeam.objects.get(name=home_team_name)
        except:
            print(str(home_team_name) + " was not recognized as an NBA team. The game was not added to the schedule.")
            continue
    
        away_team_name = game['teams']['visitors']['nickname']
        try:
            away_team = NBATeam.objects.get(name=away_team_name)
        except:
            print(str(away_team_name) + " was not recognized as an NBA team. The game was not added to the schedule.")
            continue

        sch_obj = NBASchedule.objects.create(id=game['id'],
                                             sport="NBA",
                                             date=game_date,
                                             home_team=home_team,
                                             away_team=away_team,
                                             time=game_time)
        
def get_nba_schedule():
    #request_nba_schedule_to_json()
    load_nba_schedule_to_db()

def load_nba_teams_to_db():
    for k,v in NBA_TEAMS_DICT.items():
        team_obj = NBATeam.objects.create(name=k,
                                          city=v,
                                          sport="NBA")
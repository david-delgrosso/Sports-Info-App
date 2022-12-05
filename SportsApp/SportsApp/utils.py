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

        if game_datetime < NBA_SEASON_START_DATE_2022:
            continue

        home_team_id = game['teams']['home']['id']
        try:
            home_team = NBATeam.objects.get(id=home_team_id)
        except:
            print(str(game['teams']['home']['name']) + " was not recognized as an NBA team. The game was not added to the schedule.")
            continue
    
        away_team_id = game['teams']['visitors']['id']
        try:
            away_team = NBATeam.objects.get(id=away_team_id)
        except:
            print(str(game['teams']['visitors']['name']) + " was not recognized as an NBA team. The game was not added to the schedule.")
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
        team_obj = NBATeam.objects.create(id=NBA_API_ID_DICT[k],
                                          name=k,
                                          city=v,
                                          sport="NBA")
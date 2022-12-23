# import sys
 
# # setting path
# sys.path.append('../SportsApp')

from SportsApp.models import NBATeam
from SportsApp.constants import *
from SportsApp.NBA import NBA
import pickle
import pandas as pd
import os
import shutil
#temp
from SportsApp.config import ODDS_API_HEADERS
import requests as re
import json

# NBA Utilities
# Clear NBA Schedule database
def clear_nba_schedule_util():
    nba = NBA(NBA_SEASON)
    nba.clear_schedule()
    print(str(nba), " has cleared its schedule...")

# Populate NBA Schedule database
def load_nba_schedule_util():
    nba = NBA(NBA_SEASON)
    nba.load_schedule()
    print(str(nba), " has successfully loaded schedule to database...")

# Clear NBA Teams database
def clear_nba_teams_util():
    NBATeam.objects.all().delete()
    print("Successfully cleared NBA teams database...")

# Populate NBA Teams database
def load_nba_teams_util():
    nba = NBA(NBA_SEASON)
    nba.load_teams()
    print(str(nba), " has successfully loaded teams to database...")

# Populate NBA team stats for each game that has already been played
def download_nba_game_stats_util():
    nba = NBA(NBA_SEASON)
    nba.download_game_stats()
    print(str(nba), " has successfully loaded game stats to schedule...")

# Calculate NBA team stats based on previous games played
# Recalculate rankings based on updated stats
def calculate_nba_team_stats_util():
    nba = NBA(NBA_SEASON)
    nba.calculate_team_stats()
    nba.set_rankings()
    print(str(nba), " has successfully calculated team stats...")

def copy_nba_stats_to_csv_util():
    years = [2017,2018,2019,2020,2021]
    nba = NBA(NBA_SEASON)
    nba.export_team_stats(years)
    print(str(nba), " has successfully copied data to csv")

def rename_nba_logos_util():
    logos_path = "SportsApp/static/media/nba_logos/"
    logos = os.listdir(logos_path)
    for logo in logos:
        if logo[0].islower():
            logo_sp = logo.split('-')
            if len(logo_sp) == 4:
                target = logos_path
                target += str(logo_sp[0]).capitalize() + '_'
                target += str(logo_sp[1]).capitalize() + '_'
                target += "Logo.png"
            elif len(logo_sp) == 5:
                target = logos_path
                target += str(logo_sp[0]).capitalize() + '_'
                target += str(logo_sp[1]).capitalize() + '_'
                target += str(logo_sp[2]).capitalize() + '_'
                target += "Logo.png"
            source = logos_path + logo
            print("Source: ", source)
            print("Target: ", target)
            shutil.copy(source, target)

def calculate_predictions_util():
    nba = NBA(NBA_SEASON)
    nba.clear_predictions()
    nba.calculate_predictions()
    nba.calculate_pred_error()
    print(str(nba), " has successfully calculated model predictions and error...")

def generate_error_plots_util():
    nba = NBA(NBA_SEASON)
    nba.models['Linear Regression'].plot_rmse()
    nba.models['Linear Regression'].plot_me()
    print(str(nba), " has successfully generated error plots...")

def request_nba_game_odds():
    sport = "basketball_nba"
    api_key = ODDS_API_HEADERS['API_KEY']
    regions = "us"
    markets = "spreads,totals"
    date = "2022-10-18T00:00:00Z"
    oddsFormat = "american"
    bookmakers = "fanduel"
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds-history/?apiKey={api_key}&regions={regions}&markets={markets}&oddsFormat={oddsFormat}&bookmakers={bookmakers}&date={date}"
    
    response = re.get(url)
    re_json = response.json()
    json_object = json.dumps(re_json, indent=4)

    filename = "odds_api_test.json"
    with open(filename,'w') as f:
        f.write(json_object)

def test_odds_api_util():
    request_nba_game_odds()

def download_game_odds_util():
    nba = NBA(NBA_SEASON)
    nba.download_game_odds()
    print(str(nba), " has successfully loaded game odds to schedule...")

import datetime
import csv
from .models import *
from .constants import *
import json
from .restapis import *
import time
import pickle
from sklearn import linear_model
import pandas as pd

# general utilities
def convert_time(time_in):
    pass

def convert_date(date_in):
    pass

# return table object of specific year
def get_schedule_db(year):
    if year == 2022:
        sch_obj = NBASchedule2022
    elif year == 2021:
        sch_obj = NBASchedule2021
    elif year == 2020:
        sch_obj = NBASchedule2020
    elif year == 2019:
        sch_obj = NBASchedule2019
    elif year == 2018:
        sch_obj = NBASchedule2018
    elif year == 2017:
        sch_obj = NBASchedule2017
    return sch_obj

# Returns a list of today's game objects
def get_nba_games(sport, day):
    games = NBASchedule2022.objects.filter(sport=sport, date=day)
    return games

def reset_nba_team_fields():
    teams = NBATeam.objects.all()
    for team in teams:
        team.games       = 0
        team.wins        = 0
        team.losses      = 0
        team.win_pct     = 0.0
        team.opp_wins    = 0
        team.opp_losses  = 0
        team.opp_win_pct = 0.0

        team.points_pg    = 0.0
        team.fgm_pg       = 0.0
        team.fga_pg       = 0.0
        team.fgp          = 0.0
        team.ftm_pg       = 0.0
        team.fta_pg       = 0.0
        team.ftp          = 0.0
        team.tpm_pg       = 0.0
        team.tpa_pg       = 0.0
        team.tpp          = 0.0
        team.offReb_pg    = 0.0
        team.defReb_pg    = 0.0
        team.totReb_pg    = 0.0
        team.assists_pg   = 0.0
        team.pFouls_pg    = 0.0
        team.steals_pg    = 0.0
        team.turnovers_pg = 0.0
        team.blocks_pg    = 0.0
        team.plusMinus_pg = 0.0

        team.opp_points_pg    = 0.0
        team.opp_fgm_pg       = 0.0
        team.opp_fga_pg       = 0.0
        team.opp_fgp          = 0.0
        team.opp_ftm_pg       = 0.0
        team.opp_fta_pg       = 0.0
        team.opp_ftp          = 0.0
        team.opp_tpm_pg       = 0.0
        team.opp_tpa_pg       = 0.0
        team.opp_tpp          = 0.0
        team.opp_offReb_pg    = 0.0
        team.opp_defReb_pg    = 0.0
        team.opp_totReb_pg    = 0.0
        team.opp_assists_pg   = 0.0
        team.opp_pFouls_pg    = 0.0
        team.opp_steals_pg    = 0.0
        team.opp_turnovers_pg = 0.0
        team.opp_blocks_pg    = 0.0
        team.opp_plusMinus_pg = 0.0

        team.save()

# NBA utilities
def clear_nba_schedule_db(year):
    sch_obj = get_schedule_db(year)
    sch_obj.objects.all().delete()

# Populate NBA Schedule database from json file
def load_nba_schedule_to_db(year):

    # Load json data
    filename = "nba_season_" + str(year) + ".json"
    f = open(filename)
    data = json.load(f)

    # Iterate over games
    for game in data['response']:

        # Determine game start time
        date_str = str(game['date']['start'])
        if len(date_str) > 10:
            date_str = date_str[:-5].replace('T',' ')
            game_datetime = datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
            game_date = game_datetime.date()
            game_time = game_datetime.time()
        elif len(date_str) == 10:
            if year == 2022:
                raise Exception("Current schedule date needs a time")
            else:
                game_datetime = datetime.strptime(date_str,'%Y-%m-%d')
                game_date = game_datetime.date()
                game_time = game_datetime.time()

        # Ignore preseason games
        if game_datetime < NBA_SEASON_START_DATE_DICT[str(year)]:
            continue

        # Find home and away team objects
        # Ignore non NBA teams
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

        # Add game to schedule database
        if year == 2022:
            sch_obj = NBASchedule2022.objects.create(id=game['id'],
                                                     sport="NBA",
                                                     date=game_date,
                                                     home_team=home_team,
                                                     away_team=away_team,
                                                     time=game_time)
        elif year == 2021:
            sch_obj = NBASchedule2021.objects.create(id=game['id'],
                                                     sport="NBA",
                                                     date=game_date,
                                                     home_team=home_team,
                                                     away_team=away_team,
                                                     time=game_time)
        elif year == 2020:
            sch_obj = NBASchedule2020.objects.create(id=game['id'],
                                                     sport="NBA",
                                                     date=game_date,
                                                     home_team=home_team,
                                                     away_team=away_team,
                                                     time=game_time)
        elif year == 2019:
            sch_obj = NBASchedule2019.objects.create(id=game['id'],
                                                     sport="NBA",
                                                     date=game_date,
                                                     home_team=home_team,
                                                     away_team=away_team,
                                                     time=game_time)
        elif year == 2018:
            sch_obj = NBASchedule2018.objects.create(id=game['id'],
                                                     sport="NBA",
                                                     date=game_date,
                                                     home_team=home_team,
                                                     away_team=away_team,
                                                     time=game_time)
        elif year == 2017:
            sch_obj = NBASchedule2017.objects.create(id=game['id'],
                                                     sport="NBA",
                                                     date=game_date,
                                                     home_team=home_team,
                                                     away_team=away_team,
                                                     time=game_time)
        
# Parent function for generating NBA Schedule database        
def get_nba_schedule(year):
    sch_obj = get_schedule_db(year)
    sch_obj.objects.all().delete()

    #request_nba_schedule_to_json(year)
    load_nba_schedule_to_db(year)

# Load NBA Teams dictionary into NBA Teams database
def load_nba_teams_to_db():
    for k,v in NBA_TEAMS_DICT.items():
        team_obj = NBATeam.objects.create(id=NBA_API_ID_DICT[k],
                                          name=k,
                                          city=v,
                                          sport="NBA")

def backfill_nba_boxscores(year):
    sch_obj = get_schedule_db(year)
    games = sch_obj.objects.all()
    
    i = 0
    for game in games:
        
        # Ignore games that already have stats filled
        if game.home_points is not None:
            continue

        i += 1

        # Request game stats
        game_stats_str = request_nba_game_stats(str(game.id))
        game_stats_json = json.loads(game_stats_str)

        # Break if game has not been played yet, otherwise wait 60s and submit request again
        try:
            if len(game_stats_json['response']) == 0:
                continue
        except:
            print("Waiting 60 seconds...")
            time.sleep(60)
            game_stats_str = request_nba_game_stats(str(game.id))
            game_stats_json = json.loads(game_stats_str)

        # Maximum iterations fail check
        if i > 1500:
            break
        
        if year == 2022:
            # Save home team stats
            game.home_points    = game_stats_json['response'][0]['statistics'][0]['points']
            game.home_fgm       = game_stats_json['response'][0]['statistics'][0]['fgm']
            game.home_fga       = game_stats_json['response'][0]['statistics'][0]['fga']
            game.home_fgp       = game_stats_json['response'][0]['statistics'][0]['fgp']
            game.home_ftm       = game_stats_json['response'][0]['statistics'][0]['ftm']
            game.home_fta       = game_stats_json['response'][0]['statistics'][0]['fta']
            game.home_ftp       = game_stats_json['response'][0]['statistics'][0]['ftp']
            game.home_tpm       = game_stats_json['response'][0]['statistics'][0]['tpm']
            game.home_tpa       = game_stats_json['response'][0]['statistics'][0]['tpa']
            game.home_tpp       = game_stats_json['response'][0]['statistics'][0]['tpp']
            game.home_offReb    = game_stats_json['response'][0]['statistics'][0]['offReb']
            game.home_defReb    = game_stats_json['response'][0]['statistics'][0]['defReb']
            game.home_totReb    = game_stats_json['response'][0]['statistics'][0]['totReb']
            game.home_assists   = game_stats_json['response'][0]['statistics'][0]['assists']
            game.home_pFouls    = game_stats_json['response'][0]['statistics'][0]['pFouls']
            game.home_steals    = game_stats_json['response'][0]['statistics'][0]['steals']
            game.home_turnovers = game_stats_json['response'][0]['statistics'][0]['turnovers']
            game.home_blocks    = game_stats_json['response'][0]['statistics'][0]['blocks']
            game.home_plusMinus = game_stats_json['response'][0]['statistics'][0]['plusMinus']
            
            # Save away stats
            game.away_points    = game_stats_json['response'][1]['statistics'][0]['points']
            game.away_fgm       = game_stats_json['response'][1]['statistics'][0]['fgm']
            game.away_fga       = game_stats_json['response'][1]['statistics'][0]['fga']
            game.away_fgp       = game_stats_json['response'][1]['statistics'][0]['fgp']
            game.away_ftm       = game_stats_json['response'][1]['statistics'][0]['ftm']
            game.away_fta       = game_stats_json['response'][1]['statistics'][0]['fta']
            game.away_ftp       = game_stats_json['response'][1]['statistics'][0]['ftp']
            game.away_tpm       = game_stats_json['response'][1]['statistics'][0]['tpm']
            game.away_tpa       = game_stats_json['response'][1]['statistics'][0]['tpa']
            game.away_tpp       = game_stats_json['response'][1]['statistics'][0]['tpp']
            game.away_offReb    = game_stats_json['response'][1]['statistics'][0]['offReb']
            game.away_defReb    = game_stats_json['response'][1]['statistics'][0]['defReb']
            game.away_totReb    = game_stats_json['response'][1]['statistics'][0]['totReb']
            game.away_assists   = game_stats_json['response'][1]['statistics'][0]['assists']
            game.away_pFouls    = game_stats_json['response'][1]['statistics'][0]['pFouls']
            game.away_steals    = game_stats_json['response'][1]['statistics'][0]['steals']
            game.away_turnovers = game_stats_json['response'][1]['statistics'][0]['turnovers']
            game.away_blocks    = game_stats_json['response'][1]['statistics'][0]['blocks']
            game.away_plusMinus = game_stats_json['response'][1]['statistics'][0]['plusMinus']
        else:
            # Save away team stats
            game.away_points    = game_stats_json['response'][0]['statistics'][0]['points']
            game.away_fgm       = game_stats_json['response'][0]['statistics'][0]['fgm']
            game.away_fga       = game_stats_json['response'][0]['statistics'][0]['fga']
            game.away_fgp       = game_stats_json['response'][0]['statistics'][0]['fgp']
            game.away_ftm       = game_stats_json['response'][0]['statistics'][0]['ftm']
            game.away_fta       = game_stats_json['response'][0]['statistics'][0]['fta']
            game.away_ftp       = game_stats_json['response'][0]['statistics'][0]['ftp']
            game.away_tpm       = game_stats_json['response'][0]['statistics'][0]['tpm']
            game.away_tpa       = game_stats_json['response'][0]['statistics'][0]['tpa']
            game.away_tpp       = game_stats_json['response'][0]['statistics'][0]['tpp']
            game.away_offReb    = game_stats_json['response'][0]['statistics'][0]['offReb']
            game.away_defReb    = game_stats_json['response'][0]['statistics'][0]['defReb']
            game.away_totReb    = game_stats_json['response'][0]['statistics'][0]['totReb']
            game.away_assists   = game_stats_json['response'][0]['statistics'][0]['assists']
            game.away_pFouls    = game_stats_json['response'][0]['statistics'][0]['pFouls']
            game.away_steals    = game_stats_json['response'][0]['statistics'][0]['steals']
            game.away_turnovers = game_stats_json['response'][0]['statistics'][0]['turnovers']
            game.away_blocks    = game_stats_json['response'][0]['statistics'][0]['blocks']
            game.away_plusMinus = game_stats_json['response'][0]['statistics'][0]['plusMinus']
            
            # Save home stats
            game.home_points    = game_stats_json['response'][1]['statistics'][0]['points']
            game.home_fgm       = game_stats_json['response'][1]['statistics'][0]['fgm']
            game.home_fga       = game_stats_json['response'][1]['statistics'][0]['fga']
            game.home_fgp       = game_stats_json['response'][1]['statistics'][0]['fgp']
            game.home_ftm       = game_stats_json['response'][1]['statistics'][0]['ftm']
            game.home_fta       = game_stats_json['response'][1]['statistics'][0]['fta']
            game.home_ftp       = game_stats_json['response'][1]['statistics'][0]['ftp']
            game.home_tpm       = game_stats_json['response'][1]['statistics'][0]['tpm']
            game.home_tpa       = game_stats_json['response'][1]['statistics'][0]['tpa']
            game.home_tpp       = game_stats_json['response'][1]['statistics'][0]['tpp']
            game.home_offReb    = game_stats_json['response'][1]['statistics'][0]['offReb']
            game.home_defReb    = game_stats_json['response'][1]['statistics'][0]['defReb']
            game.home_totReb    = game_stats_json['response'][1]['statistics'][0]['totReb']
            game.home_assists   = game_stats_json['response'][1]['statistics'][0]['assists']
            game.home_pFouls    = game_stats_json['response'][1]['statistics'][0]['pFouls']
            game.home_steals    = game_stats_json['response'][1]['statistics'][0]['steals']
            game.home_turnovers = game_stats_json['response'][1]['statistics'][0]['turnovers']
            game.home_blocks    = game_stats_json['response'][1]['statistics'][0]['blocks']
            game.home_plusMinus = game_stats_json['response'][1]['statistics'][0]['plusMinus']
        
        # Set game played flag
        game.played = True
        
        # Update table fields to reflect statistics
        game.save(update_fields=['home_points','home_fgm','home_fga','home_fgp','home_ftm',
                                'home_fta','home_ftp','home_tpm','home_tpa','home_tpp',
                                'home_offReb','home_defReb','home_totReb','home_assists',
                                'home_pFouls','home_steals','home_turnovers','home_blocks',
                                'home_plusMinus',
                                'away_points','away_fgm','away_fga','away_fgp','away_ftm',
                                'away_fta','away_ftp','away_tpm','away_tpa','away_tpp',
                                'away_offReb','away_defReb','away_totReb','away_assists',
                                'away_pFouls','away_steals','away_turnovers','away_blocks',
                                'away_plusMinus','played'])

        print("Game " + str(i) + " recorded...")
        time.sleep(0.5)

# Parse NBA Schedule database to calculate aggregate team stats
def update_nba_team_stats(year):
    #reset_nba_team_fields()
    #nba_game_by_game_calcs(year)
    nba_rankings()

def nba_game_by_game_calcs(year):

    sch_obj = get_schedule_db(year)
    games = sch_obj.objects.all()

    for game in games:

        home_team = game.home_team
        away_team = game.away_team

        if ( ( home_team.games == 0 ) or ( away_team.games == 0 ) ):
            game.first_game = True

        game.home_games       = home_team.games
        game.home_wins        = home_team.wins
        game.home_losses      = home_team.losses
        game.home_win_pct     = home_team.win_pct
        game.home_opp_wins    = home_team.opp_wins
        game.home_opp_losses  = home_team.opp_losses
        game.home_opp_win_pct = home_team.opp_win_pct

        game.home_points_pg    = home_team.points_pg
        game.home_fgm_pg       = home_team.fgm_pg
        game.home_fga_pg       = home_team.fga_pg
        game.home_fgp          = home_team.fgp
        game.home_ftm_pg       = home_team.ftm_pg
        game.home_fta_pg       = home_team.fta_pg
        game.home_ftp          = home_team.ftp
        game.home_tpm_pg       = home_team.tpm_pg
        game.home_tpa_pg       = home_team.tpa_pg
        game.home_tpp          = home_team.tpp
        game.home_offReb_pg    = home_team.offReb_pg
        game.home_defReb_pg    = home_team.defReb_pg
        game.home_totReb_pg    = home_team.totReb_pg
        game.home_assists_pg   = home_team.assists_pg
        game.home_pFouls_pg    = home_team.pFouls_pg
        game.home_steals_pg    = home_team.steals_pg
        game.home_turnovers_pg = home_team.turnovers_pg
        game.home_blocks_pg    = home_team.blocks_pg
        game.home_plusMinus_pg = home_team.plusMinus_pg

        game.home_opp_points_pg    = home_team.opp_points_pg
        game.home_opp_fgm_pg       = home_team.opp_fgm_pg
        game.home_opp_fga_pg       = home_team.opp_fga_pg
        game.home_opp_fgp          = home_team.opp_fgp
        game.home_opp_ftm_pg       = home_team.opp_ftm_pg
        game.home_opp_fta_pg       = home_team.opp_fta_pg
        game.home_opp_ftp          = home_team.opp_ftp
        game.home_opp_tpm_pg       = home_team.opp_tpm_pg
        game.home_opp_tpa_pg       = home_team.opp_tpa_pg
        game.home_opp_tpp          = home_team.opp_tpp
        game.home_opp_offReb_pg    = home_team.opp_offReb_pg
        game.home_opp_defReb_pg    = home_team.opp_defReb_pg
        game.home_opp_totReb_pg    = home_team.opp_totReb_pg
        game.home_opp_assists_pg   = home_team.opp_assists_pg
        game.home_opp_pFouls_pg    = home_team.opp_pFouls_pg
        game.home_opp_steals_pg    = home_team.opp_steals_pg
        game.home_opp_turnovers_pg = home_team.opp_turnovers_pg
        game.home_opp_blocks_pg    = home_team.opp_blocks_pg
        game.home_opp_plusMinus_pg = home_team.opp_plusMinus_pg

        game.away_games       = away_team.games
        game.away_wins        = away_team.wins
        game.away_losses      = away_team.losses
        game.away_win_pct     = away_team.win_pct
        game.away_opp_wins    = away_team.opp_wins
        game.away_opp_losses  = away_team.opp_losses
        game.away_opp_win_pct = away_team.opp_win_pct

        game.away_points_pg    = away_team.points_pg
        game.away_fgm_pg       = away_team.fgm_pg
        game.away_fga_pg       = away_team.fga_pg
        game.away_fgp          = away_team.fgp
        game.away_ftm_pg       = away_team.ftm_pg
        game.away_fta_pg       = away_team.fta_pg
        game.away_ftp          = away_team.ftp
        game.away_tpm_pg       = away_team.tpm_pg
        game.away_tpa_pg       = away_team.tpa_pg
        game.away_tpp          = away_team.tpp
        game.away_offReb_pg    = away_team.offReb_pg
        game.away_defReb_pg    = away_team.defReb_pg
        game.away_totReb_pg    = away_team.totReb_pg
        game.away_assists_pg   = away_team.assists_pg
        game.away_pFouls_pg    = away_team.pFouls_pg
        game.away_steals_pg    = away_team.steals_pg
        game.away_turnovers_pg = away_team.turnovers_pg
        game.away_blocks_pg    = away_team.blocks_pg
        game.away_plusMinus_pg = away_team.plusMinus_pg

        game.away_opp_points_pg    = away_team.opp_points_pg
        game.away_opp_fgm_pg       = away_team.opp_fgm_pg
        game.away_opp_fga_pg       = away_team.opp_fga_pg
        game.away_opp_fgp          = away_team.opp_fgp
        game.away_opp_ftm_pg       = away_team.opp_ftm_pg
        game.away_opp_fta_pg       = away_team.opp_fta_pg
        game.away_opp_ftp          = away_team.opp_ftp
        game.away_opp_tpm_pg       = away_team.opp_tpm_pg
        game.away_opp_tpa_pg       = away_team.opp_tpa_pg
        game.away_opp_tpp          = away_team.opp_tpp
        game.away_opp_offReb_pg    = away_team.opp_offReb_pg
        game.away_opp_defReb_pg    = away_team.opp_defReb_pg
        game.away_opp_totReb_pg    = away_team.opp_totReb_pg
        game.away_opp_assists_pg   = away_team.opp_assists_pg
        game.away_opp_pFouls_pg    = away_team.opp_pFouls_pg
        game.away_opp_steals_pg    = away_team.opp_steals_pg
        game.away_opp_turnovers_pg = away_team.opp_turnovers_pg
        game.away_opp_blocks_pg    = away_team.opp_blocks_pg
        game.away_opp_plusMinus_pg = away_team.opp_plusMinus_pg

        preds = run_nba_lin_reg(game)
        game.home_linreg_points = preds['home_score']
        game.away_linreg_points = preds['away_score']

        if game.played:

            # Win/loss totals
            home_team.opp_wins   += away_team.wins
            home_team.opp_losses += away_team.losses
            if ( home_team.opp_wins + home_team.opp_losses ) > 0:
                home_team.opp_win_pct = home_team.opp_wins / ( home_team.opp_wins + home_team.opp_losses )
            else:
                home_team.opp_win_pct = 0.0

            away_team.opp_wins   += home_team.wins
            away_team.opp_losses += home_team.losses
            if ( away_team.opp_wins + away_team.opp_losses ):
                away_team.opp_win_pct = away_team.opp_wins / ( away_team.opp_wins + away_team.opp_losses )
            else:
                away_team.opp_win_pct = 0.0

            home_team.games += 1
            away_team.games += 1
            if game.home_points > game.away_points:
                home_team.wins += 1
                away_team.losses += 1
            else:
                home_team.losses += 1
                away_team.wins += 1
            home_team.win_pct = home_team.wins / home_team.games
            away_team.win_pct = away_team.wins / away_team.games

            # Home team per game stats
            home_team.points_pg = ( ( home_team.points_pg * ( home_team.games - 1 ) ) + game.home_points ) / home_team.games
            
            home_team.fgm_pg    = ( ( home_team.fgm_pg * ( home_team.games - 1 ) ) + game.home_fgm ) / home_team.games
            home_team.fga_pg    = ( ( home_team.fga_pg * ( home_team.games - 1 ) ) + game.home_fga ) / home_team.games
            home_team.fgp       = home_team.fgm_pg / home_team.fga_pg

            home_team.ftm_pg    = ( ( home_team.ftm_pg * ( home_team.games - 1 ) ) + game.home_ftm ) / home_team.games
            home_team.fta_pg    = ( ( home_team.fta_pg * ( home_team.games - 1 ) ) + game.home_fta ) / home_team.games
            home_team.ftp       = home_team.ftm_pg / home_team.fta_pg

            home_team.tpm_pg    = ( ( home_team.tpm_pg * ( home_team.games - 1 ) ) + game.home_tpm ) / home_team.games
            home_team.tpa_pg    = ( ( home_team.tpa_pg * ( home_team.games - 1 ) ) + game.home_tpa ) / home_team.games
            home_team.tpp       = home_team.tpm_pg / home_team.tpa_pg

            home_team.offReb_pg    = ( ( home_team.offReb_pg * ( home_team.games - 1 ) ) + game.home_offReb ) / home_team.games
            home_team.defReb_pg    = ( ( home_team.defReb_pg * ( home_team.games - 1 ) ) + game.home_defReb ) / home_team.games
            home_team.totReb_pg    = ( ( home_team.totReb_pg * ( home_team.games - 1 ) ) + game.home_totReb ) / home_team.games

            home_team.assists_pg   = ( ( home_team.assists_pg   * ( home_team.games - 1 ) ) + game.home_assists   ) / home_team.games
            home_team.pFouls_pg    = ( ( home_team.pFouls_pg    * ( home_team.games - 1 ) ) + game.home_pFouls    ) / home_team.games
            home_team.steals_pg    = ( ( home_team.steals_pg    * ( home_team.games - 1 ) ) + game.home_steals    ) / home_team.games
            home_team.turnovers_pg = ( ( home_team.turnovers_pg * ( home_team.games - 1 ) ) + game.home_turnovers ) / home_team.games
            home_team.blocks_pg    = ( ( home_team.blocks_pg    * ( home_team.games - 1 ) ) + game.home_blocks    ) / home_team.games
            home_team.plusMinus_pg = ( ( home_team.plusMinus_pg * ( home_team.games - 1 ) ) + game.home_plusMinus ) / home_team.games

            # Home team opponents per game stats
            home_team.opp_points_pg = ( ( home_team.opp_points_pg * ( home_team.games - 1 ) ) + game.away_points ) / home_team.games
            
            home_team.opp_fgm_pg    = ( ( home_team.opp_fgm_pg * ( home_team.games - 1 ) ) + game.away_fgm ) / home_team.games
            home_team.opp_fga_pg    = ( ( home_team.opp_fga_pg * ( home_team.games - 1 ) ) + game.away_fga ) / home_team.games
            home_team.opp_fgp       = home_team.opp_fgm_pg / home_team.opp_fga_pg

            home_team.opp_ftm_pg    = ( ( home_team.opp_ftm_pg * ( home_team.games - 1 ) ) + game.away_ftm ) / home_team.games
            home_team.opp_fta_pg    = ( ( home_team.opp_fta_pg * ( home_team.games - 1 ) ) + game.away_fta ) / home_team.games
            home_team.opp_ftp       = home_team.opp_ftm_pg / home_team.opp_fta_pg

            home_team.opp_tpm_pg    = ( ( home_team.opp_tpm_pg * ( home_team.games - 1 ) ) + game.away_tpm ) / home_team.games
            home_team.opp_tpa_pg    = ( ( home_team.opp_tpa_pg * ( home_team.games - 1 ) ) + game.away_tpa ) / home_team.games
            home_team.opp_tpp       = home_team.opp_tpm_pg / home_team.opp_tpa_pg

            home_team.opp_offReb_pg    = ( ( home_team.opp_offReb_pg * ( home_team.games - 1 ) ) + game.away_offReb ) / home_team.games
            home_team.opp_defReb_pg    = ( ( home_team.opp_defReb_pg * ( home_team.games - 1 ) ) + game.away_defReb ) / home_team.games
            home_team.opp_totReb_pg    = ( ( home_team.opp_totReb_pg * ( home_team.games - 1 ) ) + game.away_totReb ) / home_team.games

            home_team.opp_assists_pg   = ( ( home_team.opp_assists_pg   * ( home_team.games - 1 ) ) + game.away_assists   ) / home_team.games
            home_team.opp_pFouls_pg    = ( ( home_team.opp_pFouls_pg    * ( home_team.games - 1 ) ) + game.away_pFouls    ) / home_team.games
            home_team.opp_steals_pg    = ( ( home_team.opp_steals_pg    * ( home_team.games - 1 ) ) + game.away_steals    ) / home_team.games
            home_team.opp_turnovers_pg = ( ( home_team.opp_turnovers_pg * ( home_team.games - 1 ) ) + game.away_turnovers ) / home_team.games
            home_team.opp_blocks_pg    = ( ( home_team.opp_blocks_pg    * ( home_team.games - 1 ) ) + game.away_blocks    ) / home_team.games
            home_team.opp_plusMinus_pg = ( ( home_team.opp_plusMinus_pg * ( home_team.games - 1 ) ) + game.away_plusMinus ) / home_team.games
        
            # Away team per game stats
            away_team.points_pg = ( ( away_team.points_pg * ( away_team.games - 1 ) ) + game.away_points ) / away_team.games
            
            away_team.fgm_pg    = ( ( away_team.fgm_pg * ( away_team.games - 1 ) ) + game.away_fgm ) / away_team.games
            away_team.fga_pg    = ( ( away_team.fga_pg * ( away_team.games - 1 ) ) + game.away_fga ) / away_team.games
            away_team.fgp       = away_team.fgm_pg / away_team.fga_pg

            away_team.ftm_pg    = ( ( away_team.ftm_pg * ( away_team.games - 1 ) ) + game.away_ftm ) / away_team.games
            away_team.fta_pg    = ( ( away_team.fta_pg * ( away_team.games - 1 ) ) + game.away_fta ) / away_team.games
            away_team.ftp       = away_team.ftm_pg / away_team.fta_pg

            away_team.tpm_pg    = ( ( away_team.tpm_pg * ( away_team.games - 1 ) ) + game.away_tpm ) / away_team.games
            away_team.tpa_pg    = ( ( away_team.tpa_pg * ( away_team.games - 1 ) ) + game.away_tpa ) / away_team.games
            away_team.tpp       = away_team.tpm_pg / away_team.tpa_pg

            away_team.offReb_pg    = ( ( away_team.offReb_pg * ( away_team.games - 1 ) ) + game.away_offReb ) / away_team.games
            away_team.defReb_pg    = ( ( away_team.defReb_pg * ( away_team.games - 1 ) ) + game.away_defReb ) / away_team.games
            away_team.totReb_pg    = ( ( away_team.totReb_pg * ( away_team.games - 1 ) ) + game.away_totReb ) / away_team.games

            away_team.assists_pg   = ( ( away_team.assists_pg   * ( away_team.games - 1 ) ) + game.away_assists   ) / away_team.games
            away_team.pFouls_pg    = ( ( away_team.pFouls_pg    * ( away_team.games - 1 ) ) + game.away_pFouls    ) / away_team.games
            away_team.steals_pg    = ( ( away_team.steals_pg    * ( away_team.games - 1 ) ) + game.away_steals    ) / away_team.games
            away_team.turnovers_pg = ( ( away_team.turnovers_pg * ( away_team.games - 1 ) ) + game.away_turnovers ) / away_team.games
            away_team.blocks_pg    = ( ( away_team.blocks_pg    * ( away_team.games - 1 ) ) + game.away_blocks    ) / away_team.games
            away_team.plusMinus_pg = ( ( away_team.plusMinus_pg * ( away_team.games - 1 ) ) + game.away_plusMinus ) / away_team.games

            # Away team opponents per game stats
            away_team.opp_points_pg = ( ( away_team.opp_points_pg * ( away_team.games - 1 ) ) + game.home_points ) / away_team.games
            
            away_team.opp_fgm_pg    = ( ( away_team.opp_fgm_pg * ( away_team.games - 1 ) ) + game.home_fgm ) / away_team.games
            away_team.opp_fga_pg    = ( ( away_team.opp_fga_pg * ( away_team.games - 1 ) ) + game.home_fga ) / away_team.games
            away_team.opp_fgp       = away_team.opp_fgm_pg / away_team.opp_fga_pg

            away_team.opp_ftm_pg    = ( ( away_team.opp_ftm_pg * ( away_team.games - 1 ) ) + game.home_ftm ) / away_team.games
            away_team.opp_fta_pg    = ( ( away_team.opp_fta_pg * ( away_team.games - 1 ) ) + game.home_fta ) / away_team.games
            away_team.opp_ftp       = away_team.opp_ftm_pg / away_team.opp_fta_pg

            away_team.opp_tpm_pg    = ( ( away_team.opp_tpm_pg * ( away_team.games - 1 ) ) + game.home_tpm ) / away_team.games
            away_team.opp_tpa_pg    = ( ( away_team.opp_tpa_pg * ( away_team.games - 1 ) ) + game.home_tpa ) / away_team.games
            away_team.opp_tpp       = away_team.opp_tpm_pg / away_team.opp_tpa_pg

            away_team.opp_offReb_pg    = ( ( away_team.opp_offReb_pg * ( away_team.games - 1 ) ) + game.home_offReb ) / away_team.games
            away_team.opp_defReb_pg    = ( ( away_team.opp_defReb_pg * ( away_team.games - 1 ) ) + game.home_defReb ) / away_team.games
            away_team.opp_totReb_pg    = ( ( away_team.opp_totReb_pg * ( away_team.games - 1 ) ) + game.home_totReb ) / away_team.games

            away_team.opp_assists_pg   = ( ( away_team.opp_assists_pg   * ( away_team.games - 1 ) ) + game.home_assists   ) / away_team.games
            away_team.opp_pFouls_pg    = ( ( away_team.opp_pFouls_pg    * ( away_team.games - 1 ) ) + game.home_pFouls    ) / away_team.games
            away_team.opp_steals_pg    = ( ( away_team.opp_steals_pg    * ( away_team.games - 1 ) ) + game.home_steals    ) / away_team.games
            away_team.opp_turnovers_pg = ( ( away_team.opp_turnovers_pg * ( away_team.games - 1 ) ) + game.home_turnovers ) / away_team.games
            away_team.opp_blocks_pg    = ( ( away_team.opp_blocks_pg    * ( away_team.games - 1 ) ) + game.home_blocks    ) / away_team.games
            away_team.opp_plusMinus_pg = ( ( away_team.opp_plusMinus_pg * ( away_team.games - 1 ) ) + game.home_plusMinus ) / away_team.games

        # Save game, home, and away teams
        home_team.save()
        away_team.save()
        game.save()

def nba_rankings():
    for stat in NBA_TEAM_DB_STATS_FIELDS_LIST:
        stat_name = "-" + str(stat)
        stat_rank = "rank_" + str(stat)
        sorted_db = NBATeam.objects.all().order_by(stat_name)
        for idx,team in enumerate(sorted_db):
            setattr(team, stat_rank, idx + 1)
            team.save()

def export_nba_stats_to_csv(years):
    csv_filename = "nba_training_data.csv"
    with open(csv_filename,'w') as f:
        writer = csv.writer(f)
        for year in years:
            sch_obj = get_schedule_db(year)
            games = sch_obj.objects.all()
            field_names = [field.name for field in sch_obj._meta.get_fields()]
            writer.writerow(field_names)
            for game in games:
                writer.writerow([getattr(game, field) for field in field_names])

def run_nba_lin_reg(game):
    preds = {}
    scaler_filename       = "SportsApp/ml_models/nba_scaler.sav"
    home_lin_reg_filename = "SportsApp/ml_models/nba_lin_reg_home_points.sav"
    away_lin_reg_filename = "SportsApp/ml_models/nba_lin_reg_away_points.sav"

    scaler       = pickle.load(open(scaler_filename,  'rb'))
    home_lin_reg = pickle.load(open(home_lin_reg_filename, 'rb'))
    away_lin_reg = pickle.load(open(away_lin_reg_filename, 'rb'))

    game_dict = game.__dict__
    game_df = pd.DataFrame(data=game_dict, index=[0])

    for col in game_df.columns:
        if col not in NBA_LIN_REG_PREDICTORS_LIST:
            game_df = game_df.drop(columns=[col])

    game_scaled = scaler.transform(game_df)

    preds['home_score'] = round(float(home_lin_reg.predict(game_scaled)),1)
    preds['away_score'] = round(float(away_lin_reg.predict(game_scaled)),1)

    return preds

def get_nba_game_predictions(game):
    preds = {}
    preds['lin_reg'] = {
        'home_score': game.home_linreg_points,
        'away_score': game.away_linreg_points
    }
    return preds
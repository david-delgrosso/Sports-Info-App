import datetime
import os
from .models import *
from .constants import *
import json
from .restapis import *
import time

# general utilities
def convert_time(time_in):
    pass

def convert_date(date_in):
    pass

# Returns a list of today's game objects
def get_todays_games(sport):
    today = str(datetime.now().strftime("%Y-%m-%d"))
    games = NBASchedule.objects.filter(sport=sport, date=today)
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
# Populate NBA Schedule database from json file
def load_nba_schedule_to_db():
    # Load json data
    f = open('nba_season_2022.json')
    data = json.load(f)

    # Iterate over games
    for game in data['response']:

        # Determine game start time
        date_str = game['date']['start'][:-5].replace('T',' ')
        game_datetime = datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
        game_date = game_datetime.date()
        game_time = game_datetime.time()

        # Ignore preseason games
        if game_datetime < NBA_SEASON_START_DATE_2022:
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
        sch_obj = NBASchedule.objects.create(id=game['id'],
                                             sport="NBA",
                                             date=game_date,
                                             home_team=home_team,
                                             away_team=away_team,
                                             time=game_time)
        
# Parent function for generating NBA Schedule database        
def get_nba_schedule():
    #request_nba_schedule_to_json()
    load_nba_schedule_to_db()

# Load NBA Teams dictionary into NBA Teams database
def load_nba_teams_to_db():
    for k,v in NBA_TEAMS_DICT.items():
        team_obj = NBATeam.objects.create(id=NBA_API_ID_DICT[k],
                                          name=k,
                                          city=v,
                                          sport="NBA")

def backfill_nba_stats():
    games = NBASchedule.objects.all()
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
                break
        except:
            time.sleep(60)
            game_stats_str = request_nba_game_stats(str(game.id))
            game_stats_json = json.loads(game_stats_str)

        # Maximum iterations fail check
        if i > 400:
            break

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

# Parse NBA Schedule database to calculate aggregate team stats
def update_nba_team_stats():
    games = NBASchedule.objects.all()
    reset_nba_team_fields()
    for game in games:
        if game.played:
            home_team = game.home_team
            away_team = game.away_team

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

            # Save home and away teams
            home_team.save()
            away_team.save()


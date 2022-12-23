from SportsApp.models import NBASchedule2017, NBASchedule2018, NBASchedule2019, NBASchedule2020, NBASchedule2021, NBASchedule2022, NBATeam, NBAModelPredictions, NBAOdds2022
from SportsApp.constants import *
from SportsApp.restapis import request_nba_schedule_to_json, request_nba_game_stats, request_nba_game_odds
from SportsApp.ML import NBALinReg
import json
from datetime import datetime, timedelta
import time
import csv
from math import sqrt

# Class to hold all logic pertaining to NBA database management,
# statistics generation, and model predictions
class NBA:
    def __init__(self, year):
        self.year = year
        self.sch_obj = self.get_schedule_obj(self.year)
        self.pred_obj = NBAModelPredictions
        self.teams_list = []
        self.models = {
            'Linear Regression' : NBALinReg(),
        }

    def __str__(self):
        return f"{self.year} NBA object"

    # Clear schedule of the selected year
    def clear_schedule(self):
        self.sch_obj.objects.all().delete()

    # Get schedule object for a specified year
    # @param[in]    year     year of schedule object to retreive
    # @param[out]   sch_obj  schedule corresponding to specified year
    def get_schedule_obj(self, year):
        if year == 2022:
            sch_obj = NBASchedule2022
        elif year == 2021:
            sch_obj = NBASchedule2021
        elif year == 2020:
            sch_obj = NBASchedule2020
        elif self.year == 2019:
            sch_obj = NBASchedule2019
        elif year == 2018:
            sch_obj = NBASchedule2018
        elif year == 2017:
            sch_obj = NBASchedule2017
        return sch_obj

    # Set schedule object to that corresponding to the selected year
    def set_schedule_obj(self):
        if self.year == 2022:
            self.sch_obj = NBASchedule2022
        elif self.year == 2021:
            self.sch_obj = NBASchedule2021
        elif self.year == 2020:
            self.sch_obj = NBASchedule2020
        elif self.year == 2019:
            self.sch_obj = NBASchedule2019
        elif self.year == 2018:
            self.sch_obj = NBASchedule2018
        elif self.year == 2017:
            self.sch_obj = NBASchedule2017

    # Get the games scheduled on a specified date
    # @param[in]    day    day to retreive games for
    def get_games(self, day):
        games = self.sch_obj.objects.filter(sport="NBA", date=day)
        return games

    # Get the predictions for games scheduled on a specified date
    # @param[in]    day    day to retreive games for
    def get_preds(self, day):
        games = self.get_games(day)
        id_list = [game.id for game in games]
        preds = self.pred_obj.objects.filter(pk__in=id_list)
        return preds

    # Reset all team stats to their default values
    def reset_team_stats(self):
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

    # Parse JSON file corresponding to selected year and populate
    # schedule database with matchups and times
    def load_schedule(self):
        # Load json data
        filename = "../nba_season_" + str(self.year) + ".json"
        f = open(filename)
        data = json.load(f)

        i = 0 # loop counter
        n = len(data['response'])

        # Iterate over games
        for game in data['response']:
            i += 1

            # Determine game date and start time
            date_str = str(game['date']['start'])
            if len(date_str) > 10:
                date_str = date_str[:-5].replace('T',' ')
                game_datetime = datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
                game_date = game_datetime.date()
                game_time = game_datetime.time()
            elif len(date_str) == 10:
                if self.year == 2022:
                    raise Exception("Current schedule date needs a time")
                else:
                    game_datetime = datetime.strptime(date_str,'%Y-%m-%d')
                    game_date = game_datetime.date()
                    game_time = game_datetime.time()

            # Ignore preseason games
            if game_datetime < NBA_SEASON_START_DATE_DICT[str(self.year)]:
                self.printProgressBar(i,n,'Loading Schedule to Database...')
                continue

            # Find home and away team objects
            # Ignore non NBA teams
            home_team_id = game['teams']['home']['id']
            try:
                home_team = NBATeam.objects.get(id=home_team_id)
            except:
                print(str(game['teams']['home']['name']) + " was not recognized as an NBA team. The game was not added to the schedule.")
                self.printProgressBar(i,n,'Loading Schedule to Database...')
                continue
        
            away_team_id = game['teams']['visitors']['id']
            try:
                away_team = NBATeam.objects.get(id=away_team_id)
            except:
                print(str(game['teams']['visitors']['name']) + " was not recognized as an NBA team. The game was not added to the schedule.")
                self.printProgressBar(i+1,n,'Loading Schedule to Database...')
                continue

            # Add game to schedule database
            self.sch_obj.objects.create(id=game['id'],
                                        sport="NBA",
                                        date=game_date,
                                        home_team=home_team,
                                        away_team=away_team,
                                        time=game_time)

            self.printProgressBar(i,n,'Loading Schedule to Database...')

    # Use API function to download schedule for selected year to JSON file
    def download_schedule(self):
        request_nba_schedule_to_json(self.year)

    # Load team info to teams database
    def load_teams(self):
        # teams = NBATeam.objects.all()
        # for team in teams:
        #     team.full_name = str(team.city) + " " + str(team.name)
        #     team.save()

        for k,v in NBA_TEAMS_DICT.items():
            NBATeam.objects.create(id=NBA_API_ID_DICT[k],
                                   name=k,
                                   city=v,
                                   sport="NBA")
            team_name = str(v) + " " + str(k)
            self.teams_list.append(team_name)
        self.teams_list = sorted(self.teams_list)

    # Download boxscore stats from API for each completed game
    def download_game_stats(self):

        # Get all games in selected year
        games = self.sch_obj.objects.all()

        i = 0 # loop counter
        n = len(games)

        # Iterate over games in schedule
        for game in games:
            i += 1 # increment loop counter

            # Ignore games that already have stats filled
            if game.boxscore_filled:
                self.printProgressBar(i,n,'Loading Stats to Database...')
                continue

            # Request game stats
            game_stats_str = request_nba_game_stats(str(game.id))
            game_stats_json = json.loads(game_stats_str)

            # Break if game has not been played yet
            if len(game_stats_json['response']) == 0:
                break
            
            # Save stats from JSON to game object
            # For some reason home/away stats are reversed for previous years compared to 2022
            if self.year == 2022:
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
            game.boxscore_filled = True
            
            # Update table fields to reflect statistics
            game.save()

            # Print completion message
            self.printProgressBar(i,n,'Loading Stats to Database...')

            # Sleep so as to not exceed API call frequency limits
            time.sleep(0.5)

    # Iterate over games played to calculate aggregate team stats
    def calculate_team_stats(self):

        # Get games for selected year
        games = self.sch_obj.objects.all()

        i = 0 # loop counter
        n = len(games)

        # Iterate over games
        for game in games:
            i += 1 # increment loop counter

            if game.team_stats_filled:
                self.printProgressBar(i,n,'Calculating Team Stats...')
                continue

            # Latch onto team objects
            home_team = game.home_team
            away_team = game.away_team

            # Set flag if game is first game for either team
            if ( ( home_team.games == 0 ) or ( away_team.games == 0 ) ):
                game.first_game = True

            # Save team statistics for home team going into the game
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

            # Save team statistics for away team going into the game
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

            # Include boxscore stats for game in aggregate team stats if game has been played
            if game.boxscore_filled:
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

                game.team_stats_filled = True

            # Save game, home, and away teams
            home_team.save()
            away_team.save()
            game.save()
            self.printProgressBar(i,n,'Calculating Team Stats...')

    # Set team rankings for each team stat recorded
    def set_rankings(self):

        # Iterate over all stats in database
        for stat in NBA_TEAM_DB_STATS_FIELDS_LIST:

            # Get stat and ranking field names
            stat_name = "-" + str(stat) # "-" included to specify descending order
            stat_rank = "rank_" + str(stat)

            # Query database filtering by specified stat
            sorted_db = NBATeam.objects.all().order_by(stat_name)

            # Iterate over queryset
            for idx,team in enumerate(sorted_db):

                # Reverse ranking if opposing team stat
                if stat_name[1:4] == 'opp':
                    setattr(team, stat_rank, len(sorted_db) - idx)
                else:
                    setattr(team, stat_rank, idx + 1)
                
                # Save team object to database
                team.save()

    # Export schedule database to csv file for model development
    # @param[in]    years    years to be exported to csv
    def export_team_stats(self, years):

        # Set filename to save to
        csv_filename = "nba_training_data.csv"

        # Open file
        with open(csv_filename,'w') as f:
            
            # Create writer object
            writer = csv.writer(f)

            # Get temporary schedule object to save field names
            sch_obj_temp = self.get_schedule_obj([years[0]])
            
            # Loop over field names in schedule object to write as column headers
            field_names = [field.name for field in sch_obj_temp._meta.get_fields()]
            writer.writerow(field_names)

            # Iterate over years specified
            for year in years:

                # Get all games in year
                sch_obj = self.get_schedule_obj(year)
                games = sch_obj.objects.all()

                # Iterate over games and write every stat to csv
                for game in games:
                    writer.writerow([getattr(game, field) for field in field_names])

    # Clear NBA predictions
    def clear_predictions(self):
        self.pred_obj.objects.all().delete()

    # Calculate predictions for each model   
    def calculate_predictions(self):

        # Get games for selected year
        games = self.sch_obj.objects.all()

        i = 0 # loop counter
        n = len(games)

        # Iterate over games
        for game in games:
            i += 1 # increment loop counter

            try:
                # Grab predictions object corresponding to this game
                pred = self.pred_obj.objects.get(id=game.id)
            except:
                pred = self.pred_obj.objects.create(id=game)

            # Generate predictions
            pred.home_points_lr, pred.away_points_lr = self.models['Linear Regression'].predict_game(game)

            # Copy in vegas predictions
            if game.boxscore_filled and game.team_stats_filled:
                try:
                    odds = NBAOdds2022.objects.get(date=game.date,
                                                home_team=game.home_team,
                                                away_team=game.away_team)
                    if odds.home_spread < 0:
                        pred.away_points_vegas = ( odds.total + odds.home_spread ) / 2
                        pred.home_points_vegas = pred.away_points_vegas - odds.home_spread
                    elif odds.home_spread > 0:
                        pred.home_points_vegas = ( odds.total + odds.away_spread ) / 2
                        pred.away_points_vegas = pred.home_points_vegas - odds.away_spread
                    else:
                        pred.home_points_vegas = odds.total / 2
                        pred.away_points_vegas = odds.total / 2

                except:
                    #print(f"{game.away_team.full_name} @ {game.home_team.full_name} on {game.date}")
                    pred.away_points_vegas = 0
                    pred.home_points_vegas = 0

            # Save predictions to database
            pred.save()

            # Print progress bar
            self.printProgressBar(i, n, 'Generating predictions...')

    # Calculate error for each model
    def calculate_pred_error(self):
        # Get games for selected year
        games = self.sch_obj.objects.all()

        home_diff_vegas_tot_err = 0
        away_diff_vegas_tot_err = 0
        home_points_vegas_cum_me = 0
        away_points_vegas_cum_me = 0

        home_diff_vegas_sqr_err = 0
        away_diff_vegas_sqr_err = 0
        home_points_vegas_cum_rmse = 0
        away_points_vegas_cum_rmse = 0

        home_diff_lr_tot_err = 0
        away_diff_lr_tot_err = 0
        home_points_lr_cum_me = 0
        away_points_lr_cum_me = 0

        home_diff_lr_sqr_err = 0
        away_diff_lr_sqr_err = 0
        home_points_lr_cum_rmse = 0
        away_points_lr_cum_rmse = 0

        i = 0 # loop counter
        n = len(games)

        # Iterate over games
        for game in games:
            i += 1 # increment loop counter

            # Grab predictions object corresponding to this game
            pred = self.pred_obj.objects.get(id=game.id)

            # Calculate RMSE if stats are filled
            if game.boxscore_filled and game.team_stats_filled:
                if pred.home_points_vegas > 0 and pred.away_points_vegas > 0:
                    home_diff_vegas_tot_err += game.home_points - pred.home_points_vegas
                    away_diff_vegas_tot_err += game.away_points - pred.away_points_vegas
                    home_points_vegas_cum_me = home_diff_vegas_tot_err / i
                    away_points_vegas_cum_me = away_diff_vegas_tot_err / i
                    
                    home_diff_vegas_sqr_err += (game.home_points - pred.home_points_vegas) ** 2
                    away_diff_vegas_sqr_err += (game.away_points - pred.away_points_vegas) ** 2
                    home_points_vegas_cum_rmse = sqrt(home_diff_vegas_sqr_err / i)
                    away_points_vegas_cum_rmse = sqrt(away_diff_vegas_sqr_err / i)    

                home_diff_lr_tot_err += game.home_points - pred.home_points_lr
                away_diff_lr_tot_err += game.away_points - pred.away_points_lr
                home_points_lr_cum_me = home_diff_lr_tot_err / i
                away_points_lr_cum_me = away_diff_lr_tot_err / i

                home_diff_lr_sqr_err += (game.home_points - pred.home_points_lr) ** 2
                away_diff_lr_sqr_err += (game.away_points - pred.away_points_lr) ** 2
                home_points_lr_cum_rmse = sqrt(home_diff_lr_sqr_err / i)
                away_points_lr_cum_rmse = sqrt(away_diff_lr_sqr_err / i)           

            # Save predictions to database
            pred.home_points_vegas_cum_me = home_points_vegas_cum_me
            pred.away_points_vegas_cum_me = away_points_vegas_cum_me
            pred.home_points_lr_cum_me    = home_points_lr_cum_me
            pred.away_points_lr_cum_me    = away_points_lr_cum_me
            
            pred.home_points_vegas_cum_rmse = home_points_vegas_cum_rmse
            pred.away_points_vegas_cum_rmse = away_points_vegas_cum_rmse
            pred.home_points_lr_cum_rmse    = home_points_lr_cum_rmse
            pred.away_points_lr_cum_rmse    = away_points_lr_cum_rmse
            
            pred.save()

            # Print progress bar
            self.printProgressBar(i, n, 'Calculating model error...')

    def predict_single_game(self, model, home_team_name, away_team_name):
        game = {}

        # Grab home team stats
        home_team_sp = home_team_name.split(' ')
        if home_team_sp[-1] in NBA_TEAMS_DICT:
            home_team = NBATeam.objects.get(name=home_team_sp[-1])
        else:
            home_team = NBATeam.objects.get(name=home_team_sp[-2:])
        home_team_dict = home_team.__dict__

        # Save home team stats in game dictionary
        for k,v in home_team_dict.items():
            col = "home_" + str(k)
            game[col] = v

        # Grab away team stats
        away_team_sp = away_team_name.split(' ')
        if away_team_sp[-1] in NBA_TEAMS_DICT:
            away_team = NBATeam.objects.get(name=away_team_sp[-1])
        else:
            away_team = NBATeam.objects.get(name=away_team_sp[-2:])
        away_team_dict = away_team.__dict__

        # Save away team stats in game dictionary
        for k,v in away_team_dict.items():
            col = "away_" + str(k)
            game[col] = v

        # Run predict ML method and return preditions
        return self.models[model].predict_game(game)

    # Print iterations progress
    def printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        if iteration == total:
            percent = 100
            filledLength = length
        else:
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

    def download_game_odds(self):
        #NBAOdds2022.objects.all().delete()

        #####################################################################
        ### DELETE THIS
        #####################################################################

        # odds_str = request_nba_game_odds("2022-10-26")

        games = self.sch_obj.objects.all()
        dates = []
        for game in games:
            if game.boxscore_filled and game.team_stats_filled:
                dates.append(game.date)
        n_games_sch = len(dates)
        dates_set = set(dates)
        unique_dates = (list(dates_set))
        unique_dates.sort(key=lambda date: date)

        i = 0
        n = len(unique_dates)

        empty_games = []

        for date in unique_dates:
            i += 1

            odds_str = request_nba_game_odds(str(date))
            odds_json = json.loads(odds_str)
            
            # f = open("test_game_odds.json")
            # odds_json = json.load(f)

            data = odds_json['data']
            for game in data:
                game_id = game['id']

                date_str = str(game['commence_time'])
                date_str = date_str[:-1].replace('T',' ')
                game_datetime = datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S') - timedelta(hours=4)
                game_date = game_datetime.date()

                game_home_team_full_name = game['home_team']
                game_away_team_full_name = game['away_team']

                try:
                    game_home_spread = game['bookmakers'][0]['markets'][0]['outcomes'][0]['point']
                    game_away_spread = game['bookmakers'][0]['markets'][0]['outcomes'][1]['point']
                    game_total = game['bookmakers'][0]['markets'][1]['outcomes'][0]['point']
                except:
                    empty_games.append(game_id)
                    continue
                
                try:
                    NBAOdds2022.objects.get(id=game_id)
                except:
                    game_home_team = NBATeam.objects.get(full_name=game_home_team_full_name)
                    game_away_team = NBATeam.objects.get(full_name=game_away_team_full_name)
                    NBAOdds2022.objects.create(id=game_id,
                                               date=game_date,
                                               home_team=game_home_team,
                                               away_team=game_away_team,
                                               home_spread=game_home_spread,
                                               away_spread=game_away_spread,
                                               total=game_total)

            # Print completion message
            self.printProgressBar(i,n,'Loading Odds to Database...')

            time.sleep(0.5)

        actual_empty_games = []
        for game_id in empty_games:
            try:
                NBAOdds2022.objects.get(id=game_id)
            except:
                actual_empty_games.append(game_id)

        n_games_odds = len(NBAOdds2022.objects.all())
        print("Game totals do not add up...")
        print("Total Games: ", n_games_sch)
        print("Games Filled: ", n_games_odds)
        print("Games Empty: ", len(actual_empty_games))
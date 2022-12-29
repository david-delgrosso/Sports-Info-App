from SportsApp.models import NBASchedule2017, NBASchedule2018, NBASchedule2019, NBASchedule2020, NBASchedule2021, NBASchedule2022, NBAGameStats2017, NBAGameStats2018, NBAGameStats2019, NBAGameStats2020, NBAGameStats2021, NBAGameStats2022, NBATeam, NBAPredictions2022, NBAOdds2022
from SportsApp.constants import *
from SportsApp.restapis import request_nba_schedule_to_json, request_nba_game_stats, request_nba_game_odds
from SportsApp.ML import NBALinReg, NBAPolyReg, NBAElnReg
import json
from datetime import datetime, timedelta
import time
import csv
from math import sqrt
import numpy as np
import scipy.optimize

# Class to hold all logic pertaining to NBA database management,
# statistics generation, and model predictions
class NBA:
    def __init__(self, year):
        self.year = year
        self.sch_obj = self.get_schedule_obj(self.year)
        self.game_stats_obj = self.get_game_stats_obj(self.year)
        self.pred_obj = NBAPredictions2022
        self.odds_obj = NBAOdds2022
        self.teams_obj = NBATeam
        self.teams_list = []
        self.models = {
            'Linear Regression' : NBALinReg(),
            'Polynomial Regression' : NBAPolyReg(),
            'Elastic Net Regression' : NBAElnReg(),
        }
        self.home_adv = 0.0
        self.load_teams()

    def __str__(self):
        return f"{self.year} NBA object"

    # Load team info to teams database
    def load_teams(self):
        for k,v in NBA_TEAMS_DICT.items():
            full_name = str(v) + " " + str(k)
            # self.teams_obj.objects.create(id=NBA_API_ID_DICT[k],
            #                        name=k,
            #                        city=v,
            #                        full_name=full_name)
            team_name = str(v) + " " + str(k)
            self.teams_list.append(team_name)
        self.teams_list = sorted(self.teams_list)
        for idx,name in enumerate(self.teams_list):
            team_obj = self.teams_obj.objects.get(full_name=name)
            team_obj.alpha_id = idx + 1
            team_obj.save()

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
    
    # Clear schedule of the selected year
    def clear_schedule(self):
        self.sch_obj.objects.all().delete()

    # Use API function to download schedule for selected year to JSON file
    def download_schedule(self):
        request_nba_schedule_to_json(self.year)

    # Parse JSON file corresponding to selected year and populate
    # schedule database with matchups and times
    def load_schedule(self):
        # Load json data
        filename = f"{NBA_DATA_PATH}nba_season_{self.year}.json"
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
                home_team = self.teams_obj.objects.get(id=home_team_id)
            except:
                print(str(game['teams']['home']['name']) + " was not recognized as an NBA team. The game was not added to the schedule.")
                self.printProgressBar(i,n,'Loading Schedule to Database...')
                continue
        
            away_team_id = game['teams']['visitors']['id']
            try:
                away_team = self.teams_obj.objects.get(id=away_team_id)
            except:
                print(str(game['teams']['visitors']['name']) + " was not recognized as an NBA team. The game was not added to the schedule.")
                self.printProgressBar(i+1,n,'Loading Schedule to Database...')
                continue

            # Add game to schedule database
            self.sch_obj.objects.create(id=game['id'],
                                        time=game_time,
                                        date=game_date,
                                        home_team=home_team,
                                        away_team=away_team)

            self.printProgressBar(i,n,'Loading Schedule to Database...')

    # Get the games scheduled on a specified date
    # @param[in]    day    day to retreive games for
    def get_games(self, day):
        games = self.sch_obj.objects.filter(date=day)
        return games

    # Get game stats object for a specified year
    # @param[in]    year     year of game stass object to retreive
    # @param[out]   sch_obj  game stats object corresponding to specified year
    def get_game_stats_obj(self, year):
        if year == 2022:
            sch_obj = NBAGameStats2022
        elif year == 2021:
            sch_obj = NBAGameStats2021
        elif year == 2020:
            sch_obj = NBAGameStats2020
        elif year == 2019:
            sch_obj = NBAGameStats2019
        elif year == 2018:
            sch_obj = NBAGameStats2018
        elif year == 2017:
            sch_obj = NBAGameStats2017
        return sch_obj

    # Set game stats object to that corresponding to the selected year
    def set_game_stats_obj(self):
        if self.year == 2022:
            self.sch_obj = NBAGameStats2022
        elif self.year == 2021:
            self.sch_obj = NBAGameStats2021
        elif self.year == 2020:
            self.sch_obj = NBAGameStats2020
        elif self.year == 2019:
            self.sch_obj = NBAGameStats2019
        elif self.year == 2018:
            self.sch_obj = NBAGameStats2018
        elif self.year == 2017:
            self.sch_obj = NBAGameStats2017

    # Clear schedule of the selected year
    def clear_game_stats(self):
        self.game_stats_obj.objects.all().delete()

    # Download boxscore stats from API for each completed game
    def download_game_stats(self):

        # Get all games in selected year
        game_sch = self.sch_obj.objects.all()

        i = 0 # loop counter
        n = len(game_sch)

        # Iterate over games in schedule
        for sch in game_sch:
            i += 1 # increment loop counter

            # Ignore games that already have stats filled
            if sch.game_stats_filled:
                self.printProgressBar(i,n,'Loading Stats to Database...')
                continue

            # Request game stats
            game_stats_str = request_nba_game_stats(str(sch.id))
            game_stats_json = json.loads(game_stats_str)

            # Break if game has not been played yet
            if len(game_stats_json['response']) == 0:
                if self.year == 2022:
                    break
                else:
                    continue

            try:
                # Grab predictions object corresponding to this game
                game_stats = self.game_stats_obj.objects.get(id=sch)
            except:
                game_stats = self.game_stats_obj.objects.create(id=sch)
            
            # Save stats from JSON to game object
            # For some reason home/away stats are reversed for previous years compared to 2022
            if self.year == 2022:
                # Save home team stats
                game_stats.home_points    = game_stats_json['response'][0]['statistics'][0]['points']
                game_stats.home_fgm       = game_stats_json['response'][0]['statistics'][0]['fgm']
                game_stats.home_fga       = game_stats_json['response'][0]['statistics'][0]['fga']
                game_stats.home_fgp       = game_stats_json['response'][0]['statistics'][0]['fgp']
                game_stats.home_ftm       = game_stats_json['response'][0]['statistics'][0]['ftm']
                game_stats.home_fta       = game_stats_json['response'][0]['statistics'][0]['fta']
                game_stats.home_ftp       = game_stats_json['response'][0]['statistics'][0]['ftp']
                game_stats.home_tpm       = game_stats_json['response'][0]['statistics'][0]['tpm']
                game_stats.home_tpa       = game_stats_json['response'][0]['statistics'][0]['tpa']
                game_stats.home_tpp       = game_stats_json['response'][0]['statistics'][0]['tpp']
                game_stats.home_offReb    = game_stats_json['response'][0]['statistics'][0]['offReb']
                game_stats.home_defReb    = game_stats_json['response'][0]['statistics'][0]['defReb']
                game_stats.home_totReb    = game_stats_json['response'][0]['statistics'][0]['totReb']
                game_stats.home_assists   = game_stats_json['response'][0]['statistics'][0]['assists']
                game_stats.home_pFouls    = game_stats_json['response'][0]['statistics'][0]['pFouls']
                game_stats.home_steals    = game_stats_json['response'][0]['statistics'][0]['steals']
                game_stats.home_turnovers = game_stats_json['response'][0]['statistics'][0]['turnovers']
                game_stats.home_blocks    = game_stats_json['response'][0]['statistics'][0]['blocks']
                game_stats.home_plusMinus = game_stats_json['response'][0]['statistics'][0]['plusMinus']
                
                # Save away stats
                game_stats.away_points    = game_stats_json['response'][1]['statistics'][0]['points']
                game_stats.away_fgm       = game_stats_json['response'][1]['statistics'][0]['fgm']
                game_stats.away_fga       = game_stats_json['response'][1]['statistics'][0]['fga']
                game_stats.away_fgp       = game_stats_json['response'][1]['statistics'][0]['fgp']
                game_stats.away_ftm       = game_stats_json['response'][1]['statistics'][0]['ftm']
                game_stats.away_fta       = game_stats_json['response'][1]['statistics'][0]['fta']
                game_stats.away_ftp       = game_stats_json['response'][1]['statistics'][0]['ftp']
                game_stats.away_tpm       = game_stats_json['response'][1]['statistics'][0]['tpm']
                game_stats.away_tpa       = game_stats_json['response'][1]['statistics'][0]['tpa']
                game_stats.away_tpp       = game_stats_json['response'][1]['statistics'][0]['tpp']
                game_stats.away_offReb    = game_stats_json['response'][1]['statistics'][0]['offReb']
                game_stats.away_defReb    = game_stats_json['response'][1]['statistics'][0]['defReb']
                game_stats.away_totReb    = game_stats_json['response'][1]['statistics'][0]['totReb']
                game_stats.away_assists   = game_stats_json['response'][1]['statistics'][0]['assists']
                game_stats.away_pFouls    = game_stats_json['response'][1]['statistics'][0]['pFouls']
                game_stats.away_steals    = game_stats_json['response'][1]['statistics'][0]['steals']
                game_stats.away_turnovers = game_stats_json['response'][1]['statistics'][0]['turnovers']
                game_stats.away_blocks    = game_stats_json['response'][1]['statistics'][0]['blocks']
                game_stats.away_plusMinus = game_stats_json['response'][1]['statistics'][0]['plusMinus']
            else:
                # Save away team stats
                game_stats.away_points    = game_stats_json['response'][0]['statistics'][0]['points']
                game_stats.away_fgm       = game_stats_json['response'][0]['statistics'][0]['fgm']
                game_stats.away_fga       = game_stats_json['response'][0]['statistics'][0]['fga']
                game_stats.away_fgp       = game_stats_json['response'][0]['statistics'][0]['fgp']
                game_stats.away_ftm       = game_stats_json['response'][0]['statistics'][0]['ftm']
                game_stats.away_fta       = game_stats_json['response'][0]['statistics'][0]['fta']
                game_stats.away_ftp       = game_stats_json['response'][0]['statistics'][0]['ftp']
                game_stats.away_tpm       = game_stats_json['response'][0]['statistics'][0]['tpm']
                game_stats.away_tpa       = game_stats_json['response'][0]['statistics'][0]['tpa']
                game_stats.away_tpp       = game_stats_json['response'][0]['statistics'][0]['tpp']
                game_stats.away_offReb    = game_stats_json['response'][0]['statistics'][0]['offReb']
                game_stats.away_defReb    = game_stats_json['response'][0]['statistics'][0]['defReb']
                game_stats.away_totReb    = game_stats_json['response'][0]['statistics'][0]['totReb']
                game_stats.away_assists   = game_stats_json['response'][0]['statistics'][0]['assists']
                game_stats.away_pFouls    = game_stats_json['response'][0]['statistics'][0]['pFouls']
                game_stats.away_steals    = game_stats_json['response'][0]['statistics'][0]['steals']
                game_stats.away_turnovers = game_stats_json['response'][0]['statistics'][0]['turnovers']
                game_stats.away_blocks    = game_stats_json['response'][0]['statistics'][0]['blocks']
                game_stats.away_plusMinus = game_stats_json['response'][0]['statistics'][0]['plusMinus']
                
                # Save home stats
                game_stats.home_points    = game_stats_json['response'][1]['statistics'][0]['points']
                game_stats.home_fgm       = game_stats_json['response'][1]['statistics'][0]['fgm']
                game_stats.home_fga       = game_stats_json['response'][1]['statistics'][0]['fga']
                game_stats.home_fgp       = game_stats_json['response'][1]['statistics'][0]['fgp']
                game_stats.home_ftm       = game_stats_json['response'][1]['statistics'][0]['ftm']
                game_stats.home_fta       = game_stats_json['response'][1]['statistics'][0]['fta']
                game_stats.home_ftp       = game_stats_json['response'][1]['statistics'][0]['ftp']
                game_stats.home_tpm       = game_stats_json['response'][1]['statistics'][0]['tpm']
                game_stats.home_tpa       = game_stats_json['response'][1]['statistics'][0]['tpa']
                game_stats.home_tpp       = game_stats_json['response'][1]['statistics'][0]['tpp']
                game_stats.home_offReb    = game_stats_json['response'][1]['statistics'][0]['offReb']
                game_stats.home_defReb    = game_stats_json['response'][1]['statistics'][0]['defReb']
                game_stats.home_totReb    = game_stats_json['response'][1]['statistics'][0]['totReb']
                game_stats.home_assists   = game_stats_json['response'][1]['statistics'][0]['assists']
                game_stats.home_pFouls    = game_stats_json['response'][1]['statistics'][0]['pFouls']
                game_stats.home_steals    = game_stats_json['response'][1]['statistics'][0]['steals']
                game_stats.home_turnovers = game_stats_json['response'][1]['statistics'][0]['turnovers']
                game_stats.home_blocks    = game_stats_json['response'][1]['statistics'][0]['blocks']
                game_stats.home_plusMinus = game_stats_json['response'][1]['statistics'][0]['plusMinus']
            
            # Set game played flag
            sch.game_stats_filled = True
            
            # Update table fields to reflect statistics
            sch.save()
            game_stats.save()

            # Print completion message
            self.printProgressBar(i,n,'Loading Stats to Database...')

            # Sleep so as to not exceed API call frequency limits
            time.sleep(0.5)

    # Get the game stats for games scheduled on a specified date
    # @param[in]    day     day to retreive games for
    # @param[out]   stats   game stats for each game on specified date
    def get_game_stats(self, day):
        games = self.get_games(day)
        id_list = [game.id for game in games]
        stats = self.game_stats_obj.objects.filter(pk__in=id_list)
        return stats

    # Reset all team stats to their default values
    def reset_team_stats(self):
        teams = self.teams_obj.objects.all()
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

            team.rank_points_pg    = 0.0
            team.rank_fgm_pg       = 0.0
            team.rank_fga_pg       = 0.0
            team.rank_fgp          = 0.0
            team.rank_ftm_pg       = 0.0
            team.rank_fta_pg       = 0.0
            team.rank_ftp          = 0.0
            team.rank_tpm_pg       = 0.0
            team.rank_tpa_pg       = 0.0
            team.rank_tpp          = 0.0
            team.rank_offReb_pg    = 0.0
            team.rank_defReb_pg    = 0.0
            team.rank_totReb_pg    = 0.0
            team.rank_assists_pg   = 0.0
            team.rank_pFouls_pg    = 0.0
            team.rank_steals_pg    = 0.0
            team.rank_turnovers_pg = 0.0
            team.rank_blocks_pg    = 0.0
            team.rank_plusMinus_pg = 0.0

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

            team.rank_opp_points_pg    = 0.0
            team.rank_opp_fgm_pg       = 0.0
            team.rank_opp_fga_pg       = 0.0
            team.rank_opp_fgp          = 0.0
            team.rank_opp_ftm_pg       = 0.0
            team.rank_opp_fta_pg       = 0.0
            team.rank_opp_ftp          = 0.0
            team.rank_opp_tpm_pg       = 0.0
            team.rank_opp_tpa_pg       = 0.0
            team.rank_opp_tpp          = 0.0
            team.rank_opp_offReb_pg    = 0.0
            team.rank_opp_defReb_pg    = 0.0
            team.rank_opp_totReb_pg    = 0.0
            team.rank_opp_assists_pg   = 0.0
            team.rank_opp_pFouls_pg    = 0.0
            team.rank_opp_steals_pg    = 0.0
            team.rank_opp_turnovers_pg = 0.0
            team.rank_opp_blocks_pg    = 0.0
            team.rank_opp_plusMinus_pg = 0.0

            team.save()

    # Iterate over games played to calculate aggregate team stats
    def calculate_team_stats(self):

        # Get games for selected year
        schs = self.sch_obj.objects.all()

        i = 0 # loop counter
        n = len(schs)

        # Iterate over games
        for sch in schs:
            i += 1 # increment loop counter

            if sch.team_stats_filled:
                self.printProgressBar(i,n,'Calculating Team Stats...')
                continue

            try:
                # Get game stats object corresponding to schedule object
                game_stats = self.game_stats_obj.objects.get(id=sch)
            except: # create game stats object if one doesn't exist
                game_stats = self.game_stats_obj.objects.create(id=sch)

            # Latch onto team objects
            home_team = sch.home_team
            away_team = sch.away_team

            # Set flag if game is first game for either team
            if ( ( home_team.games <= NBA_EARLY_SEASON_CUTOFF ) or ( away_team.games <= NBA_EARLY_SEASON_CUTOFF ) ):
                sch.early_season_game = True

            # Save team statistics for home team going into the game
            game_stats.home_games       = home_team.games
            game_stats.home_wins        = home_team.wins
            game_stats.home_losses      = home_team.losses
            game_stats.home_win_pct     = home_team.win_pct
            game_stats.home_opp_wins    = home_team.opp_wins
            game_stats.home_opp_losses  = home_team.opp_losses
            game_stats.home_opp_win_pct = home_team.opp_win_pct

            game_stats.home_points_pg    = home_team.points_pg
            game_stats.home_fgm_pg       = home_team.fgm_pg
            game_stats.home_fga_pg       = home_team.fga_pg
            game_stats.home_fgp          = home_team.fgp
            game_stats.home_ftm_pg       = home_team.ftm_pg
            game_stats.home_fta_pg       = home_team.fta_pg
            game_stats.home_ftp          = home_team.ftp
            game_stats.home_tpm_pg       = home_team.tpm_pg
            game_stats.home_tpa_pg       = home_team.tpa_pg
            game_stats.home_tpp          = home_team.tpp
            game_stats.home_offReb_pg    = home_team.offReb_pg
            game_stats.home_defReb_pg    = home_team.defReb_pg
            game_stats.home_totReb_pg    = home_team.totReb_pg
            game_stats.home_assists_pg   = home_team.assists_pg
            game_stats.home_pFouls_pg    = home_team.pFouls_pg
            game_stats.home_steals_pg    = home_team.steals_pg
            game_stats.home_turnovers_pg = home_team.turnovers_pg
            game_stats.home_blocks_pg    = home_team.blocks_pg
            game_stats.home_plusMinus_pg = home_team.plusMinus_pg

            game_stats.home_opp_points_pg    = home_team.opp_points_pg
            game_stats.home_opp_fgm_pg       = home_team.opp_fgm_pg
            game_stats.home_opp_fga_pg       = home_team.opp_fga_pg
            game_stats.home_opp_fgp          = home_team.opp_fgp
            game_stats.home_opp_ftm_pg       = home_team.opp_ftm_pg
            game_stats.home_opp_fta_pg       = home_team.opp_fta_pg
            game_stats.home_opp_ftp          = home_team.opp_ftp
            game_stats.home_opp_tpm_pg       = home_team.opp_tpm_pg
            game_stats.home_opp_tpa_pg       = home_team.opp_tpa_pg
            game_stats.home_opp_tpp          = home_team.opp_tpp
            game_stats.home_opp_offReb_pg    = home_team.opp_offReb_pg
            game_stats.home_opp_defReb_pg    = home_team.opp_defReb_pg
            game_stats.home_opp_totReb_pg    = home_team.opp_totReb_pg
            game_stats.home_opp_assists_pg   = home_team.opp_assists_pg
            game_stats.home_opp_pFouls_pg    = home_team.opp_pFouls_pg
            game_stats.home_opp_steals_pg    = home_team.opp_steals_pg
            game_stats.home_opp_turnovers_pg = home_team.opp_turnovers_pg
            game_stats.home_opp_blocks_pg    = home_team.opp_blocks_pg
            game_stats.home_opp_plusMinus_pg = home_team.opp_plusMinus_pg

            # Save team statistics for away team going into the game
            game_stats.away_games       = away_team.games
            game_stats.away_wins        = away_team.wins
            game_stats.away_losses      = away_team.losses
            game_stats.away_win_pct     = away_team.win_pct
            game_stats.away_opp_wins    = away_team.opp_wins
            game_stats.away_opp_losses  = away_team.opp_losses
            game_stats.away_opp_win_pct = away_team.opp_win_pct

            game_stats.away_points_pg    = away_team.points_pg
            game_stats.away_fgm_pg       = away_team.fgm_pg
            game_stats.away_fga_pg       = away_team.fga_pg
            game_stats.away_fgp          = away_team.fgp
            game_stats.away_ftm_pg       = away_team.ftm_pg
            game_stats.away_fta_pg       = away_team.fta_pg
            game_stats.away_ftp          = away_team.ftp
            game_stats.away_tpm_pg       = away_team.tpm_pg
            game_stats.away_tpa_pg       = away_team.tpa_pg
            game_stats.away_tpp          = away_team.tpp
            game_stats.away_offReb_pg    = away_team.offReb_pg
            game_stats.away_defReb_pg    = away_team.defReb_pg
            game_stats.away_totReb_pg    = away_team.totReb_pg
            game_stats.away_assists_pg   = away_team.assists_pg
            game_stats.away_pFouls_pg    = away_team.pFouls_pg
            game_stats.away_steals_pg    = away_team.steals_pg
            game_stats.away_turnovers_pg = away_team.turnovers_pg
            game_stats.away_blocks_pg    = away_team.blocks_pg
            game_stats.away_plusMinus_pg = away_team.plusMinus_pg

            game_stats.away_opp_points_pg    = away_team.opp_points_pg
            game_stats.away_opp_fgm_pg       = away_team.opp_fgm_pg
            game_stats.away_opp_fga_pg       = away_team.opp_fga_pg
            game_stats.away_opp_fgp          = away_team.opp_fgp
            game_stats.away_opp_ftm_pg       = away_team.opp_ftm_pg
            game_stats.away_opp_fta_pg       = away_team.opp_fta_pg
            game_stats.away_opp_ftp          = away_team.opp_ftp
            game_stats.away_opp_tpm_pg       = away_team.opp_tpm_pg
            game_stats.away_opp_tpa_pg       = away_team.opp_tpa_pg
            game_stats.away_opp_tpp          = away_team.opp_tpp
            game_stats.away_opp_offReb_pg    = away_team.opp_offReb_pg
            game_stats.away_opp_defReb_pg    = away_team.opp_defReb_pg
            game_stats.away_opp_totReb_pg    = away_team.opp_totReb_pg
            game_stats.away_opp_assists_pg   = away_team.opp_assists_pg
            game_stats.away_opp_pFouls_pg    = away_team.opp_pFouls_pg
            game_stats.away_opp_steals_pg    = away_team.opp_steals_pg
            game_stats.away_opp_turnovers_pg = away_team.opp_turnovers_pg
            game_stats.away_opp_blocks_pg    = away_team.opp_blocks_pg
            game_stats.away_opp_plusMinus_pg = away_team.opp_plusMinus_pg

            # Include boxscore stats for game in aggregate team stats if game has been played
            if sch.game_stats_filled:
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
                if game_stats.home_points > game_stats.away_points:
                    home_team.wins += 1
                    away_team.losses += 1
                else:
                    home_team.losses += 1
                    away_team.wins += 1
                home_team.win_pct = home_team.wins / home_team.games
                away_team.win_pct = away_team.wins / away_team.games

                # Home team per game stats
                home_team.points_pg = ( ( home_team.points_pg * ( home_team.games - 1 ) ) + game_stats.home_points ) / home_team.games
                
                home_team.fgm_pg    = ( ( home_team.fgm_pg * ( home_team.games - 1 ) ) + game_stats.home_fgm ) / home_team.games
                home_team.fga_pg    = ( ( home_team.fga_pg * ( home_team.games - 1 ) ) + game_stats.home_fga ) / home_team.games
                home_team.fgp       = home_team.fgm_pg / home_team.fga_pg

                home_team.ftm_pg    = ( ( home_team.ftm_pg * ( home_team.games - 1 ) ) + game_stats.home_ftm ) / home_team.games
                home_team.fta_pg    = ( ( home_team.fta_pg * ( home_team.games - 1 ) ) + game_stats.home_fta ) / home_team.games
                home_team.ftp       = home_team.ftm_pg / home_team.fta_pg

                home_team.tpm_pg    = ( ( home_team.tpm_pg * ( home_team.games - 1 ) ) + game_stats.home_tpm ) / home_team.games
                home_team.tpa_pg    = ( ( home_team.tpa_pg * ( home_team.games - 1 ) ) + game_stats.home_tpa ) / home_team.games
                home_team.tpp       = home_team.tpm_pg / home_team.tpa_pg

                home_team.offReb_pg    = ( ( home_team.offReb_pg * ( home_team.games - 1 ) ) + game_stats.home_offReb ) / home_team.games
                home_team.defReb_pg    = ( ( home_team.defReb_pg * ( home_team.games - 1 ) ) + game_stats.home_defReb ) / home_team.games
                home_team.totReb_pg    = ( ( home_team.totReb_pg * ( home_team.games - 1 ) ) + game_stats.home_totReb ) / home_team.games

                home_team.assists_pg   = ( ( home_team.assists_pg   * ( home_team.games - 1 ) ) + game_stats.home_assists   ) / home_team.games
                home_team.pFouls_pg    = ( ( home_team.pFouls_pg    * ( home_team.games - 1 ) ) + game_stats.home_pFouls    ) / home_team.games
                home_team.steals_pg    = ( ( home_team.steals_pg    * ( home_team.games - 1 ) ) + game_stats.home_steals    ) / home_team.games
                home_team.turnovers_pg = ( ( home_team.turnovers_pg * ( home_team.games - 1 ) ) + game_stats.home_turnovers ) / home_team.games
                home_team.blocks_pg    = ( ( home_team.blocks_pg    * ( home_team.games - 1 ) ) + game_stats.home_blocks    ) / home_team.games
                home_team.plusMinus_pg = ( ( home_team.plusMinus_pg * ( home_team.games - 1 ) ) + game_stats.home_plusMinus ) / home_team.games

                # Home team opponents per game stats
                home_team.opp_points_pg = ( ( home_team.opp_points_pg * ( home_team.games - 1 ) ) + game_stats.away_points ) / home_team.games
                
                home_team.opp_fgm_pg    = ( ( home_team.opp_fgm_pg * ( home_team.games - 1 ) ) + game_stats.away_fgm ) / home_team.games
                home_team.opp_fga_pg    = ( ( home_team.opp_fga_pg * ( home_team.games - 1 ) ) + game_stats.away_fga ) / home_team.games
                home_team.opp_fgp       = home_team.opp_fgm_pg / home_team.opp_fga_pg

                home_team.opp_ftm_pg    = ( ( home_team.opp_ftm_pg * ( home_team.games - 1 ) ) + game_stats.away_ftm ) / home_team.games
                home_team.opp_fta_pg    = ( ( home_team.opp_fta_pg * ( home_team.games - 1 ) ) + game_stats.away_fta ) / home_team.games
                home_team.opp_ftp       = home_team.opp_ftm_pg / home_team.opp_fta_pg

                home_team.opp_tpm_pg    = ( ( home_team.opp_tpm_pg * ( home_team.games - 1 ) ) + game_stats.away_tpm ) / home_team.games
                home_team.opp_tpa_pg    = ( ( home_team.opp_tpa_pg * ( home_team.games - 1 ) ) + game_stats.away_tpa ) / home_team.games
                home_team.opp_tpp       = home_team.opp_tpm_pg / home_team.opp_tpa_pg

                home_team.opp_offReb_pg    = ( ( home_team.opp_offReb_pg * ( home_team.games - 1 ) ) + game_stats.away_offReb ) / home_team.games
                home_team.opp_defReb_pg    = ( ( home_team.opp_defReb_pg * ( home_team.games - 1 ) ) + game_stats.away_defReb ) / home_team.games
                home_team.opp_totReb_pg    = ( ( home_team.opp_totReb_pg * ( home_team.games - 1 ) ) + game_stats.away_totReb ) / home_team.games

                home_team.opp_assists_pg   = ( ( home_team.opp_assists_pg   * ( home_team.games - 1 ) ) + game_stats.away_assists   ) / home_team.games
                home_team.opp_pFouls_pg    = ( ( home_team.opp_pFouls_pg    * ( home_team.games - 1 ) ) + game_stats.away_pFouls    ) / home_team.games
                home_team.opp_steals_pg    = ( ( home_team.opp_steals_pg    * ( home_team.games - 1 ) ) + game_stats.away_steals    ) / home_team.games
                home_team.opp_turnovers_pg = ( ( home_team.opp_turnovers_pg * ( home_team.games - 1 ) ) + game_stats.away_turnovers ) / home_team.games
                home_team.opp_blocks_pg    = ( ( home_team.opp_blocks_pg    * ( home_team.games - 1 ) ) + game_stats.away_blocks    ) / home_team.games
                home_team.opp_plusMinus_pg = ( ( home_team.opp_plusMinus_pg * ( home_team.games - 1 ) ) + game_stats.away_plusMinus ) / home_team.games
            
                # Away team per game stats
                away_team.points_pg = ( ( away_team.points_pg * ( away_team.games - 1 ) ) + game_stats.away_points ) / away_team.games
                
                away_team.fgm_pg    = ( ( away_team.fgm_pg * ( away_team.games - 1 ) ) + game_stats.away_fgm ) / away_team.games
                away_team.fga_pg    = ( ( away_team.fga_pg * ( away_team.games - 1 ) ) + game_stats.away_fga ) / away_team.games
                away_team.fgp       = away_team.fgm_pg / away_team.fga_pg

                away_team.ftm_pg    = ( ( away_team.ftm_pg * ( away_team.games - 1 ) ) + game_stats.away_ftm ) / away_team.games
                away_team.fta_pg    = ( ( away_team.fta_pg * ( away_team.games - 1 ) ) + game_stats.away_fta ) / away_team.games
                away_team.ftp       = away_team.ftm_pg / away_team.fta_pg

                away_team.tpm_pg    = ( ( away_team.tpm_pg * ( away_team.games - 1 ) ) + game_stats.away_tpm ) / away_team.games
                away_team.tpa_pg    = ( ( away_team.tpa_pg * ( away_team.games - 1 ) ) + game_stats.away_tpa ) / away_team.games
                away_team.tpp       = away_team.tpm_pg / away_team.tpa_pg

                away_team.offReb_pg    = ( ( away_team.offReb_pg * ( away_team.games - 1 ) ) + game_stats.away_offReb ) / away_team.games
                away_team.defReb_pg    = ( ( away_team.defReb_pg * ( away_team.games - 1 ) ) + game_stats.away_defReb ) / away_team.games
                away_team.totReb_pg    = ( ( away_team.totReb_pg * ( away_team.games - 1 ) ) + game_stats.away_totReb ) / away_team.games

                away_team.assists_pg   = ( ( away_team.assists_pg   * ( away_team.games - 1 ) ) + game_stats.away_assists   ) / away_team.games
                away_team.pFouls_pg    = ( ( away_team.pFouls_pg    * ( away_team.games - 1 ) ) + game_stats.away_pFouls    ) / away_team.games
                away_team.steals_pg    = ( ( away_team.steals_pg    * ( away_team.games - 1 ) ) + game_stats.away_steals    ) / away_team.games
                away_team.turnovers_pg = ( ( away_team.turnovers_pg * ( away_team.games - 1 ) ) + game_stats.away_turnovers ) / away_team.games
                away_team.blocks_pg    = ( ( away_team.blocks_pg    * ( away_team.games - 1 ) ) + game_stats.away_blocks    ) / away_team.games
                away_team.plusMinus_pg = ( ( away_team.plusMinus_pg * ( away_team.games - 1 ) ) + game_stats.away_plusMinus ) / away_team.games

                # Away team opponents per game stats
                away_team.opp_points_pg = ( ( away_team.opp_points_pg * ( away_team.games - 1 ) ) + game_stats.home_points ) / away_team.games
                
                away_team.opp_fgm_pg    = ( ( away_team.opp_fgm_pg * ( away_team.games - 1 ) ) + game_stats.home_fgm ) / away_team.games
                away_team.opp_fga_pg    = ( ( away_team.opp_fga_pg * ( away_team.games - 1 ) ) + game_stats.home_fga ) / away_team.games
                away_team.opp_fgp       = away_team.opp_fgm_pg / away_team.opp_fga_pg

                away_team.opp_ftm_pg    = ( ( away_team.opp_ftm_pg * ( away_team.games - 1 ) ) + game_stats.home_ftm ) / away_team.games
                away_team.opp_fta_pg    = ( ( away_team.opp_fta_pg * ( away_team.games - 1 ) ) + game_stats.home_fta ) / away_team.games
                away_team.opp_ftp       = away_team.opp_ftm_pg / away_team.opp_fta_pg

                away_team.opp_tpm_pg    = ( ( away_team.opp_tpm_pg * ( away_team.games - 1 ) ) + game_stats.home_tpm ) / away_team.games
                away_team.opp_tpa_pg    = ( ( away_team.opp_tpa_pg * ( away_team.games - 1 ) ) + game_stats.home_tpa ) / away_team.games
                away_team.opp_tpp       = away_team.opp_tpm_pg / away_team.opp_tpa_pg

                away_team.opp_offReb_pg    = ( ( away_team.opp_offReb_pg * ( away_team.games - 1 ) ) + game_stats.home_offReb ) / away_team.games
                away_team.opp_defReb_pg    = ( ( away_team.opp_defReb_pg * ( away_team.games - 1 ) ) + game_stats.home_defReb ) / away_team.games
                away_team.opp_totReb_pg    = ( ( away_team.opp_totReb_pg * ( away_team.games - 1 ) ) + game_stats.home_totReb ) / away_team.games

                away_team.opp_assists_pg   = ( ( away_team.opp_assists_pg   * ( away_team.games - 1 ) ) + game_stats.home_assists   ) / away_team.games
                away_team.opp_pFouls_pg    = ( ( away_team.opp_pFouls_pg    * ( away_team.games - 1 ) ) + game_stats.home_pFouls    ) / away_team.games
                away_team.opp_steals_pg    = ( ( away_team.opp_steals_pg    * ( away_team.games - 1 ) ) + game_stats.home_steals    ) / away_team.games
                away_team.opp_turnovers_pg = ( ( away_team.opp_turnovers_pg * ( away_team.games - 1 ) ) + game_stats.home_turnovers ) / away_team.games
                away_team.opp_blocks_pg    = ( ( away_team.opp_blocks_pg    * ( away_team.games - 1 ) ) + game_stats.home_blocks    ) / away_team.games
                away_team.opp_plusMinus_pg = ( ( away_team.opp_plusMinus_pg * ( away_team.games - 1 ) ) + game_stats.home_plusMinus ) / away_team.games

                sch.team_stats_filled = True

            # Save game, home, and away teams
            home_team.save()
            away_team.save()
            sch.save()
            game_stats.save()
            self.printProgressBar(i,n,'Calculating Team Stats...')

    # Set team rankings for each team stat recorded
    def set_rankings(self):

        # Iterate over all stats in database
        for stat in NBA_TEAM_DB_STATS_FIELDS_LIST:

            # Get stat and ranking field names
            if stat in NBA_REVERSE_FIELDS_LIST:
                stat_name = str(stat)
            else:
                stat_name = "-" + str(stat) # "-" included to specify descending order
            
            
            stat_rank = "rank_" + str(stat)

            # Query database filtering by specified stat
            sorted_db = self.teams_obj.objects.all().order_by(stat_name)

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

        # Save individual years to csv
        for year in years:

            # Set csv name
            csv_filename = f"{NBA_DATA_PATH}nba_training_data_{year}.csv"

            with open(csv_filename, 'w') as f:

                # Create writer object
                writer = csv.writer(f)

                # Get game stats object for specific year
                game_stats_obj = self.get_game_stats_obj(year)

                # Loop over field names in game stats object to write as column headers
                field_names = [field.name for field in game_stats_obj._meta.get_fields()]
                writer.writerow(field_names)

                # Iterate over games and write stats to csv
                game_stats_all = game_stats_obj.objects.all()
                for game_stats in game_stats_all:
                    writer.writerow([getattr(game_stats, field) for field in field_names])

        # Set filename to save all stats to
        csv_filename = f"{NBA_DATA_PATH}nba_training_data_{years[0]}_to_{years[-1]}.csv"

        # Open file
        with open(csv_filename,'w') as f:
            
            # Create writer object
            writer = csv.writer(f)

            # Get temporary game_stats object to save field names
            game_stats_obj_temp = self.get_game_stats_obj(years[0])
            
            # Loop over field names in schedule object to write as column headers
            field_names = [field.name for field in game_stats_obj_temp._meta.get_fields()]
            writer.writerow(field_names)

            # Iterate over years specified
            for year in years:

                # Get all games in year
                game_stats_obj = self.get_game_stats_obj(year)
                game_stats_all = game_stats_obj.objects.all()

                # Iterate over games and write every stat to csv
                for game_stats in game_stats_all:
                    writer.writerow([getattr(game_stats, field) for field in field_names])

    # Clear NBA predictions
    def clear_predictions(self):
        self.pred_obj.objects.all().delete()

    # Calculate predictions for each model   
    def calculate_predictions(self):

        # Get games for selected year
        schs = self.sch_obj.objects.all()

        i = 0 # loop counter
        n = len(schs)

        # Iterate over games
        for sch in schs:
            i += 1 # increment loop counter

            if sch.early_season_game:
                continue

            # Get corresponding game stats object
            game_stats = self.game_stats_obj.objects.get(id=sch.id)

            try:
                # Grab predictions object corresponding to this game
                pred = self.pred_obj.objects.get(id=sch.id)
            except:
                pred = self.pred_obj.objects.create(id=sch)

            # Generate predictions
            pred.home_points_lr, pred.away_points_lr = self.models['Linear Regression'].predict_game(game_stats)
            pred.home_points_pr, pred.away_points_pr = self.models['Polynomial Regression'].predict_game(game_stats)
            pred.home_points_eln, pred.away_points_eln = self.models['Elastic Net Regression'].predict_game(game_stats)

            # Copy in vegas predictions
            if sch.game_stats_filled and sch.team_stats_filled:
                try:
                    odds = self.odds_obj.objects.get(date=sch.date,
                                                     home_team=sch.home_team,
                                                     away_team=sch.away_team)
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
        schs = self.sch_obj.objects.all()

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

        home_diff_pr_tot_err = 0
        away_diff_pr_tot_err = 0
        home_points_pr_cum_me = 0
        away_points_pr_cum_me = 0

        home_diff_pr_sqr_err = 0
        away_diff_pr_sqr_err = 0
        home_points_pr_cum_rmse = 0
        away_points_pr_cum_rmse = 0

        home_diff_eln_tot_err = 0
        away_diff_eln_tot_err = 0
        home_points_eln_cum_me = 0
        away_points_eln_cum_me = 0

        home_diff_eln_sqr_err = 0
        away_diff_eln_sqr_err = 0
        home_points_eln_cum_rmse = 0
        away_points_eln_cum_rmse = 0

        i = 0 # loop counter
        n = len(schs)

        # Iterate over games
        for sch in schs:
            i += 1 # increment loop counter

            # No predictions made on early season games
            if sch.early_season_game:
                continue

            # Grab game stats and predictions object corresponding to this game
            game_stats = self.game_stats_obj.objects.get(id=sch.id)
            pred = self.pred_obj.objects.get(id=sch.id)

            # Calculate RMSE if stats are filled
            if sch.game_stats_filled and sch.team_stats_filled:
                if pred.home_points_vegas > 0 and pred.away_points_vegas > 0:
                    home_diff_vegas_tot_err += game_stats.home_points - pred.home_points_vegas
                    away_diff_vegas_tot_err += game_stats.away_points - pred.away_points_vegas
                    home_points_vegas_cum_me = home_diff_vegas_tot_err / i
                    away_points_vegas_cum_me = away_diff_vegas_tot_err / i
                    
                    home_diff_vegas_sqr_err += (game_stats.home_points - pred.home_points_vegas) ** 2
                    away_diff_vegas_sqr_err += (game_stats.away_points - pred.away_points_vegas) ** 2
                    home_points_vegas_cum_rmse = sqrt(home_diff_vegas_sqr_err / i)
                    away_points_vegas_cum_rmse = sqrt(away_diff_vegas_sqr_err / i)    

                home_diff_lr_tot_err += game_stats.home_points - pred.home_points_lr
                away_diff_lr_tot_err += game_stats.away_points - pred.away_points_lr
                home_points_lr_cum_me = home_diff_lr_tot_err / i
                away_points_lr_cum_me = away_diff_lr_tot_err / i

                home_diff_lr_sqr_err += (game_stats.home_points - pred.home_points_lr) ** 2
                away_diff_lr_sqr_err += (game_stats.away_points - pred.away_points_lr) ** 2
                home_points_lr_cum_rmse = sqrt(home_diff_lr_sqr_err / i)
                away_points_lr_cum_rmse = sqrt(away_diff_lr_sqr_err / i)

                home_diff_pr_tot_err += game_stats.home_points - pred.home_points_pr
                away_diff_pr_tot_err += game_stats.away_points - pred.away_points_pr
                home_points_pr_cum_me = home_diff_pr_tot_err / i
                away_points_pr_cum_me = away_diff_pr_tot_err / i

                home_diff_pr_sqr_err += (game_stats.home_points - pred.home_points_pr) ** 2
                away_diff_pr_sqr_err += (game_stats.away_points - pred.away_points_pr) ** 2
                home_points_pr_cum_rmse = sqrt(home_diff_pr_sqr_err / i)
                away_points_pr_cum_rmse = sqrt(away_diff_pr_sqr_err / i)

                home_diff_eln_tot_err += game_stats.home_points - pred.home_points_eln
                away_diff_eln_tot_err += game_stats.away_points - pred.away_points_eln
                home_points_eln_cum_me = home_diff_eln_tot_err / i
                away_points_eln_cum_me = away_diff_eln_tot_err / i

                home_diff_eln_sqr_err += (game_stats.home_points - pred.home_points_eln) ** 2
                away_diff_eln_sqr_err += (game_stats.away_points - pred.away_points_eln) ** 2
                home_points_eln_cum_rmse = sqrt(home_diff_eln_sqr_err / i)
                away_points_eln_cum_rmse = sqrt(away_diff_eln_sqr_err / i)

            # Save predictions to database
            pred.home_points_vegas_cum_me = home_points_vegas_cum_me
            pred.away_points_vegas_cum_me = away_points_vegas_cum_me
            pred.home_points_lr_cum_me    = home_points_lr_cum_me
            pred.away_points_lr_cum_me    = away_points_lr_cum_me
            pred.home_points_pr_cum_me    = home_points_pr_cum_me
            pred.away_points_pr_cum_me    = away_points_pr_cum_me
            pred.home_points_eln_cum_me   = home_points_eln_cum_me
            pred.away_points_eln_cum_me   = away_points_eln_cum_me
            
            pred.home_points_vegas_cum_rmse = home_points_vegas_cum_rmse
            pred.away_points_vegas_cum_rmse = away_points_vegas_cum_rmse
            pred.home_points_lr_cum_rmse    = home_points_lr_cum_rmse
            pred.away_points_lr_cum_rmse    = away_points_lr_cum_rmse
            pred.home_points_pr_cum_rmse    = home_points_pr_cum_rmse
            pred.away_points_pr_cum_rmse    = away_points_pr_cum_rmse
            pred.home_points_eln_cum_rmse   = home_points_eln_cum_rmse
            pred.away_points_eln_cum_rmse   = away_points_eln_cum_rmse
            
            pred.save()

            # Print progress bar
            self.printProgressBar(i, n, 'Calculating model error...')

    # Calculate predictions for a single game
    # @param[in]    model             model selected to perform predictions
    # @param[in]    home_team_name    name of home team
    # @param[in]    away_team_name    name of away team
    # @param[out]   home_points       predicted points to be scored by home team
    # @param[out]   away_points       predicted points to be scored by away team
    def predict_single_game(self, model, home_team_name, away_team_name):
        game = {}

        # Grab home team stats
        home_team_sp = home_team_name.split(' ')
        if home_team_sp[-1] in NBA_TEAMS_DICT:
            home_team = self.teams_obj.objects.get(name=home_team_sp[-1])
        else:
            home_team = self.teams_obj.objects.get(name=home_team_sp[-2:])
        home_team_dict = home_team.__dict__

        # Save home team stats in game dictionary
        for k,v in home_team_dict.items():
            col = "home_" + str(k)
            game[col] = v

        # Grab away team stats
        away_team_sp = away_team_name.split(' ')
        if away_team_sp[-1] in NBA_TEAMS_DICT:
            away_team = self.teams_obj.objects.get(name=away_team_sp[-1])
        else:
            away_team = self.teams_obj.objects.get(name=away_team_sp[-2:])
        away_team_dict = away_team.__dict__

        # Save away team stats in game dictionary
        for k,v in away_team_dict.items():
            col = "away_" + str(k)
            game[col] = v

        # Run predict ML method and return preditions
        return self.models[model].predict_game(game)

    # Get the predictions for games scheduled on a specified date
    # @param[in]    day     day to retreive games for
    # @param[out]   preds   predictions for each game on specified date
    def get_preds(self, day):
        games = self.get_games(day)
        id_list = [game.id for game in games]
        preds = self.pred_obj.objects.filter(pk__in=id_list)
        return preds

    # Clear NBA odds
    def clear_game_odds(self):
        self.odds_obj.objects.all().delete()

    # Use API call to download game odds for each game in current season
    def download_game_odds(self):

        # Get current schedule object
        schs = self.sch_obj.objects.all()

        # Get list of unique dates that games were played on
        dates = []
        for sch in schs:
            #sch.game_odds_filled = 0
            if sch.game_stats_filled and sch.team_stats_filled and not sch.game_odds_filled:
                dates.append(sch.date)
        n_games_sch = len(dates)
        dates_set = set(dates)
        unique_dates = (list(dates_set))
        unique_dates.sort(key=lambda date: date)

        # Iterate over dates to send in API call
        i = 0
        j = 0
        n = len(unique_dates)

        empty_games = []

        for date in unique_dates:
            i += 1

            odds_str = request_nba_game_odds(str(date))
            odds_json = json.loads(odds_str)
            
            # f = open("test_game_odds.json")
            # odds_json = json.load(f)

            # Iterate over games in response
            data = odds_json['data']
            for game in data:

                # Save game info
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
                except: # handling for when bookmakers comes back empty
                    empty_games.append(game_id)
                    continue
                
                # Save odds object to database if it hasn't been already
                try:
                    self.odds_obj.objects.get(id=game_id)
                except:
                    game_home_team = self.teams_obj.objects.get(full_name=game_home_team_full_name)
                    game_away_team = self.teams_obj.objects.get(full_name=game_away_team_full_name)
                    self.odds_obj.objects.create(id=game_id,
                                                 date=game_date,
                                                 home_team=game_home_team,
                                                 away_team=game_away_team,
                                                 home_spread=game_home_spread,
                                                 away_spread=game_away_spread,
                                                 total=game_total)
                    try:
                        sch = self.sch_obj.objects.get(date=game_date,
                                                       home_team=game_home_team,
                                                       away_team=game_away_team)
                        sch.game_odds_filled = 1
                        sch.save()
                    except:
                        j += 1
                        print(f"{j}: {game_away_team} @ {game_home_team} on {game_date} not found in schedule...")

            # Print completion message
            self.printProgressBar(i,n,'Loading Odds to Database...')

            time.sleep(0.5)

        # Print status report of how many game odds were downloaded
        # Some are usually missing
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

    # 
    def set_best_fit_rankings(self):
        teams = self.teams_obj.objects.all()
        n_teams = len(teams)
        games = self.sch_obj.objects.filter(game_stats_filled=1)
        n_games = len(games)
        
        m_rows = n_teams + 1
        m_cols = n_games
        M = np.zeros((m_rows, m_cols))

        s_cols = n_games
        S = np.zeros(s_cols)

        for col,game in enumerate(games):
            game_stat_obj = self.game_stats_obj.objects.get(id=game.id)
            home_team      = game.home_team.alpha_id
            away_team      = game.away_team.alpha_id
            home_points    = game_stat_obj.home_points
            away_points    = game_stat_obj.away_points

            M[0,col]         = 1.0
            M[home_team,col] = 1.0
            M[away_team,col] = -1.0
            S[col]           = home_points - away_points

        init_W = np.array([2.0] + [0.0]*n_teams)

        def errorfn(w,m,s):
            return w.dot(m) - s

        W = scipy.optimize.leastsq(errorfn, init_W, args=(M,S))

        self.home_adv = W[0][0]
        team_ratings = W[0][1:]

        for idx,team in enumerate(self.teams_list):
            team_obj = self.teams_obj.objects.get(alpha_id=(idx+1))
            team_obj.best_fit_rating = team_ratings[idx]
            team_obj.save()
        
        # Query database filtering by specified stat
        sorted_db = self.teams_obj.objects.all().order_by("-best_fit_rating")

        ratings_sum = 0

        # Iterate over queryset
        for idx,team in enumerate(sorted_db):
            
            ratings_sum += team.best_fit_rating

            team.best_fit_rank = idx + 1
           
            # Save team object to database
            team.save()

        mean_rating = ratings_sum / n_teams

        for idx,team in enumerate(sorted_db):
            
            team.best_fit_rating = team.best_fit_rating - mean_rating
           
            # Save team object to database
            team.save()
        
        print("Home court advantage:",round(self.home_adv,2))

    def get_best_fit_ratings(self):
        teams = self.teams_obj.objects.all().order_by("best_fit_rank")
        ratings = {
            'ranking' : [],
            'team' : [],
            'rating' : [],
            'string' : [],
        }

        for team in teams:
            ratings['ranking'].append(team.best_fit_rank)
            ratings['team'].append(team.full_name)
            ratings['rating'].append(team.best_fit_rating)
            ratings['string'].append(team.full_name.replace(' ','_'))

        return ratings



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

import pickle
import pandas as pd
import os
from SportsApp.models import NBAPredictions2022, NBASchedule2022
import matplotlib.pyplot as plt
from SportsApp.constants import PLOT_PATH

class NBALinReg:
    def __init__(self):
        self.home_filename   = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/ml_models/nba_lin_reg_home_points.sav"
        self.away_filename   = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/ml_models/nba_lin_reg_away_points.sav"
        self.scaler_filename = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/ml_models/nba_scaler.sav"

        self.home_lin_reg = pickle.load(open(self.home_filename, 'rb'))
        self.away_lin_reg = pickle.load(open(self.away_filename, 'rb'))
        self.scaler       = pickle.load(open(self.scaler_filename,  'rb'))

        self.predictor_list = [
            'home_opp_win_pct', 'home_fgm_pg', 'home_fga_pg', 'home_fgp',
            'home_ftm_pg', 'home_ftp', 'home_tpm_pg', 'home_tpp', 'home_offReb_pg',
            'home_defReb_pg', 'home_assists_pg', 'home_steals_pg',
            'home_turnovers_pg', 'home_blocks_pg', 'home_plusMinus_pg',
            'home_opp_fgm_pg', 'home_opp_fga_pg', 'home_opp_fgp', 'home_opp_ftm_pg',
            'home_opp_ftp', 'home_opp_tpm_pg', 'home_opp_tpp', 'home_opp_offReb_pg',
            'home_opp_defReb_pg', 'home_opp_assists_pg', 'home_opp_pFouls_pg',
            'home_opp_steals_pg', 'home_opp_turnovers_pg', 'home_opp_blocks_pg',
            'away_opp_win_pct', 'away_fgm_pg', 'away_fga_pg', 'away_fgp',
            'away_ftm_pg', 'away_ftp', 'away_tpm_pg', 'away_tpp', 'away_offReb_pg',
            'away_defReb_pg', 'away_assists_pg', 'away_steals_pg',
            'away_turnovers_pg', 'away_blocks_pg', 'away_plusMinus_pg',
            'away_opp_fgm_pg', 'away_opp_fga_pg', 'away_opp_fgp', 'away_opp_ftm_pg',
            'away_opp_ftp', 'away_opp_tpm_pg', 'away_opp_tpp', 'away_opp_offReb_pg',
            'away_opp_defReb_pg', 'away_opp_assists_pg', 'away_opp_pFouls_pg',
            'away_opp_steals_pg', 'away_opp_turnovers_pg', 'away_opp_blocks_pg'
        ]

    def __str__(self):
        return "NBA Linear Regression Model"

    # Standard game prediction method
    # @param[in]    game         game stats used to generate predictions
    # @param[out]   home_score   predicted score of home team
    # @param[out]   away_score   predicted score of away_team
    def predict_game(self, game):

        # Save game as dictionary
        if type(game) is not dict:
            game_dict = game.__dict__
        else:
            game_dict = game

        # Convert game dictionary to dataframe
        game_df = pd.DataFrame(data=game_dict, index=[0])

        # Drop unnecessary columns
        for col in game_df.columns:
            if col not in self.predictor_list:
                game_df = game_df.drop(columns=[col])

        # Scale relevant game data
        game_scaled = self.scaler.transform(game_df)

        # Generate predictions for home and away team scores
        home_score = round(float(self.home_lin_reg.predict(game_scaled)),1)
        away_score = round(float(self.away_lin_reg.predict(game_scaled)),1)

        return home_score, away_score

    def plot_rmse(self):
        schs = NBASchedule2022.objects.all()

        home_rmse = []
        away_rmse = []
        home_vegas_rmse = []
        away_vegas_rmse = []

        for sch in schs:
            if sch.game_stats_filled and sch.team_stats_filled and sch.game_odds_filled and not sch.early_season_game:
                game_pred = NBAPredictions2022.objects.get(id=sch.id)
                home_rmse.append(game_pred.home_points_lr_cum_rmse)
                away_rmse.append(game_pred.away_points_lr_cum_rmse)
                home_vegas_rmse.append(game_pred.home_points_vegas_cum_rmse)
                away_vegas_rmse.append(game_pred.away_points_vegas_cum_rmse)

        idx = [i for i in range(1, len(home_rmse) + 1)]

        plt.figure(figsize=(7,4))
        plt.style.use('dark_background')
        plt.plot(idx, home_rmse, 'dodgerblue')
        plt.plot(idx, away_rmse, 'tab:orange')
        plt.plot(idx, home_vegas_rmse, 'blue')
        plt.plot(idx, away_vegas_rmse, 'red')
        plt.title('NBA Linear Regression Root Mean Squared Error')
        plt.xlabel('Number of Games Predicted')
        plt.ylabel("RMSE")
        plt.legend(labels=["Home Score Prediction", "Away Score Prediction", "Home Score Baseline", "Away Score Baseline"], bbox_to_anchor=(1.42, 0.5), loc='center right')
        plt.grid(True)
        save_name = PLOT_PATH + "nba_lin_reg_rmse.png"
        plt.savefig(save_name, bbox_inches='tight')
        plt.show(block=False)

    def plot_me(self):
        schs = NBASchedule2022.objects.all()

        home_me = []
        away_me = []
        home_vegas_me = []
        away_vegas_me = []

        for sch in schs:
            if sch.game_stats_filled and sch.team_stats_filled and sch.game_odds_filled and not sch.early_season_game:
                game_pred = NBAPredictions2022.objects.get(id=sch.id)
                home_me.append(game_pred.home_points_lr_cum_me)
                away_me.append(game_pred.away_points_lr_cum_me)
                home_vegas_me.append(game_pred.home_points_vegas_cum_me)
                away_vegas_me.append(game_pred.away_points_vegas_cum_me)

        idx = [i for i in range(1, len(home_me) + 1)]

        plt.figure(figsize=(7,4))
        plt.style.use('dark_background')
        plt.plot(idx, home_me, 'dodgerblue')
        plt.plot(idx, away_me, 'tab:orange')
        plt.plot(idx, home_vegas_me, 'blue')
        plt.plot(idx, away_vegas_me, 'red')
        plt.title('NBA Linear Regression Mean Error')
        plt.xlabel('Number of Games Predicted')
        plt.ylabel("Mean Error")
        plt.legend(labels=["Home Score Prediction", "Away Score Prediction", "Home Score Baseline", "Away Score Baseline"], bbox_to_anchor=(1.42, 0.5), loc='center right')
        plt.grid(True)
        save_name = PLOT_PATH + "nba_lin_reg_me.png"
        plt.savefig(save_name, bbox_inches='tight')
        plt.show(block=False)



class NBAPolyReg:
    def __init__(self):
        self.home_filename   = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/ml_models/nba_poly_reg_home_points.sav"
        self.away_filename   = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/ml_models/nba_poly_reg_away_points.sav"
        self.scaler_filename = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/ml_models/nba_scaler.sav"

        self.home_poly_reg = pickle.load(open(self.home_filename, 'rb'))
        self.away_poly_reg = pickle.load(open(self.away_filename, 'rb'))
        self.scaler       = pickle.load(open(self.scaler_filename,  'rb'))

        self.predictor_list = [
            'home_opp_win_pct', 'home_fgm_pg', 'home_fga_pg', 'home_fgp',
            'home_ftm_pg', 'home_ftp', 'home_tpm_pg', 'home_tpp', 'home_offReb_pg',
            'home_defReb_pg', 'home_assists_pg', 'home_steals_pg',
            'home_turnovers_pg', 'home_blocks_pg', 'home_plusMinus_pg',
            'home_opp_fgm_pg', 'home_opp_fga_pg', 'home_opp_fgp', 'home_opp_ftm_pg',
            'home_opp_ftp', 'home_opp_tpm_pg', 'home_opp_tpp', 'home_opp_offReb_pg',
            'home_opp_defReb_pg', 'home_opp_assists_pg', 'home_opp_pFouls_pg',
            'home_opp_steals_pg', 'home_opp_turnovers_pg', 'home_opp_blocks_pg',
            'away_opp_win_pct', 'away_fgm_pg', 'away_fga_pg', 'away_fgp',
            'away_ftm_pg', 'away_ftp', 'away_tpm_pg', 'away_tpp', 'away_offReb_pg',
            'away_defReb_pg', 'away_assists_pg', 'away_steals_pg',
            'away_turnovers_pg', 'away_blocks_pg', 'away_plusMinus_pg',
            'away_opp_fgm_pg', 'away_opp_fga_pg', 'away_opp_fgp', 'away_opp_ftm_pg',
            'away_opp_ftp', 'away_opp_tpm_pg', 'away_opp_tpp', 'away_opp_offReb_pg',
            'away_opp_defReb_pg', 'away_opp_assists_pg', 'away_opp_pFouls_pg',
            'away_opp_steals_pg', 'away_opp_turnovers_pg', 'away_opp_blocks_pg'
        ]

    def __str__(self):
        return "NBA Linear Regression Model"

    # Standard game prediction method
    # @param[in]    game         game stats used to generate predictions
    # @param[out]   home_score   predicted score of home team
    # @param[out]   away_score   predicted score of away_team
    def predict_game(self, game):

        # Save game as dictionary
        if type(game) is not dict:
            game_dict = game.__dict__
        else:
            game_dict = game

        # Convert game dictionary to dataframe
        game_df = pd.DataFrame(data=game_dict, index=[0])

        # Drop unnecessary columns
        for col in game_df.columns:
            if col not in self.predictor_list:
                game_df = game_df.drop(columns=[col])

        # Scale relevant game data
        game_scaled = self.scaler.transform(game_df)

        # Generate predictions for home and away team scores
        home_score = round(float(self.home_poly_reg.predict(game_scaled)),1)
        away_score = round(float(self.away_poly_reg.predict(game_scaled)),1)

        return home_score, away_score

    def plot_rmse(self):
        schs = NBASchedule2022.objects.all()

        home_rmse = []
        away_rmse = []
        home_vegas_rmse = []
        away_vegas_rmse = []

        for sch in schs:
            if sch.game_stats_filled and sch.team_stats_filled and sch.game_odds_filled and not sch.early_season_game:
                game_pred = NBAPredictions2022.objects.get(id=sch.id)
                home_rmse.append(game_pred.home_points_pr_cum_rmse)
                away_rmse.append(game_pred.away_points_pr_cum_rmse)
                home_vegas_rmse.append(game_pred.home_points_vegas_cum_rmse)
                away_vegas_rmse.append(game_pred.away_points_vegas_cum_rmse)

        idx = [i for i in range(1, len(home_rmse) + 1)]

        plt.figure(figsize=(7,4))
        plt.style.use('dark_background')
        plt.plot(idx, home_rmse, 'dodgerblue')
        plt.plot(idx, away_rmse, 'tab:orange')
        plt.plot(idx, home_vegas_rmse, 'blue')
        plt.plot(idx, away_vegas_rmse, 'red')
        plt.title('NBA Linear Regression Root Mean Squared Error')
        plt.xlabel('Number of Games Predicted')
        plt.ylabel("RMSE")
        plt.legend(labels=["Home Score Prediction", "Away Score Prediction", "Home Score Baseline", "Away Score Baseline"], bbox_to_anchor=(1.42, 0.5), loc='center right')
        plt.grid(True)
        save_name = PLOT_PATH + "nba_poly_reg_rmse.png"
        plt.savefig(save_name, bbox_inches='tight')
        plt.show(block=False)

    def plot_me(self):
        schs = NBASchedule2022.objects.all()

        home_me = []
        away_me = []
        home_vegas_me = []
        away_vegas_me = []

        for sch in schs:
            if sch.game_stats_filled and sch.team_stats_filled and sch.game_odds_filled and not sch.early_season_game:
                game_pred = NBAPredictions2022.objects.get(id=sch.id)
                home_me.append(game_pred.home_points_pr_cum_me)
                away_me.append(game_pred.away_points_pr_cum_me)
                home_vegas_me.append(game_pred.home_points_vegas_cum_me)
                away_vegas_me.append(game_pred.away_points_vegas_cum_me)

        idx = [i for i in range(1, len(home_me) + 1)]

        plt.figure(figsize=(7,4))
        plt.style.use('dark_background')
        plt.plot(idx, home_me, 'dodgerblue')
        plt.plot(idx, away_me, 'tab:orange')
        plt.plot(idx, home_vegas_me, 'blue')
        plt.plot(idx, away_vegas_me, 'red')
        plt.title('NBA Linear Regression Mean Error')
        plt.xlabel('Number of Games Predicted')
        plt.ylabel("Mean Error")
        plt.legend(labels=["Home Score Prediction", "Away Score Prediction", "Home Score Baseline", "Away Score Baseline"], bbox_to_anchor=(1.42, 0.5), loc='center right')
        plt.grid(True)
        save_name = PLOT_PATH + "nba_poly_reg_me.png"
        plt.savefig(save_name, bbox_inches='tight')
        plt.show(block=False)
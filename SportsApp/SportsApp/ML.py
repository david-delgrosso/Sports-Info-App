import pickle
import pandas as pd
import os

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

    def predict_game(self, game):
        game_dict = game.__dict__
        game_df = pd.DataFrame(data=game_dict, index=[0])

        for col in game_df.columns:
            if col not in self.predictor_list:
                game_df = game_df.drop(columns=[col])

        game_scaled = self.scaler.transform(game_df)

        home_score = round(float(self.home_lin_reg.predict(game_scaled)),1)
        away_score = round(float(self.away_lin_reg.predict(game_scaled)),1)

        return home_score, away_score
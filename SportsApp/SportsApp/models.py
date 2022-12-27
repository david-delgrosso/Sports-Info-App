from django.db import models

class NBATeam(models.Model):
    id        = models.IntegerField(primary_key=True)
    name      = models.CharField(max_length=30)
    city      = models.CharField(max_length=30)
    full_name = models.CharField(max_length=40)
        
    games       = models.IntegerField(default=0)
    wins        = models.IntegerField(default=0)
    losses      = models.IntegerField(default=0)
    win_pct     = models.FloatField(default=0.0)
    opp_wins    = models.IntegerField(default=0)
    opp_losses  = models.IntegerField(default=0)
    opp_win_pct = models.FloatField(default=0.0)

    points_pg    = models.FloatField(default=0.0)
    fgm_pg       = models.FloatField(default=0.0)
    fga_pg       = models.FloatField(default=0.0)
    fgp          = models.FloatField(default=0.0)
    ftm_pg       = models.FloatField(default=0.0)
    fta_pg       = models.FloatField(default=0.0)
    ftp          = models.FloatField(default=0.0)
    tpm_pg       = models.FloatField(default=0.0)
    tpa_pg       = models.FloatField(default=0.0)
    tpp          = models.FloatField(default=0.0)
    offReb_pg    = models.FloatField(default=0.0)
    defReb_pg    = models.FloatField(default=0.0)
    totReb_pg    = models.FloatField(default=0.0)
    assists_pg   = models.FloatField(default=0.0)
    pFouls_pg    = models.FloatField(default=0.0)
    steals_pg    = models.FloatField(default=0.0)
    turnovers_pg = models.FloatField(default=0.0)
    blocks_pg    = models.FloatField(default=0.0)
    plusMinus_pg = models.FloatField(default=0.0)

    opp_points_pg    = models.FloatField(default=0.0)
    opp_fgm_pg       = models.FloatField(default=0.0)
    opp_fga_pg       = models.FloatField(default=0.0)
    opp_fgp          = models.FloatField(default=0.0)
    opp_ftm_pg       = models.FloatField(default=0.0)
    opp_fta_pg       = models.FloatField(default=0.0)
    opp_ftp          = models.FloatField(default=0.0)
    opp_tpm_pg       = models.FloatField(default=0.0)
    opp_tpa_pg       = models.FloatField(default=0.0)
    opp_tpp          = models.FloatField(default=0.0)
    opp_offReb_pg    = models.FloatField(default=0.0)
    opp_defReb_pg    = models.FloatField(default=0.0)
    opp_totReb_pg    = models.FloatField(default=0.0)
    opp_assists_pg   = models.FloatField(default=0.0)
    opp_pFouls_pg    = models.FloatField(default=0.0)
    opp_steals_pg    = models.FloatField(default=0.0)
    opp_turnovers_pg = models.FloatField(default=0.0)
    opp_blocks_pg    = models.FloatField(default=0.0)
    opp_plusMinus_pg = models.FloatField(default=0.0)

    rank_points_pg    = models.IntegerField(default=0.0)
    rank_fgm_pg       = models.IntegerField(default=0.0)
    rank_fga_pg       = models.IntegerField(default=0.0)
    rank_fgp          = models.IntegerField(default=0.0)
    rank_ftm_pg       = models.IntegerField(default=0.0)
    rank_fta_pg       = models.IntegerField(default=0.0)
    rank_ftp          = models.IntegerField(default=0.0)
    rank_tpm_pg       = models.IntegerField(default=0.0)
    rank_tpa_pg       = models.IntegerField(default=0.0)
    rank_tpp          = models.IntegerField(default=0.0)
    rank_offReb_pg    = models.IntegerField(default=0.0)
    rank_defReb_pg    = models.IntegerField(default=0.0)
    rank_totReb_pg    = models.IntegerField(default=0.0)
    rank_assists_pg   = models.IntegerField(default=0.0)
    rank_pFouls_pg    = models.IntegerField(default=0.0)
    rank_steals_pg    = models.IntegerField(default=0.0)
    rank_turnovers_pg = models.IntegerField(default=0.0)
    rank_blocks_pg    = models.IntegerField(default=0.0)
    rank_plusMinus_pg = models.IntegerField(default=0.0)

    rank_opp_points_pg    = models.IntegerField(default=0.0)
    rank_opp_fgm_pg       = models.IntegerField(default=0.0)
    rank_opp_fga_pg       = models.IntegerField(default=0.0)
    rank_opp_fgp          = models.IntegerField(default=0.0)
    rank_opp_ftm_pg       = models.IntegerField(default=0.0)
    rank_opp_fta_pg       = models.IntegerField(default=0.0)
    rank_opp_ftp          = models.IntegerField(default=0.0)
    rank_opp_tpm_pg       = models.IntegerField(default=0.0)
    rank_opp_tpa_pg       = models.IntegerField(default=0.0)
    rank_opp_tpp          = models.IntegerField(default=0.0)
    rank_opp_offReb_pg    = models.IntegerField(default=0.0)
    rank_opp_defReb_pg    = models.IntegerField(default=0.0)
    rank_opp_totReb_pg    = models.IntegerField(default=0.0)
    rank_opp_assists_pg   = models.IntegerField(default=0.0)
    rank_opp_pFouls_pg    = models.IntegerField(default=0.0)
    rank_opp_steals_pg    = models.IntegerField(default=0.0)
    rank_opp_turnovers_pg = models.IntegerField(default=0.0)
    rank_opp_blocks_pg    = models.IntegerField(default=0.0)
    rank_opp_plusMinus_pg = models.IntegerField(default=0.0)

    def __str__(self):
        return str(self.city) + ' ' + (self.name)

class NBAScheduleTemplate(models.Model):
    id                = models.IntegerField(primary_key=True)
    time              = models.TimeField('%H:%M')
    date              = models.DateField()
    game_stats_filled = models.BooleanField(default='False')
    team_stats_filled = models.BooleanField(default='False')
    game_odds_filled  = models.BooleanField(default='False')
    early_season_game = models.BooleanField(default='False')

    def __str__(self):
        return str(self.home_team) + " vs " + str(self.away_team) + " @ " + str(self.time)

    class Meta:
        abstract = True

class NBAGameStatsTemplate(models.Model):
    home_points    = models.IntegerField(blank=True, null=True)
    home_fgm       = models.IntegerField(blank=True, null=True)
    home_fga       = models.IntegerField(blank=True, null=True)
    home_fgp       = models.FloatField(blank=True, null=True)
    home_ftm       = models.IntegerField(blank=True, null=True)
    home_fta       = models.IntegerField(blank=True, null=True)
    home_ftp       = models.FloatField(blank=True, null=True)
    home_tpm       = models.IntegerField(blank=True, null=True)
    home_tpa       = models.IntegerField(blank=True, null=True)
    home_tpp       = models.FloatField(blank=True, null=True)
    home_offReb    = models.IntegerField(blank=True, null=True)
    home_defReb    = models.IntegerField(blank=True, null=True)
    home_totReb    = models.IntegerField(blank=True, null=True)
    home_assists   = models.IntegerField(blank=True, null=True)
    home_pFouls    = models.IntegerField(blank=True, null=True)
    home_steals    = models.IntegerField(blank=True, null=True)
    home_turnovers = models.IntegerField(blank=True, null=True)
    home_blocks    = models.IntegerField(blank=True, null=True)
    home_plusMinus = models.IntegerField(blank=True, null=True)

    away_points    = models.IntegerField(blank=True, null=True)
    away_fgm       = models.IntegerField(blank=True, null=True)
    away_fga       = models.IntegerField(blank=True, null=True)
    away_fgp       = models.FloatField(blank=True, null=True)
    away_ftm       = models.IntegerField(blank=True, null=True)
    away_fta       = models.IntegerField(blank=True, null=True)
    away_ftp       = models.FloatField(blank=True, null=True)
    away_tpm       = models.IntegerField(blank=True, null=True)
    away_tpa       = models.IntegerField(blank=True, null=True)
    away_tpp       = models.FloatField(blank=True, null=True)
    away_offReb    = models.IntegerField(blank=True, null=True)
    away_defReb    = models.IntegerField(blank=True, null=True)
    away_totReb    = models.IntegerField(blank=True, null=True)
    away_assists   = models.IntegerField(blank=True, null=True)
    away_pFouls    = models.IntegerField(blank=True, null=True)
    away_steals    = models.IntegerField(blank=True, null=True)
    away_turnovers = models.IntegerField(blank=True, null=True)
    away_blocks    = models.IntegerField(blank=True, null=True)
    away_plusMinus = models.IntegerField(blank=True, null=True)

    home_games       = models.IntegerField(default=0)
    home_wins        = models.IntegerField(default=0)
    home_losses      = models.IntegerField(default=0)
    home_win_pct     = models.FloatField(default=0.0)
    home_opp_wins    = models.IntegerField(default=0)
    home_opp_losses  = models.IntegerField(default=0)
    home_opp_win_pct = models.FloatField(default=0.0)

    home_points_pg    = models.FloatField(default=0.0)
    home_fgm_pg       = models.FloatField(default=0.0)
    home_fga_pg       = models.FloatField(default=0.0)
    home_fgp          = models.FloatField(default=0.0)
    home_ftm_pg       = models.FloatField(default=0.0)
    home_fta_pg       = models.FloatField(default=0.0)
    home_ftp          = models.FloatField(default=0.0)
    home_tpm_pg       = models.FloatField(default=0.0)
    home_tpa_pg       = models.FloatField(default=0.0)
    home_tpp          = models.FloatField(default=0.0)
    home_offReb_pg    = models.FloatField(default=0.0)
    home_defReb_pg    = models.FloatField(default=0.0)
    home_totReb_pg    = models.FloatField(default=0.0)
    home_assists_pg   = models.FloatField(default=0.0)
    home_pFouls_pg    = models.FloatField(default=0.0)
    home_steals_pg    = models.FloatField(default=0.0)
    home_turnovers_pg = models.FloatField(default=0.0)
    home_blocks_pg    = models.FloatField(default=0.0)
    home_plusMinus_pg = models.FloatField(default=0.0)

    home_opp_points_pg    = models.FloatField(default=0.0)
    home_opp_fgm_pg       = models.FloatField(default=0.0)
    home_opp_fga_pg       = models.FloatField(default=0.0)
    home_opp_fgp          = models.FloatField(default=0.0)
    home_opp_ftm_pg       = models.FloatField(default=0.0)
    home_opp_fta_pg       = models.FloatField(default=0.0)
    home_opp_ftp          = models.FloatField(default=0.0)
    home_opp_tpm_pg       = models.FloatField(default=0.0)
    home_opp_tpa_pg       = models.FloatField(default=0.0)
    home_opp_tpp          = models.FloatField(default=0.0)
    home_opp_offReb_pg    = models.FloatField(default=0.0)
    home_opp_defReb_pg    = models.FloatField(default=0.0)
    home_opp_totReb_pg    = models.FloatField(default=0.0)
    home_opp_assists_pg   = models.FloatField(default=0.0)
    home_opp_pFouls_pg    = models.FloatField(default=0.0)
    home_opp_steals_pg    = models.FloatField(default=0.0)
    home_opp_turnovers_pg = models.FloatField(default=0.0)
    home_opp_blocks_pg    = models.FloatField(default=0.0)
    home_opp_plusMinus_pg = models.FloatField(default=0.0)

    away_games       = models.IntegerField(default=0)
    away_wins        = models.IntegerField(default=0)
    away_losses      = models.IntegerField(default=0)
    away_win_pct     = models.FloatField(default=0.0)
    away_opp_wins    = models.IntegerField(default=0)
    away_opp_losses  = models.IntegerField(default=0)
    away_opp_win_pct = models.FloatField(default=0.0)

    away_points_pg    = models.FloatField(default=0.0)
    away_fgm_pg       = models.FloatField(default=0.0)
    away_fga_pg       = models.FloatField(default=0.0)
    away_fgp          = models.FloatField(default=0.0)
    away_ftm_pg       = models.FloatField(default=0.0)
    away_fta_pg       = models.FloatField(default=0.0)
    away_ftp          = models.FloatField(default=0.0)
    away_tpm_pg       = models.FloatField(default=0.0)
    away_tpa_pg       = models.FloatField(default=0.0)
    away_tpp          = models.FloatField(default=0.0)
    away_offReb_pg    = models.FloatField(default=0.0)
    away_defReb_pg    = models.FloatField(default=0.0)
    away_totReb_pg    = models.FloatField(default=0.0)
    away_assists_pg   = models.FloatField(default=0.0)
    away_pFouls_pg    = models.FloatField(default=0.0)
    away_steals_pg    = models.FloatField(default=0.0)
    away_turnovers_pg = models.FloatField(default=0.0)
    away_blocks_pg    = models.FloatField(default=0.0)
    away_plusMinus_pg = models.FloatField(default=0.0)

    away_opp_points_pg    = models.FloatField(default=0.0)
    away_opp_fgm_pg       = models.FloatField(default=0.0)
    away_opp_fga_pg       = models.FloatField(default=0.0)
    away_opp_fgp          = models.FloatField(default=0.0)
    away_opp_ftm_pg       = models.FloatField(default=0.0)
    away_opp_fta_pg       = models.FloatField(default=0.0)
    away_opp_ftp          = models.FloatField(default=0.0)
    away_opp_tpm_pg       = models.FloatField(default=0.0)
    away_opp_tpa_pg       = models.FloatField(default=0.0)
    away_opp_tpp          = models.FloatField(default=0.0)
    away_opp_offReb_pg    = models.FloatField(default=0.0)
    away_opp_defReb_pg    = models.FloatField(default=0.0)
    away_opp_totReb_pg    = models.FloatField(default=0.0)
    away_opp_assists_pg   = models.FloatField(default=0.0)
    away_opp_pFouls_pg    = models.FloatField(default=0.0)
    away_opp_steals_pg    = models.FloatField(default=0.0)
    away_opp_turnovers_pg = models.FloatField(default=0.0)
    away_opp_blocks_pg    = models.FloatField(default=0.0)
    away_opp_plusMinus_pg = models.FloatField(default=0.0)

    def __str__(self):
        return f"Game Stats id: {self.id}"

    class Meta:
        abstract = True

class NBASchedule2022(NBAScheduleTemplate):
    home_team = models.ForeignKey(NBATeam, related_name="home_team_2022", on_delete=models.CASCADE)
    away_team = models.ForeignKey(NBATeam, related_name="away_team_2022", on_delete=models.CASCADE)

class NBASchedule2021(NBAScheduleTemplate):
    home_team = models.ForeignKey(NBATeam, related_name="home_team_2021", on_delete=models.CASCADE)
    away_team = models.ForeignKey(NBATeam, related_name="away_team_2021", on_delete=models.CASCADE)

class NBASchedule2020(NBAScheduleTemplate):
    home_team = models.ForeignKey(NBATeam, related_name="home_team_2020", on_delete=models.CASCADE)
    away_team = models.ForeignKey(NBATeam, related_name="away_team_2020", on_delete=models.CASCADE)

class NBASchedule2019(NBAScheduleTemplate):
    home_team = models.ForeignKey(NBATeam, related_name="home_team_2019", on_delete=models.CASCADE)
    away_team = models.ForeignKey(NBATeam, related_name="away_team_2019", on_delete=models.CASCADE)

class NBASchedule2018(NBAScheduleTemplate):
    home_team = models.ForeignKey(NBATeam, related_name="home_team_2018", on_delete=models.CASCADE)
    away_team = models.ForeignKey(NBATeam, related_name="away_team_2018", on_delete=models.CASCADE)

class NBASchedule2017(NBAScheduleTemplate):
    home_team = models.ForeignKey(NBATeam, related_name="home_team_2017", on_delete=models.CASCADE)
    away_team = models.ForeignKey(NBATeam, related_name="away_team_2017", on_delete=models.CASCADE)

class NBAGameStats2022(NBAGameStatsTemplate):
    id = models.OneToOneField(NBASchedule2022, on_delete=models.CASCADE, primary_key=True)

class NBAGameStats2021(NBAGameStatsTemplate):
    id = models.OneToOneField(NBASchedule2021, on_delete=models.CASCADE, primary_key=True)

class NBAGameStats2020(NBAGameStatsTemplate):
    id = models.OneToOneField(NBASchedule2020, on_delete=models.CASCADE, primary_key=True)

class NBAGameStats2019(NBAGameStatsTemplate):
    id = models.OneToOneField(NBASchedule2019, on_delete=models.CASCADE, primary_key=True)

class NBAGameStats2018(NBAGameStatsTemplate):
    id = models.OneToOneField(NBASchedule2018, on_delete=models.CASCADE, primary_key=True)

class NBAGameStats2017(NBAGameStatsTemplate):
    id = models.OneToOneField(NBASchedule2017, on_delete=models.CASCADE, primary_key=True)

class NBAPredictions2022(models.Model):
    id                          = models.OneToOneField(NBASchedule2022, on_delete=models.CASCADE, primary_key=True)
    home_points_vegas           = models.FloatField(default=0.0)
    away_points_vegas           = models.FloatField(default=0.0)
    home_points_vegas_cum_me    = models.FloatField(default=0.0)
    away_points_vegas_cum_me    = models.FloatField(default=0.0)
    home_points_vegas_cum_rmse  = models.FloatField(default=0.0)
    away_points_vegas_cum_rmse  = models.FloatField(default=0.0)
    home_points_lr              = models.FloatField(default=0.0)
    away_points_lr              = models.FloatField(default=0.0)
    home_points_lr_cum_me       = models.FloatField(default=0.0)
    away_points_lr_cum_me       = models.FloatField(default=0.0)
    home_points_lr_cum_rmse     = models.FloatField(default=0.0)
    away_points_lr_cum_rmse     = models.FloatField(default=0.0)
    home_points_pr              = models.FloatField(default=0.0)
    away_points_pr              = models.FloatField(default=0.0)
    home_points_pr_cum_me       = models.FloatField(default=0.0)
    away_points_pr_cum_me       = models.FloatField(default=0.0)
    home_points_pr_cum_rmse     = models.FloatField(default=0.0)
    away_points_pr_cum_rmse     = models.FloatField(default=0.0)

class NBAOdds2022(models.Model):
    id          = models.CharField(primary_key=True, max_length=50)
    date        = models.DateField()
    home_team   = models.ForeignKey(NBATeam, related_name="home_team_odds_2022", on_delete=models.CASCADE)
    away_team   = models.ForeignKey(NBATeam, related_name="away_team_odds_2022", on_delete=models.CASCADE)
    home_spread = models.FloatField(default=0.0)
    away_spread = models.FloatField(default=0.0)
    total       = models.FloatField(default=0.0)
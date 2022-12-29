import sys, os, django
sys.path.append("/home/davidm97/Projects/Sports-Info-App/SportsApp")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SportsApp.settings")
django.setup()
 
from utils import *

#clear_tables_util()
#load_nba_teams_util()
#load_nba_schedule_util()
#download_nba_game_stats_util()
#calculate_nba_team_stats_util()
#download_game_odds_util()
calculate_predictions_util()
generate_error_plots_util()

#clear_nba_teams_util()

#copy_nba_stats_to_csv_util()
#rename_nba_logos_util()
#test_odds_api_util()

from datetime import datetime

NBA_SEASON = 2018
NBA_EARLY_SEASON_CUTOFF = 5

PLOT_PATH = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/static/media/plots/"
NBA_DATA_PATH = "/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/data/NBA/"

NBA_SEASON_START_DATE_DICT = {
    '2022' : datetime.strptime("2022-10-18", '%Y-%m-%d'),
    '2021' : datetime.strptime("2021-10-19", '%Y-%m-%d'),
    '2020' : datetime.strptime("2020-12-22", '%Y-%m-%d'),
    '2019' : datetime.strptime("2019-10-22", '%Y-%m-%d'),
    '2018' : datetime.strptime("2018-10-16", '%Y-%m-%d'),
    '2017' : datetime.strptime("2017-10-17", '%Y-%m-%d'),
}

NBA_TEAMS_LIST = [
    'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets',
    'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
    'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
    'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat',
    'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
    'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns',
    'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
    'Utah Jazz', 'Washington Wizards'
]

NBA_TEAMS_DICT = {
    "76ers"         : "Philadelphia"  ,
    "Celtics"       : "Boston"        ,
    "Lakers"        : "Los Angeles"   ,
    "Warriors"      : "Golden State"  ,
    "Magic"         : "Orlando"       ,
    "Pistons"       : "Detroit"       ,
    "Wizards"       : "Washington"    ,
    "Pacers"        : "Indiana"       ,
    "Rockets"       : "Houston"       ,
    "Hawks"         : "Atlanta"       ,
    "Pelicans"      : "New Orleans"   ,
    "Nets"          : "Brooklyn"      ,
    "Bulls"         : "Chicago"       ,
    "Heat"          : "Miami"         ,
    "Cavaliers"     : "Cleveland"     ,
    "Raptors"       : "Toronto"       ,
    "Knicks"        : "New York"      ,
    "Grizzlies"     : "Memphis"       ,
    "Thunder"       : "Oklahoma City" ,
    "Timberwolves"  : "Minnesota"     ,
    "Hornets"       : "Charlotte"     ,
    "Spurs"         : "San Antonio"   ,
    "Nuggets"       : "Denver"        ,
    "Jazz"          : "Utah"          ,
    "Mavericks"     : "Dallas"        ,
    "Suns"          : "Phoenix"       ,
    "Trail Blazers" : "Portland"      ,
    "Kings"         : "Sacramento"    ,
    "Clippers"      : "Los Angeles"   ,
    "Bucks"         : "Milwaukee"     
}

NBA_API_ID_DICT = {
    "76ers"         : 27   ,
    "Celtics"       : 2    ,
    "Lakers"        : 17   ,
    "Warriors"      : 11   ,
    "Magic"         : 26   ,
    "Pistons"       : 10   ,
    "Wizards"       : 41   ,
    "Pacers"        : 15   ,
    "Rockets"       : 14   ,
    "Hawks"         : 1    ,
    "Pelicans"      : 23   ,
    "Nets"          : 4    ,
    "Bulls"         : 6    ,
    "Heat"          : 20   ,
    "Cavaliers"     : 7    ,
    "Raptors"       : 38   ,
    "Knicks"        : 24   ,
    "Grizzlies"     : 19   ,
    "Thunder"       : 25   ,
    "Timberwolves"  : 22   ,
    "Hornets"       : 5    ,
    "Spurs"         : 31   ,
    "Nuggets"       : 9    ,
    "Jazz"          : 40   ,
    "Mavericks"     : 8    ,
    "Suns"          : 28   ,
    "Trail Blazers" : 29   ,
    "Kings"         : 30   ,
    "Clippers"      : 16   ,
    "Bucks"         : 21     
}

NBA_STAT_NAMES_LIST = [
    "PPG","FGM","FGA","FG%","FTM","FTA","FT%","3PM",
    "3PA","3P%","ORB","DRB","TRB","AST","PF","ST","TO",
    "BK","+/-"
]

NBA_TEAM_DB_STATS_FIELDS_LIST = [
    'points_pg','fgm_pg','fga_pg','fgp','ftm_pg','fta_pg',
    'ftp','tpm_pg','tpa_pg','tpp','offReb_pg','defReb_pg',
    'totReb_pg','assists_pg','pFouls_pg','steals_pg',
    'turnovers_pg','blocks_pg','plusMinus_pg','opp_points_pg',
    'opp_fgm_pg','opp_fga_pg','opp_fgp','opp_ftm_pg','opp_fta_pg',
    'opp_ftp','opp_tpm_pg','opp_tpa_pg','opp_tpp','opp_offReb_pg',
    'opp_defReb_pg','opp_totReb_pg','opp_assists_pg','opp_pFouls_pg',
    'opp_steals_pg','opp_turnovers_pg','opp_blocks_pg','opp_plusMinus_pg'
]

NBA_BOXSCORE_STATS_LIST = [
        'home_points','home_fgm','home_fga','home_fgp','home_ftm',
        'home_fta','home_ftp','home_tpm','home_tpa','home_tpp',
        'home_offReb','home_defReb','home_totReb','home_assists',
        'home_pFouls','home_steals','home_turnovers','home_blocks',
        'home_plusMinus',
        'away_points','away_fgm','away_fga','away_fgp','away_ftm',
        'away_fta','away_ftp','away_tpm','away_tpa','away_tpp',
        'away_offReb','away_defReb','away_totReb','away_assists',
        'away_pFouls','away_steals','away_turnovers','away_blocks',
        'away_plusMinus','played'
]

NBA_MODELS_TUPLE = (
    ('1','Linear Regression'),
    ('2','Choice 2')
)

NBA_TEAMS_TUPLE = (
    ( '1'  , 'Atlanta Hawks'),
    ( '2'  , 'Boston Celtics'),
    ( '3'  , 'Brooklyn Nets'),
    ( '4'  , 'Charlotte Hornets'),
    ( '5'  , 'Chicago Bulls'),
    ( '6'  , 'Cleveland Cavaliers'),
    ( '7'  , 'Dallas Mavericks'),
    ( '8'  , 'Denver Nuggets'),
    ( '9'  , 'Detroit Pistons'),
    ( '10' , 'Golden State Warriors'),
    ( '11' , 'Houston Rockets'),
    ( '12' , 'Indiana Pacers'),
    ( '13' , 'Los Angeles Clippers'),
    ( '14' , 'Los Angeles Lakers'),
    ( '15' , 'Memphis Grizzlies'),
    ( '16' , 'Miami Heat'),
    ( '17' , 'Milwaukee Bucks'),
    ( '18' , 'Minnesota Timberwolves'),
    ( '19' , 'New Orleans Pelicans'),
    ( '20' , 'New York Knicks'),
    ( '21' , 'Oklahoma City Thunder'),
    ( '22' , 'Orlando Magic'),
    ( '23' , 'Philadelphia 76ers'),
    ( '24' , 'Phoenix Suns'),
    ( '25' , 'Portland Trail Blazers'),
    ( '26' , 'Sacramento Kings'),
    ( '27' , 'San Antonio Spurs'),
    ( '28' , 'Toronto Raptors'),
    ( '29' , 'Utah Jazz'),
    ( '30' , 'Washington Wizards')
)
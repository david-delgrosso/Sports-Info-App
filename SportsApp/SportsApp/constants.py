from datetime import *

NBA_SEASON = 2019

NBA_SEASON_START_DATE_DICT = {
    '2022' : datetime.strptime("2022-10-18", '%Y-%m-%d'),
    '2021' : datetime.strptime("2021-10-19", '%Y-%m-%d'),
    '2020' : datetime.strptime("2020-12-22", '%Y-%m-%d'),
    '2019' : datetime.strptime("2019-10-22", '%Y-%m-%d'),
    '2018' : datetime.strptime("2018-10-16", '%Y-%m-%d'),
    '2017' : datetime.strptime("2017-10-17", '%Y-%m-%d'),
}

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

NBA_STAT_NAMES_LIST = ["PPG","FGM","FGA","FG%","FTM","FTA","FT%","3PM",
                       "3PA","3P%","ORB","DRB","TRB","AST","PF","ST","TO",
                       "BK","+/-"]
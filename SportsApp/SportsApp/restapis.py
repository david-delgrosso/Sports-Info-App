import requests as re
import json
from .config import *


def request_nba_schedule_to_json(year):
    
    url = "https://api-nba-v1.p.rapidapi.com/games"

    querystring = {"season":str(year)}

    headers = API_NBA_HEADERS

    response = re.request("GET", url, headers=headers, params=querystring)

    re_json = response.json()
    json_object = json.dumps(re_json, indent=4)

    filename = "nba_season_" + str(year) + ".json"
    with open(filename,'w') as f:
        f.write(json_object)

def request_nba_game_stats(id):
    url = "https://api-nba-v1.p.rapidapi.com/games/statistics"

    querystring = {"id":id}
    
    headers = API_NBA_HEADERS
    
    response = re.request("GET", url, headers=headers, params=querystring)
    re_json = response.json()
    json_object = json.dumps(re_json, indent=4)

    with open("test_game_stats.json",'w') as f:
        f.write(json_object)
    
    return json_object
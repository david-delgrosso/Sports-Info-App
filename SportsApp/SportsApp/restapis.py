import requests as re
import json
from .config import *

# Download schedule from API and save to JSON file
# @param[in]    year    year of season being requested
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

# Download game stats from API
# @param[in]    id    id of game being requested
def request_nba_game_stats(id):
    url = "https://api-nba-v1.p.rapidapi.com/games/statistics"

    querystring = {"id":id}
    
    headers = API_NBA_HEADERS
    
    response = re.request("GET", url, headers=headers, params=querystring)
    re_json = response.json()
    json_object = json.dumps(re_json, indent=4)

    # with open("test_game_stats.json",'w') as f:
    #     f.write(json_object)
    
    return json_object

def request_nba_game_odds(date):
    sport = "basketball_nba"
    api_key = ODDS_API_HEADERS['API_KEY']
    regions = "us"
    markets = "spreads,totals"
    date += "T00:00:00Z"
    oddsFormat = "american"
    bookmakers = "fanduel,draftkings,williamhill_us,pointsbetus"
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds-history/?apiKey={api_key}&regions={regions}&markets={markets}&oddsFormat={oddsFormat}&bookmakers={bookmakers}&date={date}"
    
    response = re.get(url)
    re_json = response.json()
    json_object = json.dumps(re_json, indent=4)

    with open("test_game_odds.json",'w') as f:
        f.write(json_object)

    return json_object

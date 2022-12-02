import requests as re
from bs4 import BeautifulSoup as bs
from .utils import *
from .models import NBASchedule
import json
from .config import *


def request_nba_schedule_to_json(**kwargs):
    
    url = "https://api-nba-v1.p.rapidapi.com/games"

    querystring = {"season":"2022"}

    headers = API_NBA_HEADERS

    response = re.request("GET", url, headers=headers, params=querystring)

    re_json = response.json()
    json_object = json.dumps(re_json, indent=4)

    filename = "nba_season_2022.json"
    with open(filename,'w') as f:
        f.write(json_object)
import requests as re
from bs4 import BeautifulSoup as bs
from .utils import convert_time
from .models import Game


def get_games(url, **kwargs):
    page = re.get(url)
    soup = bs(page.content, 'html.parser')
    table = soup.findAll('div', {'class':'ScheduleTables'})[0]
    
    games = []
    
    is_first = True
    for i,row in enumerate(table.find_all('tr')):
        if not is_first:
            cols = row.findAll('td')
            away_team = cols[0].find('span', {'class': 'Table__Team'}).get_text()
            home_team = cols[1].find('span', {'class': 'Table__Team'}).get_text()
            #time = convert_time(cols[2].get_text())
            time = cols[2].get_text()
            game_obj = Game(home_team=home_team, away_team=away_team, time=time)
            games.append(game_obj)
        else:
            is_first = False
        
    return games
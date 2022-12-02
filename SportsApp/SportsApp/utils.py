from datetime import *
import os
from .models import NBASchedule
from .constants import *

def convert_time(time_in):
    if time_in.endswith('PM'):
                    time_sp = time_in.split(':')
                    hr = int(time_sp[0])
                    hr += 12
                    min = time_sp[1][:2]
                    time_out = str(hr) + ':' + min
    if time_out.startswith("24"):
        time_out = '00' + time_out[2:]
    return time_out

def convert_date(date_in):
    month_dict = {"Jan":1,
                   "Feb":2,
                   "Mar":3,
                   "Apr":4,
                   "Oct":10,
                   "Nov":11,
                   "Dec":12}
    year_dict = {"Jan":2023,
                 "Feb":2023,
                 "Mar":2023,
                 "Apr":2023,
                 "Oct":2022,
                 "Nov":2022,
                 "Dec":2022}
    date_sp = date_in.split(' ')
    date_out = str(year_dict[date_sp[0]]) + '-' + str(month_dict[date_sp[0]]) + '-' + date_sp[1]
    return date_out

def load_nba_schedule(**kwargs):
    games = []

    process_nba_schedule_raw()
    load_nba_schedule_to_db()

    games = NBASchedule.objects.all()

    return games

def process_nba_schedule_raw():

    raw_filename = '/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/nba_schedule_raw.csv'
    proc_filename = '/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/nba_schedule.csv'
    col_names = "sport,date,home_city,home_team,away_city,away_team,time"
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    with open(raw_filename,'r') as fraw:
        lines = fraw.readlines()

    with open(proc_filename,'w') as fproc:
        fproc.write(col_names)
        fproc.write('\n')

        date = ''
        for line in lines:
            line_sp = line.split(',')
            if line_sp[0][:3] in days_of_week:
                date = convert_date(line_sp[0][4:])
                continue
            else:
                teams = line_sp[0]
                time = convert_time(line_sp[1])

                if '@' in teams:
                    teams_sp = teams.split('@')
                else:
                    teams_sp = teams.split('vs.')

                away_team, away_city = get_nba_team_city(teams_sp[0][:-1])
                home_team, home_city = get_nba_team_city(teams_sp[1][1:])

            write_line = "NBA" + ','
            write_line += str(date) + ','
            write_line += str(home_city) + ','
            write_line += str(home_team) + ','
            write_line += str(away_city) + ','
            write_line += str(away_team) + ','
            write_line += str(time)

            fproc.write(write_line)
            fproc.write('\n')

def load_nba_schedule_to_db():
    filename = '/home/davidm97/Projects/Sports-Info-App/SportsApp/SportsApp/nba_schedule.csv'
    with open(filename,'r') as f:
        lines = f.readlines()

    first_line = True
    for line in lines:
        if first_line:
            first_line = False
            continue

        line_sp = line.split(',')
        sch_obj = NBASchedule.objects.create(sport=line_sp[0],
                                             date=line_sp[1],
                                             home_city=line_sp[2],
                                             home_team=line_sp[3],
                                             away_city=line_sp[4],
                                             away_team=line_sp[5],
                                             time=line_sp[6])

def get_nba_team_city(team_in):
    name = NBA_TEAMS_DICT[team_in]
    city = NBA_CITY_DICT[team_in]
    return name, city

def get_todays_games(sport):
    today = str(datetime.now().strftime("%Y-%m-%d"))
    games = NBASchedule.objects.filter(sport=sport, date=today)
    return games
from datetime import *

def convert_time(time_in):
    try:
        t = datetime.strptime(time_in, '%I:%M %p')
        time_out = t.time()
    except:
        time_out = 'LIVE'
    return time_out
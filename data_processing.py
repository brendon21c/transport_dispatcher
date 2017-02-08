import zipcode
from datetime import *
from models import *
from app import db



def process_time_entry(start, end):

    time_list = []

    start_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')

    start_time = start_time.time()
    end_time = end_time.time()

    time_list.append(start_time)
    time_list.append(end_time)


    return time_list

def check_driver_schedule(current_time,check_start,check_end):

    """ This will check the current time against a particular driver and return
    a string response. """

    if current_time < check_start:

        return "before start"

    elif current_time > check_end:

        return "after end"

    else:

        return "working"

def is_driver_clocked_in(id_number):

    query = Drivers.query.filter_by(id = id_number).all()

    start = 0
    end = 0

    for x in query:

        start = x.start_time
        end = x.end_time


    now = datetime.now()
    now = now.time()

    #print(now)

    working = check_driver_schedule(now, start, end)

    return working

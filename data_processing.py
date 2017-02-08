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

def check_driver_schedule(time, check):

    """ This will check the current time against a particular driver and return
    a True/False return. """


    pass

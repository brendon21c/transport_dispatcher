import zipcode
from datetime import *
from models import *
from app import db
from sqlalchemy import *


def create_driver_zone(driver_zip):

    """ This will create a new zone for a driver. """
    # gets last entry in the database so that zones can be kept in order.
    last_zone_entry = db.session.query(func.max(MN_Zipcodes.delivery_zone)).first()
    zone_num = last_zone_entry[0]

    #last_zone_entry = db.session.query(func.max(MN_Zipcodes.delivery_zone).filter)

    print(last_zone_entry)

    if last_zone_entry[0] == None:

        zone = 1
        print(zone)

        return zone

    else:

        zone = last_zone_entry.delivery_zone

        zone_final = zone + 1
        print(zone_final)

        return zone_final

def create_driver_zipcode_zone(start_zip):


    zip_loc = zipcode.isequal(start_zip)

    zip_lat_lon = (zip_loc.lat, zip_loc.lon)

    zip_radius = zipcode.isinradius(zip_lat_lon, 15)

    zip_list_final = []

    for z in zip_radius:

        zip_list_final.append[z[0]]

    print(zip_list_final)

    return zip_list_final



def process_time_entry(start, end):

    time_list = []

    start_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')

    start_time = start_time.time()
    end_time = end_time.time()

    time_list.append(start_time)
    time_list.append(end_time)


    return time_list

# This method may not be needed.
# def check_driver_schedule(current_time,check_start,check_end):
#
#     """ This will check the current time against a particular driver and return
#     a string response. """
#
#     if current_time < check_start:
#
#         return "before start"
#
#     elif current_time > check_end:
#
#         return "after end"
#
#     else:
#
#         return "working"


def current_driver_list():

    # query = Drivers.query.filter_by(id = id_number).all()
    #
    # start = 0
    # end = 0
    #
    # for x in query:
    #
    #     start = x.start_time
    #     end = x.end_time


    now = datetime.now()
    now = now.time()

    query_all = Drivers.query.filter(Drivers.start_time <= now).filter(Drivers.end_time >= now)

    # for x in query_all:
    #     print(x.id)

    #print(now)

    #working = check_driver_schedule(now, start, end)

    return query_all

from datetime import *
from models import *
from app import db
from sqlalchemy import *



def create_driver_zipcode_zone(start_zip):

    import zipcode # need to import here or you get a thredding error.

    zip_loc = zipcode.isequal(start_zip)

    zip_lat_lon = (zip_loc.lat, zip_loc.lon)

    zip_radius = zipcode.isinradius(zip_lat_lon, 15)
    print(zip_radius)

    zip_list_final = []

    for z in zip_radius:

        zip_list_final.append(z.zip)

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


def current_driver_list():


    now = datetime.now().time()
    hour = now.hour # returns just the hour
    date = datetime.now().date # returns the date


    query_all = Drivers.query.filter(Drivers.start_time <= now).filter(Drivers.end_time >= now)

    # for x in query_all:
    #     print(x.id)

    #print(now)

    #working = check_driver_schedule(now, start, end)

    return query_all


def assign_route_to_driver(del_zip):

    timeTest = datetime.strptime("06:00", '%H:%M').time() # variable time for testing purposes.

    driver_query = Drivers.query.filter(Drivers.start_time <= timeTest).filter(Drivers.end_time >= timeTest)

    dest_query = MN_Zipcodes.query.filter(MN_Zipcodes.zip_code == del_zip)

    driver_id_assign = get_driver_for_route(driver_query, dest_query)

    return driver_id_assign
    

# This takes a list of current drivers and finds returns the appropiate
# driver
def get_driver_for_route(drivers, dest):

    possible_zones = [] # in case there are more than one zone for the zip code

    possible_drivers = []

    zone = "" # zone to assign to

    for x in dest:

        possible_zones.append(x.delivery_zone)

    if len(possible_zones) == 1:

        zone = possible_zones[0]

    driver = 0 # driver id to assign to

    driver_query = drivers.filter(Drivers.delivery_zone == zone)

    for x in driver_query:

        possible_drivers.append(x.id)

    if len(possible_drivers) == 1:

        driver = possible_drivers[0]

    return driver

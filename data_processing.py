from datetime import *
from models import *
from app import db
from sqlalchemy import *
import logging as log


# takes a 12hr time and turns it into a 24 for data entry.
def process_time_entry(start, end):

    time_list = []

    start_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')

    start_time = start_time.time()
    end_time = end_time.time()

    time_list.append(start_time)
    time_list.append(end_time)


    return time_list

# Sets up the Workload table for each day to track driver stops.
def create_new_stop_day():

    today = datetime.now().date() # returns the date
    #print(today)

    query = Workload.query.filter_by(date = today).first()
    #print(query)

    if not query:

        all_drivers = Drivers.query.all()

        for driver in all_drivers:

            person = driver.id

            new_day = Workload(today, person, 0)

            db.session.add(new_day)
            db.session.commit()

def current_driver_list():


    now = datetime.now().time() # current time.
    hour = now.hour # returns just the hour
    date = datetime.now().date() # returns the date

    # print(type(date))
    # print(date)

    query_all = Drivers.query.filter(Drivers.start_time <= now).filter(Drivers.end_time >= now)

    return query_all


def assign_route_to_driver(del_zip, current_time):


    driver_query = Drivers.query.filter(Drivers.start_time <= current_time).filter(Drivers.end_time >= current_time)

    dest_query = MN_Zipcodes.query.filter(MN_Zipcodes.zip_code == del_zip)

    dest_zones = possible_zones(dest_query) # get zones

    drivers_list = possible_drivers(driver_query, dest_zones) # get drivers

    if drivers_list:

        if len(drivers_list) == 1: # only one driver.

            driver_id = drivers_list[0]
            update_driver_workload(driver_id)

            return driver_id

        else:

            driver_id = compare_driver_workload(drivers_list) # multiple drivers.
            update_driver_workload(driver_id)

            return driver_id


# Updates the driver workload table to keep track of stops.
def update_driver_workload(driver):

    today = datetime.now().date() # returns the date

    stop_numbers = Workload.query.filter_by(date = today).filter_by(driverID = driver).first()

    stop_numbers.del_num = stop_numbers.del_num + 2 # Adding 2 to the number because each order has 2 stops (pickup & delivery)

    db.session.commit()


# gets a list of available drivers.
def possible_drivers(drivers, zones):

    possible_drivers = []

    for driver in drivers:
        for zone in zones:

            if driver.delivery_zone == zone:

                possible_drivers.append(driver.id)

    print(possible_drivers)

    return(possible_drivers)

# gets a list of zones for the delivery.
def possible_zones(dest):

    possible_zones = []

    for x in dest:

        possible_zones.append(x.delivery_zone)


    return possible_zones


# Work in progress, may be modified with query.
def compare_driver_workload(drivers_list):

    today = datetime.now().date() # returns the date

    workload_number = []

    for driver in drivers_list:

        stop_numbers = Workload.query.filter_by(date = today).filter_by(driverID = driver).first()

        number = stop_numbers.del_num

        #print(number)

        workload_number.append(number)


    low = workload_number[0]
    #print(low)
    driver_id = 0

    for stops in workload_number: # finds the driver with the least amount of stops.

        if stops <= low:

            low = stops

            index = workload_number.index(stops) # position in list

            driver_id = drivers_list[index]

    print(driver_id)

    return driver_id

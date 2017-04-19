from datetime import *
from models import *
from app import db
from sqlalchemy import *
import logging as log
import requests
import json
from keys import keys
from flask import jsonify


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

# Processes and assigns an order to the appropitate driver.
# This does a alot and I tried to break it down for testing purposes as much as possible.
def assign_route_to_driver(del_zip, current_time):


    driver_query = Drivers.query.filter(Drivers.start_time <= current_time).filter(Drivers.end_time >= current_time)

    dest_query = MN_Zipcodes.query.filter(MN_Zipcodes.zip_code == del_zip)

    dest_zones = possible_zones(dest_query) # get zones

    if not dest_zones:

        dest_zones = find_anchor_zone(del_zip) # del zipcode is not in the database.

    drivers_list = possible_drivers(driver_query, dest_zones) # get drivers

    if not drivers_list:

        drivers_list = find_backup_driver(driver_query, dest_zones)

    # print(dest_zones)
    # print(drivers_list)

    if drivers_list:

        if len(drivers_list) == 1: # only one driver.

            driver_id = drivers_list[0]
            #print(driver_id)
            update_driver_workload(driver_id)

            return driver_id

        else:

            driver_id = compare_driver_workload(drivers_list) # multiple drivers.
            #print(driver_id)
            update_driver_workload(driver_id)

            return driver_id


# Updates the driver workload table to keep track of stops.
def update_driver_workload(driver):

    today = datetime.now().date() # returns the date

    stop_numbers = Workload.query.filter_by(date = today).filter_by(driverID = driver).first()

    stop_numbers.del_num = stop_numbers.del_num + 2 # Adding 2 to the number because each order has 2 stops (pickup & delivery)

    db.session.commit()

# This will get called when the user updates or deletes orders.
def update_driver_workload_subtraction(driver):

    today = datetime.now().date() # returns the date

    stop_numbers = Workload.query.filter_by(date = today).filter_by(driverID = driver).first()

    stop_numbers.del_num = stop_numbers.del_num - 2

    db.session.commit()

# Will update both pickup and delivery tables.(for assining a new driver id.)
def update_orders_table(order_id, new_driver, old_driver):


    pickup_update = Order_Table_Pickup.query.filter_by(id = order_id).first()
    pickup_update.driverID = new_driver

    delivery_update = Order_Table_Del.query.filter_by(id = order_id).first()
    delivery_update.driverID = new_driver

    db.session.commit()

    update_driver_workload(new_driver) # adds two to the new

    update_driver_workload_subtraction(old_driver) # deletes two from the old.

def delete_order(order_id, driver):

    pickup_delete = Order_Table_Pickup.query.filter_by(id = order_id).delete()

    delivery_delete = Order_Table_Del.query.filter_by(id = order_id).delete()

    db.session.commit()

    update_driver_workload_subtraction(driver)





# gets a list of available drivers.
def possible_drivers(drivers, zones):

    possible_drivers = []

    for driver in drivers:
        for zone in zones:

            if driver.delivery_zone == zone:

                possible_drivers.append(driver.id)

    return(possible_drivers)

# finds a driver if no driver in a zone.
def find_backup_driver(drivers, zones):

    now = datetime.now().time() # current time.
    hour = now.hour # returns just the hour
    today = datetime.now().date() # returns the date

    final_driver_return = [] # return to assign_route_to_driver.

    if hour >= 18:

        driver_pool = []

        for driver in drivers:

            driver_id = driver.id

            driver_pool.append(driver_id)

        driver = compare_driver_workload(driver_pool) # find me the driver with the lowest amount of work.

        final_driver_return.append(driver)

        return final_driver_return

    else:

        zone = zones[0]

        if zone == 2:

            zone = 1

            for driver in drivers:

                if driver.delivery_zone == zone:

                    final_driver_return.append(driver.id)

                    return final_driver_return


        elif zone == 1:

            zone = 2

            for driver in drivers:

                if driver.delivery_zone == zone:

                    final_driver_return.append(driver.id)

                    return final_driver_return

        else:

            zone = 5

            for driver in drivers:

                if driver.delivery_zone == zone:

                    final_driver_return.append(driver.id)

                    return final_driver_return





# gets a list of zones for the delivery.
def possible_zones(dest):

    possible_zones = []

    for x in dest:

        possible_zones.append(x.delivery_zone)


    return possible_zones


# Finds the nearest zone if the delivery zip code isn't in the database.
def find_anchor_zone(dest):

    key = keys['GOOGLE_KEY']

    query = MN_Zipcodes.query.filter(MN_Zipcodes.anchor_zip == True)

    zone_list = [] # Needs to be a list to work with other functions later.

    zone = 0
    low = 500 # default number to start the comparison, this would be 500mi.

    for x in query:

        url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}'.format(dest,x.zip_code, key)

        request = requests.get(url)

        json_format = request.json()

        distance_string = json_format['routes'][0]['legs'][0]['distance']['text'] # gets the distance in miles.
        distance_split = distance_string.split(' ')
        distance_float = float(distance_split[0])

        if distance_float < low:

            zone = x.delivery_zone
            low = distance_float

    print(zone)
    print(low)

    zone_list.append(zone)

    return zone_list


def compare_driver_workload(drivers_list):

    today = datetime.now().date() # returns the date

    workload_number = []

    for driver in drivers_list:

        stop_numbers = Workload.query.filter_by(date = today).filter_by(driverID = driver).first()

        number = stop_numbers.del_num # Gets the current number of stops for every driver working.

        #print(number)

        workload_number.append(number)


    low = workload_number[0]
    #print(low)
    driver_id = 0

    # finds the driver with the least amount of stops.
    for stops in workload_number:

        if stops <= low:

            low = stops

            index = workload_number.index(stops) # position in list

            driver_id = drivers_list[index]

    print(driver_id)

    return driver_id

# Loop over query and send back a JSON to send to phone.
def create_json(query):

    data = {}

    for item in query:

        order_info = {}

        order_info['customer'] = item.name
        order_info['address'] = item.address
        order_info['city'] = item.city
        order_info['zip_code'] = item.zip_code

        data[item.id] = order_info

        # print(item.id)
        # print(item.name)
        # print(item.address)
        # print(item.city)
        # print(item.zip_code)

    json_data = json.dumps(data) # TODO Not sure if this the best way to build JSON data.

    print(json_data)

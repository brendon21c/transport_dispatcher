from flask import request, Blueprint, jsonify, current_app

account_api = Blueprint('account_api', __name__)

from data_processing import *
from datetime import *
import logging
from models import *
import json
import itertools



class PickupEncoder(json.JSONEncoder):
    """take a database query and returns a json"""
    def default(self,obj):

        if isinstance(obj, Order_Table_Pickup):

            return { 'OrderNumber' : obj.id,
            #'date' : obj.date,
            'customer' : obj.name,
            'address' : obj.address,
            'city' : obj.city,
            'zip_code' : obj.zip_code,
            'pickup_time' : obj.pick_time.isoformat(),
            'delivery_time' : obj.del_time.isoformat(),
            'action' : obj.action
            }

        elif isinstance(obj, Order_Table_Del):

            return { 'OrderNumber' : obj.id,
            #'date' : obj.date,
            'customer' : obj.name,
            'address' : obj.address,
            'city' : obj.city,
            'zip_code' : obj.zip_code,
            'pickup_time' : obj.pick_time.isoformat(),
            'delivery_time' : obj.del_time.isoformat(),
            'action' : obj.action
            }
        else:

            return json.JSONEncoder.default(self, obj)


# gets the current route list for the requested driver number, e.g. driver #7.
@account_api.route('/api/routes/')
def get_routes_for_driver():

    current_app.json_encoder = PickupEncoder

    if request.args.get('driverid'):

        driverid = request.args.get('driverid')

        order_date = datetime.now().date() # returns the date

        driver_list = current_driver_list()

        name = ""

        for driver in driver_list:

            # name = driver.first_name
            name_id = driver.id

            if name_id == int(driverid):

                Pickup_query = Order_Table_Pickup.query.filter_by(date = order_date).filter_by(driverID = name_id).all()
                Delivery_query = Order_Table_Del.query.filter_by(date = order_date).filter_by(driverID = name_id).all()

                pickup_json = jsonify(Pickup_query)
                del_json = jsonify(Delivery_query)

                combined_1= json.loads(pickup_json.data)
                combined_2= json.loads(del_json.data)

                combined_final = { 'Pickup' : combined_1, 'Delivery' : combined_2 }

                json.dumps(combined_final)


                # response = dict(itertools.chain(pickup_json,items(), del_json.items()))
                # print(response)
                # print(type(response))


                return jsonify(combined_final)

                #return 'this is an api call for driver id ' + str(driverid) + ' ' + name



    else:

        return 'no routes'

# checks to see if driver exists and sends back the Driver ID is they do.
@account_api.route('/api/driver_login/')
def get_driver():

    if request.args.get('driverid'):

        driverid = request.args.get('driverid')

        order_date = datetime.now().date() # returns the date

        driver_list = current_driver_list()

        for driver in driver_list:

            driver_id = driver.id

            if driver.id == int(driverid):

                return "driving"

        return "not driving"

# driver has arrived at pickup. This will update the pickup time for both Pickup and Delivery tables.
# Future Program will include a deadline.
@account_api.route('/api/pickup/')
def pickup_stop():

    if request.args.get('driverid'):

        driverid = request.args.get('driverid')
        order_num = request.args.get('ordernum')


        try:

            update_pickup_time(driverid, order_num)

        except Exception as e:

            return "problems"


        return driverid + order_num

# driver has arrived at Delivery. This will update the pickup time for both Pickup and Delivery tables.
# Future Program will include a deadline.
@account_api.route('/api/delivery/')
def delivery_stop():

    if request.args.get('driverid'):

        driverid = request.args.get('driverid')
        order_num = request.args.get('ordernum')


        try:

            update_delivery_time(driverid, order_num)

        except Exception as e:

            return "problems"


        return driverid + order_num



@account_api.route('/api')
def apicall():

    return 'this is an api call'

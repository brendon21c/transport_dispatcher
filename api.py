from flask import request, Blueprint, jsonify

account_api = Blueprint('account_api', __name__)

from data_processing import *
from datetime import *
import logging
from models import *
import json


class PickupEncoder(json.JSONEncoder):
    """take a database query and returns a json"""
    def process_del_to_json(self,obj):

        if isinstance(obj, Order_Table_Pickup):

            return { 'OrderNumber' : obj.id,
            'date' : obj.date,
            'customer' : obj.name,
            'address' : obj.address,
            'city' : obj.city,
            'zip_code' : obj.zip_code,
            'pickup_time' : obj.pick_time,
            'delivery_time' : obj.del_time

            }
        else:

            return json.JSONEncoder.default(self, obj)



account_api.JSONEncoder = PickupEncoder

@account_api.route('/api/routes/')
def get_routes_for_driver():

    if request.args.get('driverid'):

        driverid = request.args.get('driverid')
        print(driverid)

        order_date = datetime.now().date() # returns the date

        driver_list = current_driver_list()

        name = ""

        for driver in driver_list:

            name = driver.first_name
            name_id = driver.id

            if name_id == int(driverid):

                Pickup_query = Order_Table_Pickup.query.filter_by(date = order_date).filter_by(driverID = name_id).all()
                Delivery_query = Order_Table_Del.query.filter_by(date = order_date).filter_by(driverID = name_id).all()

                return_list = [Pickup_query]
                result = jsonify(return_list)
                print(result)

                return 'this is an api call for driver id ' + str(driverid) + ' ' + name



    else:

        return 'no driver'


@account_api.route('/api')
def apicall():

    return 'this is an api call'

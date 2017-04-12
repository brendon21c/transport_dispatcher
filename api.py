from flask import request, Blueprint, jsonify

account_api = Blueprint('account_api', __name__)

from data_processing import *
from datetime import *
import logging
from models import *


@account_api.route('/api/routes/')
def get_routes_for_driver():

    if request.args.get('driverid'):

        driverid = request.args.get('driverid')

        order_date = datetime.now().date() # returns the date

        driver_list = current_driver_list()

        name = ""

        test_query = Order_Table_Pickup.query.filter_by(date = order_date).all()

        create_json(test_query)

        for driver in driver_list:

            name = driver.first_name

        return 'this is an api call for driver id ' + str(driverid) + ' ' + name

    else:

        return 'no driver'


@account_api.route('/api')
def apicall():

    return 'this is an api call'

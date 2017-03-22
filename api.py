from flask import request
from app import app


@app.route('/api/routes/')
def get_routes_for_driver():

    driverid = request.args.get('driverid')

    driver_list = current_driver_list()

    name = ""

    for driver in driver_list:

        name = driver.first_name

    return 'this is an api call for driver id ' + str(driverid)


@app.route('/api')
def apicall():

    print('got here')
    return 'this is an api call'

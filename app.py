from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exists, and_
import itertools
from datetime import *
import logging as log
from keys import keys
from api import account_api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport_db.sqlite3'
app.config['SECRET_KEY'] = "transportation"
app.register_blueprint(account_api)

db = SQLAlchemy(app)
from data_processing import *
from models import * # Needs to be after db, otherwise no tables are created.



@app.route('/', methods = ['GET', 'POST'])
def home_page():
    #

    # create a new zone

    # Zones for testing
    # zip_code_list_1 = [55316,55448,55433,55434,55445,55443,55304,55444,55327,55303,55369,55569,55449,55432,55311,55429,55428,55430,55014,55442,55421,55011,55112,55374,55412,55446,55422,55126,55418,55427,55441,55340,55411,55413,55447]
    # zip_code_list_2 = [ 55305,55441,55447,55426,55345,55427,55343,55391,55446,55442,55436,55416,55422,55323,55361,55346,55424,55356,55405,55344,55428,55439,55410,55411,55392,55408,55403,55409,55429,55412,55435,55402,55401,55384,55419,55440,55458,55459,55460,55474,55478,55479,55480,55483,55484,55485,55486,55487,55488,55470,55472,55467,55404,55415,55317,55347,55430,55340,55331,55407,55594,55570,55571,55572,55574,55576,55577,55578,55579,55593,55348,55573,55454,55413,55455,55569,55414,55418,55595,55596,55597,55598,
    # 55599,55311,55423,55438,55369,55364,55445,55437,55406,55359,55421,55443,55417
    # ]
    #
    # zip_code_list_3 = [55306,55044,55124,55337,55378,55372,55020,55122,55024,55054,55431,55437,55420,55068,55438,55425,55123,55121,55379,55010,55088,55423,55435,55347,55450,55439,55111,55120,55344,55077,55150,55419,55417,55424]
    # zip_code_list_4 = [55125,55129,55188,55119,55055,55128,55042,55075,55106,55001,55016,55101,55107,55170,55133,55144,55145,55146,55155,55164,55165,55175,55187,55109,55076,55071,55130,55043,55102,55077,55118,55090,55172,55103,55117,55003,55115,55120,55105,55082,55116,55104,55083,55150,54016,55110,55108,55113,55121,55123,55114,55111,55127,55033,55406,54082,55450,55417,55126,55414]
    # zip_code_list_5 = [55113,55108,55117,55114,55103,55413,55104,55418,55414,55455,55454,55130,55467,55415,55421,55472,55470,55488,55487,55486,55485,55484,55483,55458,55459,55460,55474,55478,55479,55480,55440,55112,55105,55401,55126,55406,55404,55402,55144,55187,55170,55133,55146,55145,55165,55155,55164,55175,55101,55172,55102,55411,55403,55127,55107,55412,55407,55116,55109,55106,55405,55430,55408,55432,55417]
    #
    # add_zone_to_DB(zip_code_list_5, 5)


    create_new_stop_day() # only runs once a day.

    get_drivers = current_driver_list()

    # This is for testing:
    #timeTest = datetime.strptime("7:00", '%H:%M').time() # variable time for testing purposes.
    #assign_route_to_driver('55303', timeTest)


    return render_template('home_page.html', drivers = get_drivers)


@app.route('/new_driver', methods = ['GET', 'POST'])
def new_driver():

    if request.method == 'POST':

        start_time = request.form['start_time']
        end_time = request.form['end_time']

        time_list = process_time_entry(start_time, end_time) # processes form data into datetime

        start_time = time_list[0]
        end_time = time_list[1]

        zip_code_form = request.form['zipcode']

        driver = Drivers(request.form['first'], request.form['last'], request.form['address'], request.form['city'], request.form['zipcode'],
        request.form['truck'], request.form['zone'], start_time, end_time)

        db.session.add(driver)
        db.session.commit()



        return redirect(url_for('home_page'))


    return render_template('new_driver.html', zones = MN_Zipcodes.query.filter_by(anchor_zip = True).all(), drivers = Drivers.query.all())


@app.route('/new_order', methods = ['GET', 'POST'])
def new_order():

    if request.method == 'POST':

        date = datetime.now().date() # returns the date
        default_time = datetime.strptime("06:00", '%H:%M').time() # Needed to enter into database, will be updated by program.

        #assign_method = request.form['assign_method']

        if request.form['assign_method'] == 'auto':


            #timeTest = datetime.strptime("09:00", '%H:%M').time() # variable time for testing purposes.

            current_time = datetime.now().time() # current time.

            driver_id = assign_route_to_driver(request.form['ToZip'], current_time)

            orderPickup = Order_Table_Pickup(date,request.form['FromName'],request.form['FromAddress'],
            request.form['FromCity'], request.form['FromZip'],default_time, default_time, "pickup",1, driver_id)

            orderDel = Order_Table_Del(date,request.form['ToName'],request.form['ToAddress'],
            request.form['ToCity'],request.form['ToZip'],default_time, default_time, "delivery",1, driver_id)

            db.session.add(orderPickup)
            db.session.add(orderDel)
            db.session.commit()

            update_driver_workload(driver_id)

            return redirect(url_for('home_page'))


        else:

            driver_id = request.form['driver_assign']

            orderPickup = Order_Table_Pickup(date,request.form['FromName'],request.form['FromAddress'],
            request.form['FromCity'], request.form['FromZip'],default_time, default_time,"pickup",1, request.form['driver_assign'])

            orderDel = Order_Table_Del(date,request.form['ToName'],request.form['ToAddress'],
            request.form['ToCity'],request.form['ToZip'],default_time, default_time,"delivery",1, request.form['driver_assign'])

            db.session.add(orderPickup)
            db.session.add(orderDel)
            db.session.commit()

            update_driver_workload(driver_id)


            return redirect(url_for('home_page'))


    return render_template('new_order.html', driver_records = Drivers.query.all(), drivers = Drivers.query.all())

# Page to view orders by driver and day.
@app.route('/display_orders', methods = ['GET', 'POST'])
def display_orders():

    if request.args.get('driver'):

        driverID = request.args.get('driver')
        order_date = request.args.get('date')


        return render_template('display_orders.html', driver_records = Drivers.query.all(), dates = Workload.query.filter_by(driverID = 1).all(), total_stops = Workload.query.filter_by(driverID = driverID).filter_by(date = order_date).all() , Pickup = Order_Table_Pickup.query.filter_by(date = order_date).filter_by(driverID = driverID).all(), Delivery = Order_Table_Del.query.filter_by(date = order_date).filter_by(driverID = driverID).all())


    return render_template('display_orders.html', driver_records = Drivers.query.all(), dates = Workload.query.filter_by(driverID = 1).all())

# Page to view orders by driver and day.
@app.route('/manage_daily_orders', methods = ['GET', 'POST'])
def manage_daily_orders():

    order_date = datetime.now().date() # returns the date

    key = keys['GOOGLE_IFRAME_KEY']

    default_map = "44.9778, -93.2650"


    if request.method == 'POST':

        if request.form['button'] == 'Update Order':

            new_driver = request.form['new_driver']

            order_number = request.form['order_id_update']

            query = Order_Table_Pickup.query.filter_by(id = order_number).first()

            old_driver = query.driverID

            update_orders_table(order_number,new_driver, old_driver)

            return redirect(url_for('manage_daily_orders'))

        if request.form['button'] == 'Directions':

            order_number = request.form['Directions']

            pickquery = Order_Table_Pickup.query.filter_by(id = order_number).first()

            del_query = Order_Table_Del.query.filter_by(id = order_number).first()

            starting_address = pickquery.address + " " + pickquery.city + " " + pickquery.zip_code

            destination = del_query.address + " " + del_query.city + " " + del_query.zip_code

            if " " in starting_address:

                starting_address = starting_address.replace(" ", "+")
                destination = destination.replace(" ", "+")

            print(starting_address)
            print(destination)

            return render_template('manage_daily_orders.html', driver_records = Drivers.query.all(), date = order_date, Pickup = Order_Table_Pickup.query.filter_by(date = order_date).all(),
             Delivery = Order_Table_Del.query.filter_by(date = order_date).all(), orders = Order_Table_Del.query.filter_by(date = order_date).all(), origin = starting_address, dest = destination, key = key)

        else:

            order_number = request.form['order_id_delete']

            query = Order_Table_Pickup.query.filter_by(id = order_number).first()

            driver = query.driverID

            delete_order(order_number, driver)

            return redirect(url_for('manage_daily_orders'))





    return render_template('manage_daily_orders.html', driver_records = Drivers.query.all(), date = order_date, Pickup = Order_Table_Pickup.query.filter_by(date = order_date).all(),
     Delivery = Order_Table_Del.query.filter_by(date = order_date).all(), orders = Order_Table_Del.query.filter_by(date = order_date).all(), center = default_map, key = key)


# Had to add zones manually due to Zipcode API problems.
def add_zone_to_DB(zip_list, zone):

    anchor_list = ["55303","55356","55088","54016","55127"]

    for x in zip_list:

        if x == 55127:

            zip_entry = MN_Zipcodes(str(x), zone, True)

        else:


            zip_entry = MN_Zipcodes(str(x), zone, False)


        db.session.add(zip_entry)
        db.session.commit()



if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)

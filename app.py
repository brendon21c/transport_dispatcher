from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exists, and_
import itertools
from datetime import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport_db.sqlite3'
app.config['SECRET_KEY'] = "transportation"

db = SQLAlchemy(app)
from data_processing import *
from models import * # Needs to be after db, otherwise no tables are created.

zipcode_check = "new" # This is how the program checks to see if a new "zone" need to be creted/

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    #

    # create a new zone

    # Zones for testing
    # zip_code_list_1 = [55316,55448,55433,55434,55445,55443,55304,55444,55327,55303,55369,55569,55449,55432,55311,55429,55428,55430,55014,55442,55421,55011,55112,55374,55412,55446,55422,55126,55418,55427,55441,55340,55411,55413,55447]
    # zip_code_list_2 = [55305,55441,55447,55426,55345,55427,55343,55391,55446,55442,55436,55416,55422,55323,55361,55346,55424,55356,55405,55344,55428,55439,55410,55411,55392,55408,55403,55409,55429,55412,55435,55402,55401,55384,55419,55440,55458,55459,55460,55474,55478,55479,55480,55483,55484,55485,55486,55487,55488,55470,55472,55467,55404,55415,55317,55347,55430,55340,55331,55407,55594,55570,55571,55572,55574,55576,55577,55578,55579,55593,55348,55573,55454,55413,55455,55569,55414,55418,55595,55596,55597,55598,55599,55311,55423,55438,55369,55364,55445,55437,55406,55359,55421,55443,55417]
    # zip_code_list_3 = [55306,55044,55124,55337,55378,55372,55020,55122,55024,55054,55431,55437,55420,55068,55438,55425,55123,55121,55379,55010,55088,55423,55435,55347,55450,55439,55111,55120,55344,55077,55150,55419,55417,55424]
    # zip_code_list_4 = [55125,55129,55188,55119,55055,55128,55042,55075,55106,55001,55016,55101,55107,55170,55133,55144,55145,55146,55155,55164,55165,55175,55187,55109,55076,55071,55130,55043,55102,55077,55118,55090,55172,55103,55117,55003,55115,55120,55105,55082,55116,55104,55083,55150,54016,55110,55108,55113,55121,55123,55114,55111,55127,55033,55406,54082,55450,55417,55126,55414]
    # zip_code_list_5 = [55113,55108,55117,55114,55103,55413,55104,55418,55414,55455,55454,55130,55467,55415,55421,55472,55470,55488,55487,55486,55485,55484,55483,55458,55459,55460,55474,55478,55479,55480,55440,55112,55105,55401,55126,55406,55404,55402,55144,55187,55170,55133,55146,55145,55165,55155,55164,55175,55101,55172,55102,55411,55403,55127,55107,55412,55407,55116,55109,55106,55405,55430,55408,55432,55417]
    #
    # add_zone_to_DB(zip_code_list_5, 5)


    get_drivers = current_driver_list()

    assign_route_to_driver('55337')


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


        # if zipcode_check == "new":
        #
        #     query = Drivers.query.order_by(Drivers.id.desc()).first()
        #     zone_zip = query.starting_zipcode
        #     zone_num = query.delivery_zone
        #     print(zone_zip)
        #     zip_list = create_driver_zipcode_zone(zone_zip)
        #     add_zone_to_DB(zip_list, zone_num)




        return redirect(url_for('home_page'))


    return render_template('new_driver.html', zones = MN_Zipcodes.query.filter_by(anchor_zip = True).all())

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

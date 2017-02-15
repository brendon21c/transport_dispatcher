from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exists, and_
import itertools
import zipcode
from datetime import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport_db.sqlite3'
app.config['SECRET_KEY'] = "transportation"

db = SQLAlchemy(app)
from data_processing import *
from models import * # Needs to be after db, otherwise no tables are created.

zipcode_check = "new"

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    #

    if zipcode_check == "new":

        query = Drivers.query.order_by(Drivers.id.desc()).first()
        zone_num = query.starting_zipcode
        print(zone_num)
        zip_list = create_driver_zipcode_zone(zone_num)
        add_zone_to_DB(zip_list, zone_num)



    get_drivers = current_driver_list()



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

        zone = create_driver_zone(zip_code_form)

        driver = Drivers(request.form['first'], request.form['last'], request.form['address'], request.form['city'], request.form['zipcode'],
        request.form['truck'], zone, start_time, end_time)

        db.session.add(driver)
        db.session.commit()



        return redirect(url_for('home_page'))


    return render_template('new_driver.html')


def add_zone_to_DB(zip_list, zone):

    for x in range(len(zip_list)):

        print(zone + x)


if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)

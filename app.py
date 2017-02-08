from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exists, and_
import itertools
import zipcode
from datetime import *
from data_processing import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport_db.sqlite3'
app.config['SECRET_KEY'] = "transportation"

db = SQLAlchemy(app)
from models import * # Needs to be after db, otherwise no tables are created.


@app.route('/', methods = ['GET', 'POST'])
def home_page():
    #
    if request.method == 'POST':

        start_time = request.form['start_time']
        end_time = request.form['end_time']

        time_list = process_time_entry(start_time, end_time)

        start_time = time_list[0]
        end_time = time_list[1]

        driver = Drivers(request.form['first'], request.form['last'], request.form['address'], request.form['city'], request.form['zipcode'],
        request.form['truck'], start_time, end_time)

        db.session.add(driver)
        db.session.commit()

        return redirect(url_for('home_page'))



    check_time = is_driver_clocked_in(3)

    print(check_time)


        #check = check_driver_schedule(now, start, end)



    return render_template('home_page.html')





if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)

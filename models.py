from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app import db


class Drivers(db.Model):

    """ This table will contain all the information needed about drivers. """

    __tablename__ = 'drivers_table'

    id = db.Column('driver_id', db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    starting_address = db.Column(db.String(50))
    starting_city = db.Column(db.String(50))
    starting_zipcode = db.Column(db.String(50))
    truck_number = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __init__(self,first,last, address, city, zipcode, truck, start, end):

        self.first_name = first
        self.last_name = last
        self.starting_address = address
        self.starting_city = city
        self.starting_zipcode = zipcode
        self.truck_number = truck
        self.start_time = start
        self.end_time = end

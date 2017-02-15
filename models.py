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
    delivery_zone = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    def __init__(self,first,last, address, city, zipcode, truck, zone, start, end):

        self.first_name = first
        self.last_name = last
        self.starting_address = address
        self.starting_city = city
        self.starting_zipcode = zipcode
        self.truck_number = truck
        self.delivery_zone = zone
        self.start_time = start
        self.end_time = end

class MN_Zipcodes(db.Model):

    """table for managing zip codes and zones for the state of minnesota, overlap with
    zipcodes and zones might happen."""


    __tablename__ = 'minnesota_zones'

    id = db.Column('id_column', db.Integer, primary_key = True)
    zip_code = db.Column(db.Integer)
    delivery_zone = db.Column(db.Integer)



    def __init__(self, zip_code, zone):

        self.zip_code = zip_code
        self.delivery_zone = zone

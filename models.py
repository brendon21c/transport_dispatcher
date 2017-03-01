from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app import db


class Drivers(db.Model):

    """ This table will contain all the information needed about drivers. """

    __tablename__ = 'drivers_table'

    id = db.Column('DriverID', db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    starting_address = db.Column(db.String(50))
    starting_city = db.Column(db.String(50))
    starting_zipcode = db.Column(db.String(50))
    truck_number = db.Column(db.Integer)
    delivery_zone = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    orderPickup = relationship("Order_Table_Pickup")
    orderDel = relationship("Order_Table_Del")

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
    zipcodes and zones might happen. The anchor column is to identify zipcodes that act as
    "anchors" around the city to help with routing zip codes not listed in the database."""


    __tablename__ = 'minnesota_zones'

    id = db.Column('id_column', db.Integer, primary_key = True)
    zip_code = db.Column(db.String(50))
    delivery_zone = db.Column(db.Integer)
    anchor_zip = db.Column(db.Boolean)

    def __init__(self, zip_code, zone, anchor):

        self.zip_code = zip_code
        self.delivery_zone = zone
        self.anchor_zip = anchor

# Table setup for order Pickups
class Order_Table_Pickup(db.Model):

    __tablename__ = 'orderPickup'
    id = db.Column('OrderNum', db.Integer, primary_key = True)
    date = db.Column(db.Date)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    zip_code = db.Column(db.String(50))
    pick_time = db.Column(db.Time)
    del_time = db.Column(db.Time)
    driverID = db.Column(db.Integer, ForeignKey('drivers_table.DriverID'))


    def __init__(self, date, FromName, FromAddress, FromCity, FromZip, pickup, delivered, driverAssign):

        self.date = date
        self.name = FromName
        self.address = FromAddress
        self.city = FromCity
        self.zip_code = FromZip
        self.pick_time = pickup
        self.del_time = delivered
        self.driverID = driverAssign

# Table setup for order Deliveries
class Order_Table_Del(db.Model):

    __tablename__ = 'orderDel'
    id = db.Column('OrderNum', db.Integer, primary_key = True)
    date = db.Column(db.Date)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    zip_code = db.Column(db.String(50))
    pick_time = db.Column(db.Time)
    del_time = db.Column(db.Time)
    driverID = db.Column(db.Integer, ForeignKey('drivers_table.DriverID'))

    def __init__(self, date, ToName, ToAddress, ToCity, ToZip, pickup, delivered, driverAssign):

        self.date = date
        self.name = ToName
        self.address = ToAddress
        self.city = ToCity
        self.zip_code = ToZip
        self.pick_time = pickup
        self.del_time = delivered
        self.driverID = driverAssign

from models.configure import (
    Model, UNIQUE_ID, CREATED_ON, MODIFIED_ON, DELETED_ON
)
from sqlalchemy import Column, String, ForeignKey, Integer, SMALLINT, text
from flask_sqlalchemy import SQLAlchemy
__author__ = 'shashi'



class Booking(Model):

    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    parking_spot_id = Column(Integer)
    cost = Column(Integer,default = 100)
    # booking cost can be later on will be fetched from parking area cost table and can be shown
    # for now i added default value here .
    user_id = Column(Integer)
    is_booked = Column(Integer,default=1)
    created_on = CREATED_ON.copy()

    def to_dict(self):
        _d = dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        return _d

class User(Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    mobile = Column(String(31))
    email = Column(String(31))
    password = Column(String(31))
    #subscribe_email_ind = BOOLEAN_TRUE.copy()


    created_on = CREATED_ON.copy()

    def to_dict(self):
        _d = dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        return _d



class ParkingSpot(Model):

    __tablename__ = 'parking_spot'
    
    id = Column(Integer, primary_key=True)
    latitude = Column(String(30))
    longitude = Column(String(10))
    address = Column(String(10))
    reserved = Column(Integer)
    created_on = CREATED_ON.copy()

    def to_dict(self):
        _d = dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        return _d



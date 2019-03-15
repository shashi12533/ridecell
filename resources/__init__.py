from flask_cors import CORS
from flask_restful import Api

from resources.ride import Parking,Account,Bookings,AvailableParking,ReservedParking,FilterParking

__author__ = 'shashi rest api '


def create_restful_api(app):
    api = Api(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    api.add_resource(Parking, '/parkings' ,endpoint="get all parkings area")
    api.add_resource(AvailableParking, '/parkings/available',endpoint="get available parking")
    api.add_resource(ReservedParking, '/parkings/reserved',endpoint="get reserved parking")
    api.add_resource(FilterParking, '/parkings/search',endpoint="get parking nearby to your coordinates")
    api.add_resource(Bookings, '/bookings',endpoint="reserve a parking area")
    api.add_resource(Bookings, '/bookings/<string:booking_id>',endpoint="delete booking")
    api.add_resource(Account, '/user',endpoint="onboard user")
    
    
   
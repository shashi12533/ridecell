from flask_jwt import jwt_required, current_identity
from flask_restful import marshal_with, fields, reqparse
from models import session,Booking,User,ParkingSpot
from resources.base_resource import BaseResource as Resource
from flask import Response,request
import json
import datetime
import re
from math import sin, cos, sqrt, atan2, radians
from sqlalchemy import text
from resource_exception import handle_exceptions
from flask import request, jsonify
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from flask_bcrypt import Bcrypt
# from validation import validate_user
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity,JWTManager)
__author__ = 'shashi'


bcrypt = Bcrypt()



class Parking(Resource):

    decorators = [handle_exceptions()]
    @jwt_required
    def get(self):
        data_obj = session.query(ParkingSpot).all()
        parking_data=[]
        
        for data in data_obj:
            temp = data.to_dict()
            temp.pop('created_on')
            parking_data.append(temp)

        return Response(json.dumps(parking_data),  mimetype='application/json')

       
    decorators = [handle_exceptions()]
    def post(self):

        # this is used to populate the database 
        data ={}
        latitude = request.json.get('latitude')
        longitude = request.json.get('longitude')
        address = request.json.get('address')
        data.update({'latitude':latitude})
        data.update({'reserved':0})
        data.update({'longitude':longitude})
        data.update({'address':address})
        if latitude is None or longitude is None or address is None:
            return Response(json.dumps({'message':'please check your payload'}), status=400, mimetype='application/json')
        else:
            data_obj = ParkingSpot(**data)
            session.add(data_obj)
            session.commit()
            return Response(json.dumps({'message':'parking area successfully added'}), mimetype='application/json')


class Auth(Resource):
    def __init__(self):
        self.user_schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "password": {
                    "type": "string",
                    "minLength": 5
                }
            },
            "required": ["email", "password"],
            "additionalProperties": False
    }


    def validate_user(self,data):
        try:
            validate(data, self.user_schema)
        except ValidationError as e:
            return {'ok': False, 'message': e}
        except SchemaError as e:
            return {'ok': False, 'message': e}
        return {'ok': True, 'data': data}

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return str(o)


    def post(self):
        data = self.validate_user(request.get_json())
        if data['ok']:
            data = data['data']
            user = session.query(User).filter(User.email == data['email']).all()
            user = user[0].to_dict()
            import pdb
            pdb.set_trace()
            if user and bcrypt.check_password_hash(user['password'], data['password']):
                del user['password']
                access_token = create_access_token(identity=data)
                refresh_token = create_refresh_token(identity=data)
                user['token'] = access_token
                user['refresh'] = refresh_token
                m = json.dumps(user,default=self.default)
                return Response(m, mimetype='application/json')

            else:
                return Response(json.dumps({'data':'user not available'}), mimetype='application/json')

        else:
            return Response(json.dumps({'message':'bad request'}), mimetype='application/json')


class Register(Resource):
    def __init__(self):
        self.user_schema = {
            "type": "object",
            "properties": {
                "user_name": {
                    "type": "string",
                },
                 "first_name": {
                    "type": "string",
                },
                 "last_name": {
                    "type": "string",
                },
                 "mobile": {
                    "type": "string",
                },
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "password": {
                    "type": "string",
                    "minLength": 5
                }
            },
            "required": ["email", "password"],
            "additionalProperties": False
    }


    def validate_user(self,data):
        try:
            validate(data, self.user_schema)
        except ValidationError as e:
            return {'ok': False, 'message': e}
        except SchemaError as e:
            return {'ok': False, 'message': e}
        return {'ok': True, 'data': data}

    def post(self):
        data = self.validate_user(request.get_json())
        import pdb
        pdb.set_trace()
        if data['ok']:
            data = data['data']
            data['password'] = bcrypt.generate_password_hash(
                data['password'])
            obj = User(**data)
            session.add(obj)
            session.commit()
            return Response(json.dumps({'data':data}), mimetype='application/json')
        else:
            return Response(json.dumps({'message':'bad request'}), mimetype='application/json')






class AvailableParking(Resource):

    def get(self):

        data_obj = session.query(ParkingSpot).filter(ParkingSpot.reserved == 0).all()
        parking_data=[]
        
        for data in data_obj:
            temp = data.to_dict()
            temp.pop('created_on')
            parking_data.append(temp)

        return Response(json.dumps(parking_data),  mimetype='application/json')

class ReservedParking(Resource):

    def get(self):

        data_obj = session.query(ParkingSpot).filter(ParkingSpot.reserved == 1).all()
        parking_data=[]
        
        for data in data_obj:
            temp = data.to_dict()
            temp.pop('created_on')
            parking_data.append(temp)

        return Response(json.dumps(parking_data),  mimetype='application/json')

class FilterParking(Resource):

    def get(self,**kwargs):

        parking_data=[]
        lat1 = radians(float(request.args.get('lat')))
        lon1 = radians(float(request.args.get('lon')))
        inp_rad = int(request.args.get('radius'))
        data_obj = session.query(ParkingSpot).all()
        data_obj = [data.to_dict() for data in data_obj]
        parking_data=[]
        for data in data_obj:
            R = 6373.0
            lat2 = radians(float(data['latitude']))
            lon2 = radians(float(data['longitude']))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if distance <= inp_rad:
                data.pop('created_on')
                parking_data.append(data)



        return Response(json.dumps(parking_data),  mimetype='application/json')



class Account(Resource):

    def post(self):

        data ={}
        user_name = request.json.get('user_name')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        mobile = str(request.json.get('mobile'))
        if user_name is None or first_name is None or last_name is None or mobile is None:
            return Response(json.dumps({'message':'please check your payload'}), status=400, mimetype='application/json')

        data.update({'user_name':user_name})
        data.update({'first_name':first_name})
        data.update({'last_name':last_name})
        data.update({'mobile':mobile})
        # 1) Begins with 0 or 91 
        # 2) Then contains 7 or 8 or 9. 
        # 3) Then contains 9 digits 
        Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
        if Pattern.match(mobile):
            data_obj = User(**data)
            session.add(data_obj)
            session.commit()
            return Response(json.dumps({'message':'user account successfully created'}), mimetype='application/json')
        else:
            return Response(json.dumps({'message':'mobile number incorrect'}), status=400, mimetype='application/json')

        




class Bookings(Resource):


    def post(self):

        
        parking_spot_id= int(request.json.get('parking_spot_id'))
        user_id= int(request.json.get('user_id'))
        data ={}
        user_obj = session.query(User).filter(User.id == user_id).all()
        parking_obj = session.query(ParkingSpot).filter(ParkingSpot.id == parking_spot_id).all()
        user_obj_id = user_obj[0].to_dict()['id']
        parking_obj_id = parking_obj[0].to_dict()['id']
        parking_status = parking_obj[0].to_dict()['reserved']
        parking_obj = parking_obj[0].to_dict()
        if user_obj_id == user_id and parking_obj_id == parking_spot_id and parking_obj['reserved'] == 0:
            data.update({'user_id':user_id})
            data.update({'parking_spot_id': parking_spot_id})
            data_obj = Booking(**data)
            session.add(data_obj)
            session.commit()
            parking_obj['reserved'] =1
            parking_data = parking_obj
            parking = ParkingSpot(**parking_data)
            session.merge(parking)
            session.commit()
            return Response(json.dumps({'message':'booking successfully done'}),status=201,  mimetype='application/json')
        else:
            return Response(json.dumps({'message':'please check your parking area existence,sorry not booked'}),  mimetype='application/json')
        
        

    def delete(self,**kwargs):
        
        booking_id= int(kwargs.get('booking_id'))
        booking_obj = session.query(Booking).filter(Booking.id == booking_id).all()
        if len(booking_obj)==0:
            return Response(json.dumps({'message':'please check booking id'}),  mimetype='application/json')

        parking_spot_id = booking_obj[0].to_dict()['parking_spot_id']
        booking_obj_id = booking_obj[0].to_dict()['id']
        parking_obj = session.query(ParkingSpot).filter(ParkingSpot.id == parking_spot_id).all()
        parking_obj = parking_obj[0].to_dict()
        if booking_id == booking_obj_id and parking_obj['reserved'] == 1:
            obj=Booking.query.filter_by(id=booking_id).one()
            session.delete(obj)
            session.commit()
            parking_obj['reserved'] =0
            parking_data = parking_obj
            parking = ParkingSpot(**parking_data)
            session.merge(parking)
            session.commit()
            return Response(json.dumps({'message':'booking deleted successfully ','id':booking_id}),  mimetype='application/json')
        else:
            return Response(json.dumps({'message':'please check booking id'}),  mimetype='application/json')
        



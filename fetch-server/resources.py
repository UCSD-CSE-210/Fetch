from models.route import Route, RouteAdmin
from models.surface import Surface
from models.wildlife import WildlifeType, Wildlife
from flask import url_for
from flask_restful import reqparse, abort, Api, Resource, inputs, fields, marshal_with
from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import Point
from flask_security import current_user

from managers.wildlife_manager import WildlifeTypeManager, WildlifeManager
from managers.weather_manager  import WeatherManager
from managers.route_manager    import RouteManager

import json
import copy

import utils


api = utils.get_api()
db = utils.get_db()

# Managers
route_manager = RouteManager(db)
wildlifetype_manager = WildlifeTypeManager(db)
wildlife_manager = WildlifeManager(db)
weather_manager = WeatherManager(db)

# GET parameters for the search
search_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
search_parser.add_argument('id',              type=int,            store_missing=False)
search_parser.add_argument('name',            type=str,            store_missing=False)
search_parser.add_argument('zipcode',         type=str,            store_missing=False)
search_parser.add_argument('is_shade',        type=inputs.boolean, store_missing=False)
search_parser.add_argument('is_water',        type=inputs.boolean, store_missing=False)
search_parser.add_argument('is_garbage_can',  type=inputs.boolean, store_missing=False)
search_parser.add_argument('has_parking_lot', type=inputs.boolean, store_missing=False)
search_parser.add_argument('is_poop_bag',     type=inputs.boolean, store_missing=False)
search_parser.add_argument('surface',         type=str,            store_missing=False, choices=Surface.types)
search_parser.add_argument('min_distance',    type=float,          store_missing=False) # in miles
search_parser.add_argument('max_distance',    type=float,          store_missing=False) # in miles
search_parser.add_argument('latitude',        type=float)
search_parser.add_argument('longitude',       type=float)
search_parser.add_argument('radius',          type=float,          store_missing=False) # in miles

# GET parameters for wildlife
wildlife_type_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
wildlife_type_parser.add_argument('is_dangerous', type=inputs.boolean, store_missing=False)
wildlife_type_parser.add_argument('name', type=str, store_missing=False)

# POST parameters for wildlife types
wildlife_type_post_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
wildlife_type_post_parser.add_argument('is_dangerous', type=inputs.boolean, store_missing=False)
wildlife_type_post_parser.add_argument('name', type=str, store_missing=False)

# POST parameters for wildlife instances
wildlife_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
wildlife_parser.add_argument('wildlifetype', type=int, store_missing=False)
wildlife_parser.add_argument('location', type=dict, store_missing=False)
wildlife_parser.add_argument('is_dangerous', type=inputs.boolean, store_missing=False)
wildlife_parser.add_argument('route', type=int, store_missing=False)

# GET parameters for weather
weather_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
weather_parser.add_argument('temperature', type=int, store_missing=False)
weather_parser.add_argument('sunny', type=inputs.boolean, store_missing=False)
weather_parser.add_argument('cloudy', type=inputs.boolean, store_missing=False)
weather_parser.add_argument('rainy', type=inputs.boolean, store_missing=False)

# POST parameters for route liking
route_like_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
route_like_parser.add_argument('route_id', type=int, required=True)

class Coordinates(fields.Raw):
    def format(self, wkb):
        coords = to_shape(wkb).coords[:]
        return map(lambda (x,y): {'latitude'  : y,
                                  'longitude' : x}, 
                   coords)

class WildlifeTypeField(fields.Raw):
    def format(self, wt):
        wt_dict = copy.deepcopy(wt.__dict__)
        del wt_dict['_sa_instance_state']
        return wt_dict

class LocationField(fields.Raw):
    def format(self, loc):
        point = to_shape(loc).coords[:]
        return {
            'latitude'  : point[0][1],
            'longitude' : point[0][0]
        }

class RouteField(fields.Raw):
    def format(self, route):
        return {
            'id': route.id,
            'name': route.name,
            'zipcode': route.zipcode,
            'is_shade': route.is_shade,
            'is_water': route.is_water,
            'is_garbage_can': route.is_garbage_can,
            'is_poop_bag': route.is_poop_bag,
        }

class ImageField(fields.Raw):
    def format(self, imgs):
        return map(lambda img: {'image_id': img.id,
                                'image_url': url_for('download_image', image_id=img.id)},
                   imgs)

class WildlifeImageField(fields.Raw):
    def format(self, imgs):
        return map(lambda img: {'image_id': img.id,
                                'image_url': url_for('download_wildlife_image', image_id=img.id)},
                   imgs)

class WeatherField(fields.Raw):
    def format(self, weather):
        return {
            'id': weather.id,
            'temperature': weather.temperature,
            'cloudy': weather.cloudy,
            'sunny': weather.sunny,
            'rainy': weather.rainy
        }

route_fields = {
    'id'              : fields.Integer,
    'name'            : fields.String,
    'address'         : fields.String,
    'zipcode'         : fields.String,
    'is_shade'        : fields.Boolean,
    'is_water'        : fields.Boolean,
    'is_garbage_can'  : fields.Boolean,
    'is_poop_bag'     : fields.Boolean,
    'has_parking_lot' : fields.Boolean,
    'coodinates'      : Coordinates(attribute='path'),
    'images'          : ImageField(attribute='images'),
    'surface'         : fields.String,
    'distance'        : fields.Float,
    'weather'         : WeatherField,
    'like_count'      : fields.Integer(attribute=lambda r: len(r.likes)),
    'can_like'        : fields.Boolean(attribute=lambda r: current_user.has_role('user') and current_user not in r.likes)
}

wildlife_type_fields = {
    'id'             : fields.Integer,
    'name'           : fields.String,
    'is_dangerous'   : fields.Boolean
}

wildlife_fields = {
    'id' : fields.Integer,
    'wildlifetype' : WildlifeTypeField,
    'location': LocationField,
    'route': RouteField,
    'images': WildlifeImageField(attribute='images')
}

weather_fields = {
    'id'          : fields.Integer,
    'temperature' : fields.Integer,
    'sunny'       : fields.Boolean,
    'cloudy'      : fields.Boolean,
    'rainy'       : fields.Boolean,
    'timestamp'   : fields.Integer
}

# filter & respond to the search query
class RouteResource(Resource):
    '''
    Query parameters:
      id             : Route id
      name           : Route name
      address        : Route address (substring, case-insensitive)
      is_shade       : Has shade?
      is_water       : Has water?
      is_garbage_can : Has garbage can?
      is_poop_bag    : Has poop bag?
      surface        : Surface type of the route
      min_distance   : Min length of the route
      max_distance   : Max length of the route
      latitude       : Current location's latitude
      longitude      : Current location's longitude
      radius         : Used to search routes within the given radius to the current location
    
    - All parameters are optional. 
    - If an `id` is not given, search will be done on all routes with the rest
      of the given parameters.
    - Otherwise, the route with the given id (if exists) will be returned.
    
    JSON Response:
    { 'results' : [route1, route2, ...] }
    where each route object contains the following:
    id, name, address, is_shade, is_water, is_garbage_can, is_poop_bag, coodinates, images, surface, distance
    
    Coordinates is a list of objects that contain latitude and longitude fields
    Images is a list of objects that contain image_id and image_url fields.
    '''
    @marshal_with(route_fields, envelope='results')
    def get(self):
        args = search_parser.parse_args(strict=True)
        return route_manager.search(args)

class RouteLikeResource(Resource):    
    @marshal_with(route_fields, envelope='results')
    def post(self):
        args = route_like_parser.parse_args(strict=True)
        return route_manager.like(args)

        
class WildlifeTypeResource(Resource):
    '''
    Query parameters:
    1. is_dangerous - optional boolean
    '''
    @marshal_with(wildlife_type_fields, envelope='results')
    def get(self):
        args = wildlife_type_parser.parse_args(strict=True)
        return wildlifetype_manager.select(args)
    
    '''
    JSON payload
    {
        "name": "raccoon",
        "is_dangerous": true
    }
    '''
    @marshal_with(wildlife_type_fields, envelope='results')
    def post(self):
        args = wildlife_type_post_parser.parse_args(strict=True)
        return wildlifetype_manager.insert(args['name'], args['is_dangerous'])

class WildlifeResource(Resource):
    '''
    Query parameters:
    1. is_dangerous - optional boolean
    2. name - optional string
    3. route - int
    '''
    @marshal_with(wildlife_fields, envelope='results')
    def get(self):
        args = wildlife_parser.parse_args(strict=True)
        return wildlife_manager.select(args.get('route'), args.get('is_dangerous'))

    '''
    JSON payload
    {
        "wildlifetype": 1,
        "location": {
            "latitude": 100.0,
            "longitude": 123.23
        },
        "route": 2
    }
    '''
    @marshal_with(wildlife_fields, envelope='results')
    def post(self):
        args = wildlife_parser.parse_args(strict=True)
        lat = args['location']['latitude']
        lon = args['location']['longitude']
        wildlifetype = args['wildlifetype']
        route = args['route']
        return wildlife_manager.insert(lat, lon, wildlifetype, route)

class WeatherResource(Resource):
    '''
    Query parameters:
    1. temperature - optional int
    2. cloudy - optional boolean
    3. rainy - optional boolean
    4. sunny - optional boolean
    '''
    @marshal_with(weather_fields, envelope='results')
    def get(self):
        args = weather_parser.parse_args(strict=True)
        return weather_manager.select(args)
    
    '''
    JSON payload example
    {
        "temperature": 95,
        "cloudy": false,
        "rainy": false,
        "sunny": true
    }
    '''
    @marshal_with(weather_fields, envelope='results')
    def post(self):
        args = weather_parser.parse_args(strict=True)
        temperature = args['temperature']
        sunny = args['sunny']
        cloudy = args['cloudy']
        rainy = args['rainy']
        return weather_manager.insert(temperature, sunny, cloudy, rainy)

# Add the resources to the app
api.add_resource(RouteResource, '/api/route')
api.add_resource(RouteLikeResource, '/api/route_like')
api.add_resource(WildlifeTypeResource, '/api/wildlifetype')
api.add_resource(WildlifeResource, '/api/wildlife')
api.add_resource(WeatherResource, '/api/weather')

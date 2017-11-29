from models.route import Route, RouteAdmin
from models.surface import Surface
from models.wildlife import WildlifeType, Wildlife
from flask import url_for
from flask_restful import reqparse, abort, Api, Resource, inputs, fields, marshal_with
from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import Point

import json
import copy

import utils


api = utils.get_api()
db = utils.get_db()

def surface_type_checker(value):
    if value not in Surface.types:
        raise ValueError("Surface type is not valid")
    return value

# GET parameters for the search
search_parser = reqparse.RequestParser(trim=True, bundle_errors=True)
search_parser.add_argument('id',              type=int,                  store_missing=False)
search_parser.add_argument('name',            type=str,                  store_missing=False)
search_parser.add_argument('address',         type=str,                  store_missing=False)
search_parser.add_argument('is_shade',        type=inputs.boolean,       store_missing=False)
search_parser.add_argument('is_water',        type=inputs.boolean,       store_missing=False)
search_parser.add_argument('is_garbage_can',  type=inputs.boolean,       store_missing=False)
search_parser.add_argument('has_parking_lot', type=inputs.boolean,       store_missing=False)
search_parser.add_argument('is_poop_bag',     type=inputs.boolean,       store_missing=False)
search_parser.add_argument('surface',         type=surface_type_checker, store_missing=False)

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
        print point
        return {
            'latitude'  : point[0][0],
            'longitude' : point[0][1]
        }

class ImageField(fields.Raw):
    def format(self, imgs):
        return map(lambda img: {'image_id': img.id,
                                'image_url': url_for('download_image', image_id=img.id)},
                   imgs)

route_fields = {
    'id'              : fields.Integer,
    'name'            : fields.String,
    'address'         : fields.String,
    'is_shade'        : fields.Boolean,
    'is_water'        : fields.Boolean,
    'is_garbage_can'  : fields.Boolean,
    'is_poop_bag'     : fields.Boolean,
    'has_parking_lot' : fields.Boolean,
    'coodinates'      : Coordinates(attribute='path'),
    'images'          : ImageField(attribute='images'),
    'surface'         : fields.String,
    'distance'        : fields.Float
}

wildlife_type_fields = {
    'id'             : fields.Integer,
    'name'           : fields.String,
    'is_dangerous'   : fields.Boolean
}

wildlife_fields = {
    'id' : fields.Integer,
    'wildlifetype' : WildlifeTypeField,
    'location': LocationField
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
    
    - All parameters are optional. 
    - If an `id` is not given, search will be done on all routes with the rest
      of the given parameters.
    - Otherwise, the route with the given id (if exists) will be returned.
    
    JSON Response:
    { 'results' : [route1, route2, ...] }
    where each route object contains the following:
    id, name, address, is_shade, is_water, is_garbage_can, is_poop_bag, coodinates, images
    
    Coordinates is a list of objects that contain latitude and longitude fields
    Images is a list of objects that contain image_id and image_url fields.
    '''
    @marshal_with(route_fields, envelope='results')
    def get(self):
        args = search_parser.parse_args(strict=True)
        print "args:", args
        if 'id' not in args:
            q = Route.query

            if 'name' in args:
                name = args['name']
                args.pop('name')
                q = q.filter(Route.name.ilike('%'+name+'%'))

            if 'address' in args:
                address = args['address']
                args.pop('address')
                q = q.filter(Route.address.ilike('%'+address+'%'))

            if 'surface' in args:
                surface = args['surface']
                args.pop('surface')
                q = q.filter(Route.surface.has(name=surface))

            results = q.filter_by(**args).all()
            return results
        else:
            route = Route.query.get(args['id'])
            return [route] if route is not None else []
    
class WildlifeTypeResource(Resource):
    '''
    Query parameters:
    1. is_dangerous - optional boolean
    '''
    @marshal_with(wildlife_type_fields, envelope='results')
    def get(self):
        args = wildlife_type_parser.parse_args(strict=True)
        q = WildlifeType.query
        results = q.filter_by(**args).all()
        return results
    
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
        wt = WildlifeType(name         = args['name'],
                          is_dangerous = args['is_dangerous'])
        db.session.add(wt)
        db.session.commit()
        return wt

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
        q = Wildlife.query
        if 'route' in args:
            q = q.filter(Wildlife.route_id == args['route'])
        if 'is_dangerous' in args:
            q = q.filter(Wildlife.wildlifetype.has(is_dangerous=args['is_dangerous']))
        return q.all()

    '''
    JSON payload
    {
        "wildlifetype": 1,
        "location": {
            "latitude": 100.0,
            "longitude": 123.23
        }
    }
    '''
    @marshal_with(wildlife_fields, envelope='results')
    def post(self):
        args = wildlife_parser.parse_args(strict=True)
        point = [args['location']['latitude'], args['location']['longitude']]
        wildlife = Wildlife(wildlifetype_id = args['wildlifetype'],
                            location = from_shape(Point(point)))
        db.session.add(wildlife)
        db.session.commit()
        return wildlife


# Add the resources to the app
api.add_resource(RouteResource, '/api/route')
api.add_resource(WildlifeTypeResource, '/api/wildlifetype')
api.add_resource(WildlifeResource, '/api/wildlife')

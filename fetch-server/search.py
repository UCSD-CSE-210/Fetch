from models.route import Route, RouteAdmin
from flask_restful import reqparse, abort, Api, Resource, inputs, fields, marshal_with
from geoalchemy2.shape import to_shape
import utils

api = utils.get_api()

# GET parameters for the search
parser = reqparse.RequestParser(trim=True, bundle_errors=True)
parser.add_argument('id'             , type=int,  store_missing=False)
parser.add_argument('name'           , type=str,  store_missing=False)
parser.add_argument('address'        , type=str,  store_missing=False)
parser.add_argument('is_shade'       , type=inputs.boolean, store_missing=False)
parser.add_argument('is_water'       , type=inputs.boolean, store_missing=False)
parser.add_argument('is_garbage_can' , type=inputs.boolean, store_missing=False)
parser.add_argument('is_poop_bag'    , type=inputs.boolean, store_missing=False)

# JSON response
# { 'results' : [ route1, route2, ...] }
# where each route has the following fields:

class Coordinates(fields.Raw):
    def format(self, wkb):
        coords = to_shape(wkb).coords[:]
        return map(lambda (x,y): [x,y], coords)

route_fields = {
    'id'             : fields.Integer,
    'name'           : fields.String,
    'address'        : fields.String,
    'is_shade'       : fields.Boolean,
    'is_water'       : fields.Boolean,
    'is_garbage_can' : fields.Boolean,
    'is_poop_bag'    : fields.Boolean,
    'coodinates'     : Coordinates(attribute='path')
}

# filter & respond to the search query
class RouteSearch(Resource):
    @marshal_with(route_fields, envelope='results')
    def get(self):
        args = parser.parse_args(strict=True)
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
            results = q.filter_by(**args).all()
            return results
        else:
            route = Route.query.get(args['id'])
            return [route] if route is not None else []

api.add_resource(RouteSearch, '/api/search')


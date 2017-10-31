from models.route import Route, RouteAdmin
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
import utils

api = utils.get_api()

# GET parameters for the search
parser = reqparse.RequestParser(trim=True, bundle_errors=True)
parser.add_argument('id'             , type=int,  store_missing=False)
parser.add_argument('name'           , type=str,  store_missing=False)
parser.add_argument('address'        , type=str,  store_missing=False)
parser.add_argument('is_shade'       , type=bool, store_missing=False)
parser.add_argument('is_water'       , type=bool, store_missing=False)
parser.add_argument('is_garbage_can' , type=bool, store_missing=False)
parser.add_argument('is_poop_bag'    , type=bool, store_missing=False)

# JSON response
# { 'results' : [ route1, route2, ...] }
# where each route has the following fields:
route_fields = {
    'id'             : fields.Integer,
    'name'           : fields.String,
    'address'        : fields.String,
    'is_shade'       : fields.Boolean,
    'is_water'       : fields.Boolean,
    'is_garbage_can' : fields.Boolean,
    'is_poop_bag'    : fields.Boolean
}

# filter & respond to the search query
class RouteSearch(Resource):
    @marshal_with(route_fields, envelope='results')
    def get(self):
        args = parser.parse_args(strict=True)
        print args
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
            return q.filter_by(**args).all()
        else:
            route = Route.query.get(args['id'])
            return [route] if route is not None else []

api.add_resource(RouteSearch, '/api/search')


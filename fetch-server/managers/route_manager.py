from sqlalchemy import func, asc
from flask_security import current_user

try:
  from ..models.route import Route
  from .. import utils
except ValueError:
  from models.route import Route
  import utils

class RouteManager():
    def __init__(self, db):
        self.db = db
        self.feature_flags = ['is_shade', 
                              'is_water', 
                              'is_garbage_can', 
                              'has_parking_lot', 
                              'is_poop_bag']
        self.filters = [('name',         self.filter_name),
                        ('surface',      self.filter_surface),
                        ('min_distance', self.filter_min_distance),
                        ('max_distance', self.filter_max_distance)]
        self.zipcodes = utils.get_zipcodes()

    def search(self, args):
        if 'id' in args:
            route = Route.query.get(args['id'])
            return [route] if route is not None else []

        q = Route.query
        
        # ######################################################################
        # filter only if the following features are wanted
        # (i.e. ignores if they are not wanted)
        # ######################################################################
        for f in self.feature_flags:
            if f in args and args[f]:
                q = q.filter_by(**{f : True})
        # ######################################################################
        # handle parameters that require special care
        # ######################################################################
        for (arg,call) in self.filters:
            q = self.update_filter(q, args, arg, call)
        # ######################################################################
        # handle geographical filters
        # ######################################################################
        latitude  = args['latitude']  if 'latitude'  in args else None
        longitude = args['longitude'] if 'longitude' in args else None
        zipcode   = args['address']   if 'address'   in args else None
        
        sql_point = None

        if latitude is not None and longitude is not None:
            sql_point = self.latlong_to_sql({'latitude'  : latitude,
                                             'longitude' : longitude})
        elif zipcode is not None and zipcode in self.zipcodes: 
            sql_point = self.latlong_to_sql(self.zipcodes[zipcode])
            
        if sql_point is not None:
            q = q.order_by(func.ST_Distance(Route.path, sql_point).asc())
            
            if 'radius' in args:
                radius = args['radius']
                q = q.filter(func.ST_Distance(Route.path, sql_point) <= 1609.34 * radius)
        # ######################################################################

        results = q.all()
        return results
    
    def like(self, args):
      route_id = args['route_id']
      r = Route.query.get(route_id)

      if r is None or not current_user.has_role('user'):
        return []

      if current_user not in r.likes:
        r.likes.append(current_user)
        self.db.session.add(r)
        self.db.session.commit()

      return [r]
        

    def update_filter(self, q, args, arg_name, call):
        if arg_name in args:
            arg = args[arg_name]
            return call(q, arg)
        else:
            return q
    
    def filter_name(self, q, name):
        return q.filter(Route.name.ilike('%'+name+'%'))
    
    def filter_address(self, q, address):
        return q.filter(Route.address.ilike('%'+address+'%'))
    
    def filter_surface(self, q, surface):
        return q.filter(Route.surface.has(name=surface))
    
    def filter_min_distance(self, q, min_distance):
        return q.filter(Route.distance >= min_distance)

    def filter_max_distance(self, q, max_distance):
        return q.filter(Route.distance <= max_distance)

    def latlong_to_sql(self, coord):
        t = 'SRID=%d;POINT(%.6f %.6f)' % (utils.get_default_srid(), coord['longitude'], coord['latitude'])
        return func.ST_GeogFromText(t)

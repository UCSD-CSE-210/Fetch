from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from fetch_test import FetchTestCase
from managers.route_manager import RouteManager
from geoalchemy2.shape import to_shape

from models.surface import Surface
from models.route import Route

import os.path as op
import json

try:
    from .. import utils
except ValueError:
    import utils
    
srid = utils.get_default_srid()

class RouteTestCase(FetchTestCase):
  def setUp(self):
    super(RouteTestCase, self).setUp()
    self.manager = RouteManager(self.db)
    self.add_routes()
    self.ucsd_cse_latlong = {'latitude'  :   32.881864,
                             'longitude' : -117.233322}
    self.petco_latlong    = {'latitude'  :   32.869370,
                             'longitude' : -117.231178}

  def test_empty(self):
    with self.app.app_context():
      self.assertEqual(len(self.manager.search({})), 9)
  
  # TODO: validate these orderings...
  def test_ordering(self):
    routes = self.manager.search(self.ucsd_cse_latlong)
    names  = ["UCSD", 
              "Par Course Trails", 
              "Torrey Pines", 
              "La Jolla Shores", 
              "Rose Canyon", 
              "Deerfield loop",
              "Mission Trails Visitor Loop",
              "Balboa Park",
              "Cowles Mountain Trail"] 
    self.assertEqual(map(lambda r: r.name, routes), names)

    routes2 = self.manager.search(self.petco_latlong)
    names2  = ["UCSD", 
               "Rose Canyon",
               "Par Course Trails", 
               "La Jolla Shores", 
               "Torrey Pines", 
               "Balboa Park", 
               "Deerfield loop", 
               "Mission Trails Visitor Loop", 
               "Cowles Mountain Trail"]
    self.assertEqual(map(lambda r: r.name, routes2), names2)

  def add_routes(self):
    # insert the surface types
    surface_types = {}
    for type_name in Surface.types:
        st = Surface(name=type_name)
        surface_types[type_name] = st
        self.db.session.add(st)
    self.db.session.commit()
    
    with open(op.join(op.dirname(op.realpath(__file__)), 'routes.json')) as data_file:    
      for r in json.load(data_file):
        rt = Route(name            = r['name'],
                   address         = r['address'],
                   is_shade        = r['is_shade'],
                   is_water        = r['is_water'],
                   is_garbage_can  = r['is_garbage_can'],
                   is_poop_bag     = r['is_poop_bag'],
                   has_parking_lot = r['has_parking_lot'],
                   surface         = surface_types[r['surface']],
                   path            = 'SRID=%d;%s' % (srid, r['pathstr']))
        self.db.session.add(rt)
      self.db.session.commit()

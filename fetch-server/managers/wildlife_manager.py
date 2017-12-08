try:
  from ..models.wildlife import Wildlife, WildlifeType
  from ..models.route import Route
except ValueError:
  from models.wildlife import Wildlife, WildlifeType
  from models.route import Route

from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import Point

class WildlifeTypeManager():
  def __init__(self, db):
    self.db = db
    self.q = WildlifeType.query

  def select(self, args):
    return self.q.filter_by(**args).all()
  
  def insert(self, name, is_dangerous):
    wt = WildlifeType(name = name, is_dangerous = is_dangerous)
    self.db.session.add(wt)
    self.db.session.commit()
    return wt

class WildlifeManager():
  def __init__(self, db):
    self.db = db

  def select(self, route, is_dangerous):
    q = Wildlife.query
    if route is not None:
      q = q.filter(Wildlife.route_id == route)
    if is_dangerous is not None:
      q = q.filter(Wildlife.wildlifetype.has(is_dangerous=is_dangerous))
    return q.all()

  def insert(self, lat, lon, wildlifetype, routeid):
    point = [lon, lat]
    location = from_shape(Point(point))
    wildlife = Wildlife(wildlifetype_id = wildlifetype,
                        location = location,
                        route_id = routeid)
    self.db.session.add(wildlife)
    self.db.session.commit()
    return wildlife

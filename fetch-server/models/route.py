from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_admin.contrib.geoa import ModelView
from flask_security import current_user
from sqlalchemy.event import listens_for
from geoalchemy2.types import Geography
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
from sqlalchemy import func

import surface

try:
    from .. import utils
except ValueError:
    import utils

db  = utils.get_db()

class Route(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True)

    name            = db.Column(db.String(255))
    address         = db.Column(db.String(255))
    is_shade        = db.Column(db.Boolean())
    is_water        = db.Column(db.Boolean())
    is_garbage_can  = db.Column(db.Boolean())
    is_poop_bag     = db.Column(db.Boolean())
    has_parking_lot = db.Column(db.Boolean())

    # srid:2877 also looks interesting ...
    path            = db.Column(Geography(geometry_type='LINESTRING', srid=utils.get_default_srid()))
    # should be in miles
    distance        = db.Column(db.Float())

    images          = db.relationship('RouteImage')
    surface_id      = db.Column(db.Integer, db.ForeignKey('surface.id'), nullable=False)
    surface         = db.relationship('Surface')
    

    def __str__(self):
        return self.name

@listens_for(Route, 'after_insert')
def update_path_distance(mapper, connection, target):
    print type(target.path), target.id, target.path
    # db.session.query(Route).filter_by(id=target.id).update({'distance': 0})
    # db.session.commit()

class RouteAdmin(ModelView):
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('superuser')

    def scaffold_form(self):
        form_class = super(RouteAdmin, self).scaffold_form()
        return form_class

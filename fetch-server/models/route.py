from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_admin.contrib.geoa import ModelView
from flask_security import current_user
from geoalchemy2.types import Geometry

from image import RouteImage

try:
    from .. import utils
except ValueError:
    import utils

db = utils.get_db()

class Route(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True)

    name           = db.Column(db.String(255))
    address        = db.Column(db.String(255))

    is_shade       = db.Column(db.Boolean())
    is_water       = db.Column(db.Boolean())
    is_garbage_can = db.Column(db.Boolean())
    is_poop_bag    = db.Column(db.Boolean())

    path           = db.Column(Geometry("LINESTRING"))

    images         = db.relationship('RouteImage')

    def __str__(self):
        return self.name

class RouteAdmin(ModelView):
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('superuser')

    def scaffold_form(self):
        form_class = super(RouteAdmin, self).scaffold_form()
        return form_class

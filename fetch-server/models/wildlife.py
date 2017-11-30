from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_security import current_user
from flask_admin.contrib.geoa import ModelView
from geoalchemy2.types import Geometry
from route import Route

try:
    from .. import utils
except ValueError:
    import utils

db = utils.get_db()

class WildlifeType(db.Model):
    __tablename__ = 'wildlifetype'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(255))
    is_dangerous  = db.Column(db.Boolean())

    def __str__(self):
        return self.name

class WildlifeTypeAdmin(ModelView):
    column_auto_select_related = True

    form_excluded_columns = ('wildlife',)

    def is_accessible(self):
        return current_user.has_role('superuser')

class Wildlife(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    wildlifetype_id = db.Column(db.Integer, db.ForeignKey('wildlifetype.id'))
    wildlifetype    = db.relationship("WildlifeType")
    location        = db.Column(Geometry("POINT"))
    images          = db.relationship('WildlifeImage')
    route_id        = db.Column(db.Integer, db.ForeignKey('route.id'))
    route           = db.relationship('Route')

class WildlifeAdmin(ModelView):
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('superuser')
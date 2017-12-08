from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_security import current_user
from flask_admin.contrib.geoa import ModelView
from geoalchemy2.types import Geometry

try:
    from .. import utils
except ValueError:
    import utils

db = utils.get_db()

class Weather(db.Model):
    __tablename__ = 'weather'
    id            = db.Column(db.Integer, primary_key=True)
    temperature   = db.Column(db.Integer)
    sunny         = db.Column(db.Boolean)
    cloudy        = db.Column(db.Boolean)
    rainy         = db.Column(db.Boolean)

    def __str__(self):
        return str(self.temperature)

class WeatherAdmin(ModelView):
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('superuser')
 
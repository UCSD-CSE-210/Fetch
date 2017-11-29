from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

from sqlalchemy import func

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

api = Api(app)

def get_db():
    return db

def get_app():
    return app

def get_api():
    return api

def get_default_srid():
    return 4326

def get_ucsdcse_latlong():
    return {'latitude':    32.881833, 
            'longitude': -117.233336}

def latlong_to_sql(coord):
    return func.ST_GeogFromText('SRID=%d;POINT(%.6f %.6f)' % (get_default_srid(), coord['longitude'], coord['latitude']))

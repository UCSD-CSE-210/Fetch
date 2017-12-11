from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
import csv
import os.path as op

app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_FILE')
CORS(app)
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

def get_zipcodes():
    zipcodes = {}
    with open(op.join(op.dirname(op.realpath(__file__)), 'zipcodes.csv')) as data_file:    
        csvreader = csv.reader(data_file, delimiter=',')
        for row in csvreader:
            zipcodes[row[0]] = {"latitude": row[1], "longitude": row[2]}
        return zipcodes

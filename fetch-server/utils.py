from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

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


from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from models.user import User, Role, UserAdmin
from models.route import Route, RouteAdmin
import utils
from flask_security import SQLAlchemyUserDatastore, Security, login_required
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with

app = utils.get_app()
api = utils.get_api()

# Initialize sqlalchemy here
db = utils.get_db()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Initialize the admin interface
admin = Admin(app, name='fetch', template_mode='bootstrap3')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RouteAdmin(Route, db.session))

# Displays the home page.
@app.route('/')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
@login_required
def index():
    return render_template('index.html')

# ------------------------------------------------------------------------------

parser = reqparse.RequestParser()
parser.add_argument('id'             , type=int)
parser.add_argument('name'           , type=str)
parser.add_argument('is_shade'       , type=bool)
parser.add_argument('is_water'       , type=bool)
parser.add_argument('is_garbage_can' , type=bool)
parser.add_argument('is_poop_bag'    , type=bool)

route_fields = {
    'id'             : fields.Integer,
    'name'           : fields.String,
    'address'        : fields.String,
    'is_shade'       : fields.Boolean,
    'is_water'       : fields.Boolean,
    'is_garbage_can' : fields.Boolean,
    'is_poop_bag'    : fields.Boolean
}

class RouteSearch(Resource):
    @marshal_with(route_fields)
    def get(self):
        args = parser.parse_args()
        if args['id'] is None:
            return Route.query.all()
        else:
            return Route.query.get(args['id'])

api.add_resource(RouteSearch, '/api/search')

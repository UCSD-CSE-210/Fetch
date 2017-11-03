from flask import Flask, render_template, send_from_directory
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from models.user import User, Role, UserAdmin
from models.route import Route, RouteAdmin
from models.wildlife import WildlifeType, WildlifeTypeAdmin, Wildlife, WildlifeAdmin
from models.image import Image, ImageAdmin

import utils

import resources

from flask_security import SQLAlchemyUserDatastore, Security, login_required

app = utils.get_app()

# Initialize sqlalchemy here
db = utils.get_db()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Initialize the admin interface
admin = Admin(app, name='fetch', template_mode='bootstrap3')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RouteAdmin(Route, db.session))
admin.add_view(WildlifeTypeAdmin(WildlifeType, db.session))
admin.add_view(WildlifeAdmin(Wildlife, db.session))
admin.add_view(ImageAdmin(Image, db.session))

# displays the home page.
@app.route('/')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
@login_required
def index():
    return render_template('index.html')

@app.route('/images/<path:filename>')
def download_image(filename):
    return send_from_directory(app.config['FS_IMAGES_ROOT'],
                               filename,
                               as_attachment=True)

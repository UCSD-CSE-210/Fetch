from flask import Flask, render_template, send_from_directory, request, jsonify, abort, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from models.image import Image, ImageAdmin
from models.route import Route, RouteAdmin
from models.user import User, Role, UserAdmin
from models.wildlife import WildlifeType, WildlifeTypeAdmin, Wildlife, WildlifeAdmin

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

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# displays the home page.
@app.route('/')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
@login_required
def index():
    return render_template('index.html')

@login_required
@app.route('/image/<int:image_id>')
def download_image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        abort(404)
    return send_from_directory(app.config['FS_IMAGES_ROOT'],
                               image.path,
                               as_attachment=False)

@login_required
@app.route('/upload_image', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'image' in request.files:
            path = images.save(request.files['image'])
            image = Image(path=path)
            db.session.add(image)
            db.session.commit()
            return jsonify({'result': 'success',
                            'image': {'id': image.id,
                                      'url': url_for('download_image',
                                                     image_id=image.id)}})
        return jsonify({'result': 'failure'})
    else:
        return render_template('upload.html')


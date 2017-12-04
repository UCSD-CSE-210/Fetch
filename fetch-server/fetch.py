from flask import Flask, render_template, send_from_directory, request, jsonify, abort, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from models.image import RouteImage, RouteImageAdmin, WildlifeImage, WildlifeImageAdmin
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
admin.add_view(RouteImageAdmin(RouteImage, db.session))
admin.add_view(WildlifeImageAdmin(WildlifeImage, db.session))

route_images = UploadSet('route', IMAGES, default_dest=(lambda app: app.config['FS_ROUTE_IMAGES_ROOT']))
wildlife_images = UploadSet('wildlife', IMAGES, default_dest=(lambda app: app.config['FS_WILDLIFE_IMAGES_ROOT']))
configure_uploads(app, route_images)
configure_uploads(app, wildlife_images)

# displays the home page.
@app.route('/')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
@login_required
def index():
    return render_template('index.html')

'''
Returns the image with the given identifier
'''
@login_required
@app.route('/api/image/route/<int:image_id>')
def download_image(image_id):
    image = RouteImage.query.get(image_id)
    if image is None:
        abort(404)
    return send_from_directory(app.config['FS_ROUTE_IMAGES_ROOT'],
                               image.path,
                               as_attachment=False)

@login_required
@app.route('/api/image/wildlife/<int:image_id>')
def download_wildlife_image(image_id):
    image = WildlifeImage.query.get(image_id)
    if image is None:
        abort(404)
    return send_from_directory(app.config['FS_WILDLIFE_IMAGES_ROOT'],
                            image.path,
                            as_attachment=False)

def failure_msg(msg):
    return jsonify({'result': 'failure',
                    'message': msg })

'''
A form with enctype="multipart/form-data" should be sent to this address. It
should contain the following fields:

<input type="file" name="image" />
<input type="text" name="route_id" />

The input "route_id" should contain the id of the route that image should be
added to.

'''
@login_required
@app.route('/api/upload_route_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        route_id = request.form.get('route_id', default=-1, type=int)

        if route_id < 0 or 'image' not in request.files:
            return failure_msg('Missing parameter(s)')

        route = Route.query.get(route_id)

        if route is None:
            return failure_msg('Route "%d" does not exist' % (route_id))

        path = route_images.save(request.files['image'])
        image = RouteImage(path=path)
        route.images.append(image)
        db.session.add(image)
        db.session.add(route)
        db.session.commit()

        return jsonify({'result': 'success',
                        'image': {'id': image.id,
                                  'url': url_for('download_image',
                                                 image_id=image.id)}})
    else:
        return render_template('upload.html')

@app.route('/api/upload_wildlife_image', methods=['GET', 'POST'])
def upload_wildlife_image():
    if request.method == 'POST':
        wildlife_id = request.form.get('wildlife_id', default=-1, type=int)
        if wildlife_id < 0:
            return failure_msg('Missing wildlife id')
        if 'wildlife_image' not in request.files:
            return failure_msg('Missing image')
        
        wildlife = Wildlife.query.get(wildlife_id)

        if wildlife is None:
            return failure_msg('Wildlife "%d" does not exist' % (wildlife_id))
        
        path = wildlife_images.save(request.files['wildlife_image'])
        image = WildlifeImage(path=path)
        wildlife.images.append(image)
        db.session.add(image)
        db.session.add(wildlife)
        db.session.commit()

        return jsonify({'result': 'success',
                        'image': {'id': '1',
                                  'url': url_for('download_wildlife_image',
                                                 image_id='1')}})
    else:
        return render_template('upload_wildlife.html')

@app.route('/api/route_like')
def route_like_page():
    return render_template('like.html')

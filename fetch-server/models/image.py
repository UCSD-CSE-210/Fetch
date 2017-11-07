from flask import url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from jinja2 import Markup
from sqlalchemy.event import listens_for
import os
import os.path as op

try:
    from .. import utils
except ValueError:
    import utils

db  = utils.get_db()
app = utils.get_app()

class RouteImage(db.Model):
    __tablename__ = 'image'
    id       = db.Column(db.Integer, primary_key=True)
    path     = db.Column(db.Unicode(255))
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))

    def __unicode__(self):
        prefix = str(self.id) + ":"
        return prefix.encode("utf-8").decode("utf-8") + self.path

    def get_fullpath(self):
        return op.join(app.config['FS_ROUTE_IMAGES_ROOT'], self.path)

class RouteImageAdmin(ModelView):
    column_list = ('path', 'image')

    def _list_thumbnail(view, context, model, value):
        if not model.path:
            return ''

        return Markup('<img src="%s" style="max-height:300px;max-width:300px;height:auto;width:auto;">' % url_for('download_image', image_id=model.id))

    column_formatters = {
        'image': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('RouteImage',
                                      allow_overwrite=False,
                                      base_path=app.config['FS_ROUTE_IMAGES_ROOT'])
    }

    def is_accessible(self):
        return current_user.has_role('superuser')

@listens_for(RouteImage, 'after_delete')
def del_image(mapper, connection, target):
    # Delete image
    try:
        os.remove(target.get_fullpath())
    except OSError:
        pass

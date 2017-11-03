from flask import url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
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

class Image(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    path = db.Column(db.Unicode(255))

    def __unicode__(self):
        return self.name

class ImageAdmin(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('download_image',
                                                 filename=form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=app.config['FS_IMAGES_ROOT'],
                                      thumbnail_size=(100, 100, True))
    }

@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        root = app.config['FS_IMAGES_ROOT']
        # Delete image
        try:
            os.remove(op.join(root, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(root,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass

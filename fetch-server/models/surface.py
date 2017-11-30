from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView

try:
    from .. import utils
except ValueError:
    import utils

db = utils.get_db()

'''
This class is used like an enum. The different types of surfaces described
below should be created first in the database.
'''
class Surface(db.Model):
    # surface types
    types = ['urban', 'trail'] 

    # database columns
    __tablename__   = 'surface'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(255))
    
    def __str__(self):
        return self.name


class SurfaceAdmin(ModelView):
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('superuser')


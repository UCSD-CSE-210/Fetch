import os

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://fetch_db:fetch_db@localhost/fetch_db'

SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# FIXME: what to do about this MAP_ID ?
# MAPBOX_MAP_ID       = 'mapbox.mapbox-streets-v7'
MAPBOX_MAP_ID       ='petrusjvr.mbhn4pjj'

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZmV0Y2gwMDEiLCJhIjoiY2o5Z2VwYTVxMnY0dTMzcndibGlrY242dyJ9.0it-uEXRGgddk0XGHVbcgg'


# FS_IMAGES_ROOT = '~/fetch_fs/images'
FS_IMAGES_ROOT = os.path.join(os.getenv('HOME'), 'fetch_fs', 'images')

UPLOADED_IMAGES_DEST = FS_IMAGES_ROOT

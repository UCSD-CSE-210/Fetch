import utils
from fetch import app, user_datastore, wildlife_images

from models.user import Role
from models.route import Route
from models.surface import Surface
from models.wildlife import WildlifeType
from models.image import RouteImage, WildlifeImage

from managers.wildlife_manager import WildlifeTypeManager, WildlifeManager

from shapely.geometry import LineString
from geoalchemy2.shape import from_shape
import os, errno, sys
import os.path as op
import json
from werkzeug.datastructures import FileStorage


if 'IMAGE_ROOT_FOLDER' in os.environ:
    IMAGE_ROOT_FOLDER = os.environ['IMAGE_ROOT_FOLDER']
else:
    print "need to pass IMAGE_ROOT_FOLDER as an env var"
    sys.exit(1)
    
def build_demo_db(db):
    db.drop_all()
    db.create_all()

    with app.app_context():
        # ######################################################################
        # users
        # ######################################################################

        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password='admin',
            roles=[user_role, super_user_role]
        )

        # ######################################################################
        # surface types
        # ######################################################################
        
        surface_types = {}
        for type_name in Surface.types:
            st = Surface(name=type_name)
            surface_types[type_name] = st
            db.session.add(st)
            
        # ######################################################################
        # wildlife types
        # ######################################################################

        wtm = WildlifeTypeManager(db)
        
        rattlesnake = wtm.insert("Rattlesnake", True)
        raccoon     = wtm.insert("Raccoon",     True)
        coyote      = wtm.insert("Coyote",      True)

        rs_tup = (rattlesnake, "rattlesnake.jpg")
        rc_tup = (raccoon,     "raccoon.jpg")
        co_tup = (coyote,      "coyote.jpg")

        # ######################################################################
        # adding wildlife & images to routes
        # ######################################################################
        
        routes = {}
        
        with open(op.join(op.dirname(op.realpath(__file__)), 'test', 'routes.json')) as data_file:    
            srid = utils.get_default_srid()

            for r in json.load(data_file):
                name = str(r['name'])
                rt = Route(name            = name,
                           address         = str(r['address']),
                           is_shade        = r['is_shade'],
                           is_water        = r['is_water'],
                           is_garbage_can  = r['is_garbage_can'],
                           is_poop_bag     = r['is_poop_bag'],
                           has_parking_lot = r['has_parking_lot'],
                           surface         = surface_types[r['surface']],
                           path            = 'SRID=%d;%s' % (srid, r['pathstr']))
                
                db.session.add(rt)
                routes[name] = rt

        # flush to get ids of wildlife, route, etc.
        db.session.flush()
        
        # ######################################################################
        # adding wildlife & images to routes
        # ######################################################################

        route_images = {}

        r_info = {'Rose Canyon'                 : {"wildlife" : [rs_tup, co_tup], 
                                                   "images"   : []}, 

                  'Torrey Pines'                : {"wildlife" : [rc_tup],
                                                   "images"   : []}, 

                  'La Jolla Shores'             : {"wildlife" : [rc_tup],
                                                   "images"   : []}, 

                  'Deerfield loop'              : {"wildlife" : [],
                                                   "images"   : []}, 

                  'Mission Trails Visitor Loop' : {"wildlife" : [],
                                                   "images"   : []},

                  'Cowles Mountain Trail'       : {"wildlife" : [co_tup],
                                                   "images"   : []}, 

                  'Balboa Park'                 : {"wildlife" : [], 
                                                   "images"   : []}, 

                  'Par Course Trails'           : {"wildlife" : [rs_tup], 
                                                   "images"   : []},

                  'UCSD'                        : {"wildlife" : [], 
                                                   "images"   : []}
        }

        wm = WildlifeManager(db)

        for name in r_info:
            assert name in routes
            rt = routes[name]

            for wildlife_type, wildlife_image_name in r_info[name]['wildlife']:
                lat, lng = (0,0)
                
                assert wildlife_type.id > 0 and rt.id > 0
                wildlife_instance = wm.insert(lat, lng, wildlife_type.id, rt.id)

                with open(op.join(IMAGE_ROOT_FOLDER, 'wildlife', wildlife_image_name), 'rb') as fp:
                    path           = wildlife_images.save(FileStorage(fp))
                    wildlife_image = WildlifeImage(path=unicode(path))
                    wildlife_instance.images.append(wildlife_image)
                    db.session.add(wildlife_instance)
                    db.session.add(wildlife_image)
        
        # ######################################################################
        # done adding stuff, now commit
        # ######################################################################

        db.session.commit()

    return

if __name__ == '__main__':
    db  = utils.get_db()
    app = utils.get_app()
    
    for d in ['FS_IMAGES_ROOT', 
              'FS_ROUTE_IMAGES_ROOT',
              'FS_WILDLIFE_IMAGES_ROOT']:
        try:
            os.makedirs(app.config[d])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    build_demo_db(db)

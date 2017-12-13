import os, errno, sys
import os.path as op
import json

import utils
from fetch import app, user_datastore, wildlife_images, route_images

from models.user     import Role
from models.route    import Route
from models.surface  import Surface
from models.wildlife import WildlifeType
from models.image    import RouteImage, WildlifeImage

from managers.wildlife_manager import WildlifeTypeManager, WildlifeManager
from managers.weather_manager  import WeatherManager

from shapely.geometry import LineString
from geoalchemy2.shape import from_shape
from werkzeug.datastructures import FileStorage

if 'IMAGE_ROOT_FOLDER' in os.environ:
    IMAGE_ROOT_FOLDER = os.environ['IMAGE_ROOT_FOLDER']
else:
    print "need to pass IMAGE_ROOT_FOLDER as an env var"
    sys.exit(1)
    
blacklisted_routes = ['UCSD']
    
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

        user1 = user_datastore.create_user(
            first_name='User1',
            email='user1',
            password='user1',
            roles=[user_role]
        )

        user2 = user_datastore.create_user(
            first_name='User2',
            email='user2',
            password='user2',
            roles=[user_role]
        )

        user3 = user_datastore.create_user(
            first_name='User3',
            email='user3',
            password='user3',
            roles=[user_role]
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
        otherwl     = wtm.insert("Other",       True)

        rs_tup = (rattlesnake, "rattlesnake.jpg")
        rc_tup = (raccoon,     "raccoon.jpg")
        co_tup = (coyote,      "coyote.jpg")

        # ######################################################################
        # adding wildlife & images to routes
        # ######################################################################
        
        routes = {}
        weatherManager = WeatherManager(db)
        
        with open(op.join(op.dirname(op.realpath(__file__)), 'test', 'routes.json')) as data_file:    
            srid = utils.get_default_srid()

            for r in json.load(data_file):
                name = str(r['name'])
                if name in blacklisted_routes:
                    continue

                w  = weatherManager.insert(r["weather"]["temperature"],
                                           r["weather"]["sunny"],
                                           r["weather"]["cloudy"],
                                           r["weather"]["rainy"])

                rt = Route(name            = name,
                           address         = str(r['address']),
                           zipcode         = str(r['zipcode']),
                           is_shade        = r['is_shade'],
                           is_water        = r['is_water'],
                           is_garbage_can  = r['is_garbage_can'],
                           is_poop_bag     = r['is_poop_bag'],
                           has_parking_lot = r['has_parking_lot'],
                           surface         = surface_types[r['surface']],
                           weather         = w,
                           path            = 'SRID=%d;%s' % (srid, r['pathstr']))
                
                db.session.add(rt)
                routes[name] = rt

        # flush to get ids of wildlife, route, etc.
        db.session.flush()
        
        # ######################################################################
        # adding wildlife & images to routes
        # ######################################################################

        r_info = {'Rose Canyon'                 : {"wildlife" : [(rs_tup, 32.846425, -117.234018), 
                                                                 (co_tup, 32.842309, -117.234618)], 
                                                   "route"    : ["01_Devin-Go-Pro-Recap-3.jpg",
                                                                 "19_Wroe-Addi-Roothie-proof-2014-2-300x300.jpg",
                                                                 "02_dog_running_grass_trail_106484_1920x1080.jpg"],
                                                   "likes"    : [user1, user2, user3]}, 

                  'Torrey Pines'                : {"wildlife" : [(rc_tup, 32.915889, -117.256696)],
                                                   "route"    : ["03_MG_6586.jpg",
                                                                 "04_n02089867_2365.jpg"],
                                                   "likes"    : []}, 

                  'La Jolla Shores'             : {"wildlife" : [(rc_tup, 32.875135, -117.250941)],
                                                   "route"    : ["05_n02091032_3886.jpg",
                                                                 "06_n02091635_2089.jpg"],
                                                   "likes"    : [user1, user3]}, 

                  'Deerfield Loop'              : {"wildlife" : [],
                                                   "route"    : ["07_n02093754_6453.jpg",
                                                                 "08_n02094258_2842.jpg"],
                                                   "likes"    : [user1, user2, user3]}, 

                  'Mission Trails Visitor Loop' : {"wildlife" : [],
                                                   "route"    : ["09_n02094433_3881.jpg",
                                                                 "10_n02095314_1835.jpg"],
                                                   "likes"    : [user2]},

                  'Cowles Mountain Trail'       : {"wildlife" : [(co_tup, 32.809915, -117.031812)],
                                                   "route"    : ["11_n02096585_1624.jpg",
                                                                 "12_n02099267_1274.jpg"],
                                                   "likes"    : []}, 

                  'Balboa Park'                 : {"wildlife" : [], 
                                                   "route"    : ["13_n02100735_5978.jpg",
                                                                 "18_trailrun_1000.jpg",
                                                                 "14_n02102318_8534.jpg"],
                                                   "likes"    : [user1, user2]}, 

                  'Par Course Trails'           : {"wildlife" : [(rs_tup, 32.886725, -117.237773)], 
                                                   "route"    : ["15_n02112706_549.jpg",
                                                                 "16_n02113023_3885.jpg",
                                                                 "17_Short Distance Breeds.jpg"],
                                                   "likes"    : [user3]}
        }
        
        wm = WildlifeManager(db)

        for name in r_info:
            assert name in routes
            rt = routes[name]

            assert rt.id > 0

            # first, add wildlifes
            for ((wildlife_type, wildlife_image_name), lat, lng) in r_info[name]['wildlife']:
                
                assert wildlife_type.id > 0
                wildlife_instance = wm.insert(lat, lng, wildlife_type.id, rt.id)

                with open(op.join(IMAGE_ROOT_FOLDER, 'wildlife', wildlife_image_name), 'rb') as fp:
                    path           = wildlife_images.save(FileStorage(fp))
                    wildlife_image = WildlifeImage(path=unicode(path))
                    wildlife_instance.images.append(wildlife_image)
                    db.session.add(wildlife_instance)
                    db.session.add(wildlife_image)
                    
            # second, add dog images
            for dog_image_name in r_info[name]['route']:
                with open(op.join(IMAGE_ROOT_FOLDER, 'route', dog_image_name), 'rb') as fp:
                    path      = route_images.save(FileStorage(fp))
                    dog_image = RouteImage(path=unicode(path))
                    rt.images.append(dog_image)

            # finally add the likes
            for u in r_info[name]['likes']:
                rt.likes.append(u)

            db.session.add(rt)
        
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

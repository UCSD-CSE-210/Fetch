import utils
from fetch import app, user_datastore
from models.user import Role
from models.route import Route
from models.surface import Surface
from models.wildlife import WildlifeType
from shapely.geometry import LineString
from geoalchemy2.shape import from_shape
import os, errno

def build_sample_db(db):
    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password='admin',
            roles=[user_role, super_user_role]
        )
        db.session.commit()
        
        # insert the surface types
        surface_types = {}
        for type_name in Surface.types:
            st = Surface(name=type_name)
            surface_types[type_name] = st
            db.session.add(st)
        db.session.commit()
        
        path1 = [[-117.236271500587, 32.8783077126596], [-117.234329581261, 32.8786140640161], [-117.234061360359, 32.8771543804097], [-117.233363986015, 32.8769291184529]]
        route1 = Route(name            = "route 1",
                       address         = "gilman dr",
                       is_garbage_can  = True,
                       is_poop_bag     = False,
                       is_shade        = False,
                       is_water        = False,
                       has_parking_lot = True,
                       surface         = surface_types['trail'],
                       path            = from_shape(LineString(path1)))

        path2 = [[-117.233954071999, 32.8820469288637], [-117.234104275703, 32.8817946493596], [-117.234104275703, 32.8809927561667], [-117.235563397408, 32.8809927561667], [-117.237580418587, 32.879307855821], [-117.237569689751, 32.8791907225207], [-117.238685488701, 32.8781455262187], [-117.238827645779, 32.8781365158522], [-117.238913476467, 32.8775508400632], [-117.239235341549, 32.8776184182363]]
        route2 = Route(name            = "from CSE to Art",
                       address         = "UCSD",
                       is_garbage_can  = True,
                       is_poop_bag     = False,
                       is_shade        = False,
                       is_water        = True,
                       has_parking_lot = False,
                       surface         = surface_types['trail'],
                       path            = from_shape(LineString(path2)))
        
        rattlesnake = WildlifeType(name = "Rattlesnake",
                                   is_dangerous = True)

        #rattlesnake_instance = Wildlife(wildlifetype_id = rattlesnake.id)

        db.session.add(route1)
        db.session.add(route2)
        db.session.add(rattlesnake)
        #db.session.add(rattlesnake_instance)
        db.session.commit()

    return

if __name__ == '__main__':
    db = utils.get_db()
    build_sample_db(db)

    app = utils.get_app()

    for d in ['FS_IMAGES_ROOT', 
              'FS_ROUTE_IMAGES_ROOT',
              'FS_WILDLIFE_IMAGES_ROOT']:
        try:
            os.makedirs(app.config[d])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

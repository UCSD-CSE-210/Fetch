import utils
from fetch import app, user_datastore
from models.user import Role
from models.route import Route

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
        
        route1 = Route(name           ='route 1',
                       address        ='address 1',
                       is_shade       = True,
                       is_water       = False,
                       is_garbage_can = True,
                       is_poop_bag    = False)
        route2 = Route(name           ='route 2',
                       address        ='address 2',
                       is_shade       = True,
                       is_water       = True,
                       is_garbage_can = True,
                       is_poop_bag    = True)
        route3 = Route(name           ='route 3',
                       address        ='address 3',
                       is_shade       = True,
                       is_water       = True,
                       is_garbage_can = False,
                       is_poop_bag    = False)
        db.session.add(route1)
        db.session.add(route2)
        db.session.add(route3)
        db.session.commit()
    return

if __name__ == '__main__':
    db = utils.get_db()
    build_sample_db(db)

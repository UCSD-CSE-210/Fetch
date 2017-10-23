import utils
from fetch import app, user_datastore
from models.user import Role

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
    return

if __name__ == '__main__':
    db = utils.get_db()
    build_sample_db(db)
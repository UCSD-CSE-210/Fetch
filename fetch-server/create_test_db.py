import utils

from models.user import Role
from models.route import Route
from models.wildlife import WildlifeType

if __name__ == 'main':
  db = utils.get_db()
  db.drop_all()
  db.create_all()
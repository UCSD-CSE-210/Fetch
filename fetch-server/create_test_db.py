import utils

from models.user import Role
from models.route import Route
from models.wildlife import WildlifeType
from models.weather import Weather

if __name__ == 'main':
  db = utils.get_db()
  db.drop_all()
  db.create_all()
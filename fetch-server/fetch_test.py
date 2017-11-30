import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models.user import Role
from models.route import Route
from models.wildlife import WildlifeType

import utils

class FetchTestCase(unittest.TestCase):
  def setUp(self):
    self.db = utils.get_db()
    self.db.drop_all()
    self.db.create_all()
    self.app = utils.get_app()
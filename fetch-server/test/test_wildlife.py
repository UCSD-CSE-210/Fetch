from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from fetch_test import FetchTestCase
from managers.wildlife_manager import WildlifeTypeManager

import utils

class WildlifeTypeTestCase(FetchTestCase):
  def setUp(self):
    super(WildlifeTypeTestCase, self).setUp()
    self.manager = WildlifeTypeManager(self.db)

  def test_empty(self):
    with self.app.app_context():
      assert self.manager.select({}) == []

  def test_add_wt(self):
    with self.app.app_context():
      self.manager.insert('Rattlesnake', True)
      wildlifetypes = self.manager.select({})
      snake = wildlifetypes[0]
      assert snake.is_dangerous
      assert snake.name == 'Rattlesnake'

  def test_simple_queries(self):
    with self.app.app_context():
      self.manager.insert('Rattlesnake', True)
      wildlifetypes = self.manager.select({'is_dangerous': True})
      snake = wildlifetypes[0]
      assert snake.is_dangerous
      assert snake.name == 'Rattlesnake'
      wildlifetypes = self.manager.select({'is_dangerous': False})
      assert len(wildlifetypes) == 0

class WildlifeTestCase(FetchTestCase):
  def setUp(self):
    super(WildlifeTestCase, self).setUp()
    self.manager = WildlifeManager(self.db)
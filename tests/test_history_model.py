from unittest import TestCase

from src.setup import db
from .test_lost_item_model import get_new_user


class TestHistory(TestCase):
    def setUp(self):
        self.db = db
        self.db.create_all()
        self.user = get_new_user()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

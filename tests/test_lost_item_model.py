from unittest import TestCase

from mimesis import Generic, Person

from src.model import Laptop, User
from src.setup import db
from src.utilities import Generator


def get_new_user() -> User:
    person = Person()
    username = person.username()
    email = person.email(domains=["gmail.com", "yahoo.com"])
    password = person.password(length=25)
    user = User(username=username, email=email, password=password)
    user, error = user.save()
    return user


class TestLostItem(TestCase):
    def setUp(self):
        self.db = db
        self.db.create_all()
        self.generic = Generic("en")

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_laptop_model(self):
        user = get_new_user()

        laptop1 = Laptop(user.uid)
        self.db.session.add(laptop1)
        self.db.session.commit()

    def test_cell_phone_model(self):
        self.fail()

    def test_vehicle_model(self):
        self.fail()

from unittest import TestCase

from mimesis import Person

from src.model import User
from src.setup import db


class UserModelTest(TestCase):
    def setUp(self):
        self.db = db
        self.db.create_all()
        self.person = Person()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_user_table(self):
        self.assertTrue(self.db.engine.has_table(User.__tablename__))

    def test_user_mode(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user = User(username=username, email=email, password=password)
        self.assertIsNotNone(user)
        self.user = user

    def test_user_save(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user = User(username=username, email=email, password=password)

        user, error = user.save()

        self.assertFalse(error)
        self.assertIsInstance(user, User)
        self.assertNotIsInstance(user, str)
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)

    def test_user_duplicate_error(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user = User(username=username, email=email, password=password)
        user.save()

        user2 = User(username=username, email=email, password=password)
        user2, error = user2.save()
        self.assertTrue(error)
        self.assertTrue("duplicate key value violates unique constraint" in user2)

    def test_add_user_in_bulk(self):
        users = list()
        length = 30
        for _ in range(length):
            username = self.person.username()
            email = self.person.email(domains=["gmail.com", "aol.com"])
            password = self.person.password(length=50)
            users.append(User(username, email, password))
        self.db.session.add_all(users)

        self.assertTrue(User.query.count() >= length)

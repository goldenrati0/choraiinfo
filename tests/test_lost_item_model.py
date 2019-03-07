import random
from typing import List
from unittest import TestCase

from mimesis import Generic, Person

from src.model import Laptop, User, LostItem, Vehicle, CellPhone
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

    def test_lost_item_parent_class(self):
        user = get_new_user()
        laptop1 = Laptop(user.uid, serial_number=self.generic.hardware.cpu_model_code(),
                         mac_address=self.generic.hardware.cpu_codename())
        self.db.session.add(laptop1)
        self.db.session.commit()

        self.assertTrue(isinstance(laptop1, LostItem))
        self.assertTrue(isinstance(laptop1, Laptop))
        self.assertFalse(isinstance(laptop1, Vehicle))

        self.assertTrue(hasattr(laptop1, "uid"))
        self.assertTrue(hasattr(laptop1, "item_type"))
        self.assertTrue(hasattr(laptop1, "is_stolen"))
        self.assertTrue(hasattr(laptop1, "gd_copy_number"))
        self.assertTrue(hasattr(laptop1, "remarks"))
        self.assertTrue(hasattr(laptop1, "record_time"))
        self.assertTrue(hasattr(laptop1, "last_update"))

    def test_models_equality(self):
        user = get_new_user()
        # ### Laptop equality ###
        laptop1 = Laptop(user.uid, serial_number=self.generic.hardware.cpu_model_code(),
                         mac_address=self.generic.hardware.cpu_codename())
        self.db.session.add(laptop1)
        self.db.session.commit()
        searched_laptop = Laptop.query.get(laptop1.uid)
        self.assertTrue(laptop1, searched_laptop)
        self.assertTrue(laptop1.__eq__(searched_laptop))

        # ### CellPhone equality ###
        cellphone1 = CellPhone(user.uid, imei_1=self.generic.code.imei())
        cellphone1.save()
        searched_cellphone = CellPhone.query.get(cellphone1.uid)
        self.assertTrue(cellphone1, searched_cellphone)
        self.assertTrue(cellphone1.__eq__(searched_cellphone))

        # ### Vehicle equality ###
        vehicle1 = Vehicle(user.uid, serial_number=self.generic.hardware.cpu_model_code() + Generator.uuid(),
                           engine_number=self.generic.hardware.cpu_model_code() + Generator.uuid())
        vehicle1.save()
        searched_vehicle = Vehicle.query.get(vehicle1.uid)
        self.assertTrue(vehicle1, searched_vehicle)
        self.assertTrue(vehicle1.__eq__(searched_vehicle))

    def test_laptop_model(self):
        user = get_new_user()

        laptop1 = Laptop(user.uid, serial_number=self.generic.hardware.cpu_model_code(),
                         mac_address=self.generic.hardware.cpu_codename())
        self.db.session.add(laptop1)
        self.db.session.commit()

        self.assertIsNotNone(laptop1.uid)
        self.assertEqual(laptop1.owner.uid, user.uid)

    def test_laptop_owner(self):
        user = get_new_user()

        laptop1 = Laptop(user.uid, serial_number=self.generic.hardware.cpu_model_code(),
                         mac_address=self.generic.hardware.cpu_codename())
        self.db.session.add(laptop1)
        self.db.session.commit()

        self.assertEqual(laptop1.owner, user)

    def test_laptop_insert_in_bulk(self):
        users: List[User] = [get_new_user() for _ in range(40)]
        laptops: List[Laptop] = list()
        length = 5

        for _ in range(length):
            laptops.append(
                Laptop(random.choice(users).uid,
                       serial_number=self.generic.hardware.cpu_model_code() + Generator.uuid(),
                       mac_address=self.generic.hardware.cpu_codename() + Generator.uuid())
            )
        db.session.add_all(laptops)
        db.session.commit()

        query_laptops = Laptop.query.all()
        self.assertTrue(len(query_laptops) == length)

    def test_cell_phone_model(self):
        self.fail()

    def test_vehicle_model(self):
        self.fail()

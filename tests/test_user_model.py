import datetime
from typing import Dict, Any
from unittest import TestCase

from mimesis import Person, Generic

from src.model import User, UserLevelEnum, Laptop, ItemTypeEnum, CellPhone, Vehicle
from src.setup import db
from src.utilities import Generator


class TestUserModel(TestCase):
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
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertIsInstance(user.joined_at, datetime.datetime)

    def test_user_repr(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user = User(username=username, email=email, password=password)
        user, error = user.save()
        self.assertFalse(error)

        user_string = str(user)
        self.assertIsNotNone(user_string)

    def test_user_check_password(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user = User(username=username, email=email, password=password)
        user.save()

        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password("wrong password"))

    def test_user_json_property(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user = User(username=username, email=email, password=password)
        user.save()

        user_json: Dict[str, Any] = user.json

        self.assertEqual(user_json.get("uid"), user.uid)
        self.assertEqual(user_json.get("username"), user.username)
        self.assertEqual(user_json.get("email"), user.email)

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
        length = 5
        for _ in range(length):
            username = self.person.username()
            email = self.person.email(domains=["gmail.com", "aol.com"])
            password = self.person.password(length=50)
            users.append(User(username, email, password))
        self.db.session.add_all(users)

        self.assertTrue(User.query.count() >= length)

    def test_user_level(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user_level = UserLevelEnum.ADMIN
        user = User(username=username, email=email, password=password, _user_level=user_level)
        user.save()

        self.assertEqual(user._user_level, user_level)

    def test_user_address(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user_level = UserLevelEnum.USER
        user = User(username=username, email=email, password=password, _user_level=user_level)
        user.save()

        self.assertDictEqual(user.address, {})

        address = {
            "area": "Mohakhali",
            "city": "Dhaka",
            "thana": {
                "name": "Banani",
                "zip": 1213
            }
        }

        user, err = user.update(address=address)
        self.assertFalse(err)

        self.assertDictEqual(user.address, address)
        self.assertEqual(user.address.get("city"), address.get("city"))

    def test_user_phone(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user_level = UserLevelEnum.SUPER_ADMIN
        user = User(username=username, email=email, password=password, _user_level=user_level)
        user.save()

        self.assertListEqual(user.phones, [])

        phones = ["01711111110", "01600000001"]
        user, err = user.update(phones=phones)
        self.assertFalse(err)

        self.assertListEqual(user.phones, phones)
        self.assertEqual(len(user.phones), len(phones))

    def test_user_update_in_bulk(self):
        users = list()
        length = 3
        for _ in range(length):
            username = self.person.username()
            email = self.person.email(domains=["gmail.com", "aol.com"])
            password = self.person.password(length=50)
            users.append(User(username, email, password))
        self.db.session.add_all(users)

        User.update_all(users, address={"city": "Dhaka"})
        self.assertTrue(any(user.address != {} for user in users))

        for user in users:
            self.assertEqual(user.address.get("city"), "Dhaka")

    def test_user_delete(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user_level = UserLevelEnum.SUPER_ADMIN
        user = User(username=username, email=email, password=password, _user_level=user_level)
        user.save()

        find_user: User = User.query.filter(
            User.username == username
        ).first()
        self.assertIsNotNone(find_user)

        find_user.delete()

        find_user: User = User.query.filter(
            User.username == username
        ).first()
        self.assertIsNone(find_user)

    def test_user_relationship_laptops(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user_level = UserLevelEnum.MODERATOR
        user = User(username=username, email=email, password=password, _user_level=user_level)
        user.save()

        laptop1 = Laptop(user.uid, serial_number="unique_serial_" + Generator.uuid(),
                         mac_address="unique_mac_" + Generator.uuid(), is_stolen=True)
        laptop2 = Laptop(user.uid, serial_number="unique_serial_" + Generator.uuid(),
                         mac_address="unique_mac_" + Generator.uuid(),
                         remarks="This laptop is imported and genuine operating system installed.")

        user.laptops.append(laptop1)
        user.laptops.append(laptop2)
        db.session.commit()

        find_user = User.query.get(user.uid)
        self.assertIsNotNone(find_user)

        self.assertTrue(find_user.laptops != [])
        self.assertEqual(len(find_user.laptops), 2)

        self.assertTrue(laptop1.owner == laptop2.owner)

        laptops = [laptop1, laptop2]
        for index, laptop in enumerate(laptops):
            self.assertEqual(find_user.laptops[index].uid, laptops[index].uid)
            self.assertEqual(find_user.laptops[index].item_type, ItemTypeEnum.LAPTOP)
            self.assertEqual(find_user.laptops[index].is_stolen, laptops[index].is_stolen)
            self.assertEqual(find_user.laptops[index].gd_copy_number, laptops[index].gd_copy_number)
            self.assertEqual(find_user.laptops[index].remarks, laptops[index].remarks)
            self.assertEqual(find_user.laptops[index].remarks, laptops[index].remarks)
            self.assertEqual(find_user.laptops[index].record_time, laptops[index].record_time)
            self.assertEqual(find_user.laptops[index].last_update, laptops[index].last_update)

            self.assertEqual(find_user.laptops[index].serial_number, laptops[index].serial_number)
            self.assertEqual(find_user.laptops[index].mac_address, laptops[index].mac_address)

    def test_user_relationship_cellphones(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user_level = UserLevelEnum.USER
        user = User(username=username, email=email, password=password, _user_level=user_level)
        user.save()

        generic = Generic("en")

        phone1 = CellPhone(user.uid, imei_1=generic.code.imei())
        phone2 = CellPhone(user.uid, imei_1=generic.code.imei(), imei_2=generic.code.imei(),
                           remarks="Dual sim phone.", is_stolen=True, gd_copy_number=f"GD-{Generator.uuid()}")
        phone3 = CellPhone(user.uid, imei_2=generic.code.imei(), is_stolen=False,
                           remarks="Oneek bhaalo phone!")

        user.cell_phones.append(phone1)
        user.cell_phones.append(phone2)
        user.cell_phones.append(phone3)
        db.session.commit()

        find_user = User.query.get(user.uid)
        self.assertIsNotNone(find_user)

        self.assertTrue(find_user.cell_phones != [])
        self.assertEqual(len(find_user.cell_phones), 3)

        self.assertTrue(phone1.owner == phone2.owner == phone3.owner)

        phones = [phone1, phone2, phone3]
        for index, _ in enumerate(phones):
            self.assertEqual(find_user.cell_phones[index].uid, phones[index].uid)
            self.assertEqual(find_user.cell_phones[index].item_type, ItemTypeEnum.CELL_PHONE)
            self.assertEqual(find_user.cell_phones[index].is_stolen, phones[index].is_stolen)
            self.assertEqual(find_user.cell_phones[index].gd_copy_number, phones[index].gd_copy_number)
            self.assertEqual(find_user.cell_phones[index].remarks, phones[index].remarks)
            self.assertEqual(find_user.cell_phones[index].remarks, phones[index].remarks)
            self.assertEqual(find_user.cell_phones[index].record_time, phones[index].record_time)
            self.assertEqual(find_user.cell_phones[index].last_update, phones[index].last_update)

            self.assertEqual(find_user.cell_phones[index].imei_1, phones[index].imei_1)
            self.assertEqual(find_user.cell_phones[index].imei_2, phones[index].imei_2)

    def test_user_relationship_vehicles(self):
        username = self.person.username()
        email = self.person.email(domains=["gmail.com"])
        password = self.person.password(length=25)
        user_level = UserLevelEnum.ADMIN
        user = User(username=username, email=email, password=password, _user_level=user_level)
        user.save()

        vehicle1 = Vehicle(user.uid, serial_number=f"serial-{Generator.uuid()}")
        vehicle2 = Vehicle(user.uid,
                           serial_number=f"serial-{Generator.uuid()}",
                           engine_number=f"engine_{Generator.uuid()}")
        vehicle3 = Vehicle(user.uid,
                           serial_number=f"serial-{Generator.uuid()}",
                           engine_number=f"engine_{Generator.uuid()}",
                           license_number=f"license-{Generator.uuid()}")

        user.vehicles.append(vehicle1)
        user.vehicles.append(vehicle2)
        user.vehicles.append(vehicle3)
        db.session.commit()

        find_user = User.query.get(user.uid)
        self.assertIsNotNone(find_user)

        self.assertTrue(find_user.vehicles != [])
        self.assertEqual(len(find_user.vehicles), 3)

        self.assertTrue(vehicle1.owner == vehicle2.owner == vehicle3.owner)

        vehicles = [vehicle1, vehicle2, vehicle3]
        for index, _ in enumerate(vehicles):
            self.assertEqual(find_user.vehicles[index].uid, vehicles[index].uid)
            self.assertEqual(find_user.vehicles[index].item_type, ItemTypeEnum.VEHICLE)
            self.assertEqual(find_user.vehicles[index].is_stolen, vehicles[index].is_stolen)
            self.assertEqual(find_user.vehicles[index].gd_copy_number, vehicles[index].gd_copy_number)
            self.assertEqual(find_user.vehicles[index].remarks, vehicles[index].remarks)
            self.assertEqual(find_user.vehicles[index].remarks, vehicles[index].remarks)
            self.assertEqual(find_user.vehicles[index].record_time, vehicles[index].record_time)
            self.assertEqual(find_user.vehicles[index].last_update, vehicles[index].last_update)

            self.assertEqual(find_user.vehicles[index].serial_number, vehicles[index].serial_number)
            self.assertEqual(find_user.vehicles[index].engine_number, vehicles[index].engine_number)
            self.assertEqual(find_user.vehicles[index].license_number, vehicles[index].license_number)

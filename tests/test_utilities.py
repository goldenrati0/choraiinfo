from unittest import TestCase

from src.utilities import Generator


class UtilityTest(TestCase):
    def test_uuid_generator(self):
        self.assertIsNotNone(Generator.uuid())

    def test_uuid_length(self):
        self.assertEqual(len(Generator.uuid()), 32)

    def test_uniqueness(self):
        uuid_list = list()
        length = 500
        for _ in range(length):
            uuid_list.append(Generator.uuid())
        self.assertEqual(len(set(uuid_list)), length)

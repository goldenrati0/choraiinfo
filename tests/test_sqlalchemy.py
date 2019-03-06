import unittest

from src.config import Database, SQLAlchemyConfig
from src.setup import app, db


class TestSQLAlchemy(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.db = db

    def test_db_driver(self):
        self.assertEqual(self.db.engine.driver, Database._db_driver)

    def test_db_engine(self):
        self.assertEqual(str(self.db.engine.url), SQLAlchemyConfig.database_uri)

    def test_db_connection(self):
        self.assertIsNotNone(self.db.engine.connect())

    def test_query_execution(self):
        query = "SELECT 1 AS num;"
        result = db.engine.execute(query)
        self.assertIsNotNone(result)
        for row in result:
            self.assertTrue("num" in row)
            self.assertEqual(row["num"], 1)

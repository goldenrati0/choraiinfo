from unittest import TestCase

from src.setup import app


class FlaskAppTest(TestCase):
    def setUp(self):
        self.app = app

    def test_app_config(self):
        self.assertIn(self.app.config.get("ENV"), ["DEV", "PRODUCTION", "STAGE"])
        self.assertTrue(self.app.config.get("DEBUG"), self.app.config.get("ENV") == "DEV")
        self.assertIsNotNone(self.app.config.get("SECRET_KEY"))

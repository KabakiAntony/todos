import unittest
from app import create_app
from app.api.model import db


class TodosBaseTest(unittest.TestCase):
    """create setUp and tearDown for todos"""
    def setUp(self):
        """set up tests all modules"""
        self.app = create_app()
        self.app.config.from_object('config.TestingConfig')
        self.client = self.app.test_client()
        db.create_all()

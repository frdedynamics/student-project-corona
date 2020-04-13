from unittest import TestCase
from src.resource.user import User


class TestUser(TestCase):

    def test_user(self):
        user = User(7, "TestUser7", "Test7")
        self.assertIsNotNone(user)
        self.assertEqual(user.password, "Test7")

import json
from .todosBaseTest import TodosBaseTest


class TestUsers(TodosBaseTest):
    """
    test various actions on the users resource
    """
    user = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "fireicewater"
    }
    user_two = {
        "email": "kabaki.antony@gmail.com",
        "password": "hollywoodemmysbafta"
    }
    empty_email_field = {
        "email": "",
        "password": "thisisapassword"
    }
    wrong_password = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "thisiswrong"
    }
    new_password = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "newpassword"
    }

    def create_new_user(self, data={}):
        if not data:
            data = self.user
        response = self.client.post(
            '/users/signup',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        return response

    def test_user_creation(self):
        """
        test creation of a user in the system
        """
        response = self.create_new_user()
        self.assertEqual(response.status_code, 201)

    def test_user_signin(self):
        """
        test user sign in with correct credentials
        """
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

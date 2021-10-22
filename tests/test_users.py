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
    empty_email_field = {
        "email": "",
        "password": "thisisapassword"
    }
    empty_password_field = {
        "email": "kabaki.kiarie@gmail.com",
        "password": ""
    }
    wrong_password = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "thisiswrong"
    }
    wrong_email = {
        "email": "kabaki4.kiarie@gmail.com",
        "password": "fireicewater"
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

    def test_user_creation_with_empty_email_field(self):
        """
        test user creation with an empty email field
        """
        response = self.client.post(
            '/users/signup',
            data=json.dumps(self.empty_email_field),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_user_creation_with_empty_password_field(self):
        """
        test user creation with an empty password field
        """
        response = self.client.post(
            '/users/signup',
            data=json.dumps(self.empty_password_field),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_user_signin(self):
        """
        test user sign in with correct credentials
        """
        self.create_new_user()
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_user_signin_with_wrong_password(self):
        """
        test user sign in with wrong password
        """
        self.create_new_user()
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.wrong_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_user_signin_non_existent_user(self):
        """
        test signing in a non existent user
        """
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.wrong_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_duplicate_user_creation(self):
        """
        test signing up a user twice
        """
        self.create_new_user()
        response = self.create_new_user()
        self.assertEqual(response.status_code, 409)

    def test_password_update(self):
        """
        test password update for a given user
        """
        self.create_new_user()
        resp = self.client.post(
            '/users/signin',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        auth_token = resp.json['data']['auth_token']
        response = self.client.put(
            '/users/update-password',
            data=json.dumps(self.new_password),
            headers={'auth_token': auth_token},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)

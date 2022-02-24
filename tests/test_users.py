import json
from app.api.models import db
from .todosBaseTest import TodosBaseTest


class TestUsers(TodosBaseTest):
    """
    test various actions on the users resource
    """
    user = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "fireicewater"
    }
    user_email = {
        "email": "kabaki.kiarie@gmail.com"
    }
    invalid_user_email = {
        "email": "kabaki.kiarie@gmail"
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
    unqualified_password = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "short"
    }
    invalid_token = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"""

    def create_new_user(self, data={}):
        if not data:
            data = self.user
        response = self.client.post(
            '/users/signup',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        return response

    def signin_user(self):
        """
        reusable user signin function
        """
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.user),
            content_type="application/json"
        )
        return response

    def test_a_user_creation(self):
        """
        test creation of a user in the system
        """
        response = self.create_new_user()
        self.assertEqual(response.status_code, 201)

    def test_b_user_creation_with_empty_email_field(self):
        """
        test user creation with an empty email field
        """
        response = self.client.post(
            '/users/signup',
            data=json.dumps(self.empty_email_field),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_c_user_creation_with_empty_password_field(self):
        """
        test user creation with an empty password field
        """
        response = self.client.post(
            '/users/signup',
            data=json.dumps(self.empty_password_field),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_d_user_signin(self):
        """
        test user sign in with correct credentials
        """
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_e_user_signin_with_wrong_password(self):
        """
        test user sign in with wrong password
        """
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.wrong_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_f_user_signin_non_existent_user(self):
        """
        test signing in a non existent user
        """
        response = self.client.post(
            '/users/signin',
            data=json.dumps(self.wrong_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_g_duplicate_user_creation(self):
        """
        test signing up a user twice
        """
        response = self.create_new_user()
        self.assertEqual(response.status_code, 409)

    def test_h_password_update(self):
        """
        test password update for a given user
        """
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
        self.assertEqual(response.status_code, 200)

    def test_i_password_update_with_an_unqualified_password(self):
        """
        test password update for a given user
        with a short password
        """
        resp = self.client.post(
            '/users/signin',
            data=json.dumps(self.new_password),
            content_type='application/json'
        )
        auth_token = resp.json['data']['auth_token']
        response = self.client.put(
            '/users/update-password',
            data=json.dumps(self.unqualified_password),
            headers={'auth_token': auth_token},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_j_forgot_password(self):
        """
        test for  forgot password.
        """
        response = self.client.post(
            '/users/forgot',
            data=json.dumps(self.user_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 202)

    def test_k_forgot_password_with_invalid_email(self):
        """
        test forgot email with an invalid email
        """
        response = self.client.post(
            '/users/forgot',
            data=json.dumps(self.invalid_user_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_l_password_update_with_invalid_token(self):
        """
        test password update for a given user
        with an invalid token
        """
        auth_token = self.invalid_token
        response = self.client.put(
            '/users/update-password',
            data=json.dumps(self.new_password),
            headers={'auth_token': auth_token},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_z_tearing_down(self):
        db.session.remove()
        db.drop_all()

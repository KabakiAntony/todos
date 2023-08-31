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

    def signup_and_verify_user(self):
        """
        signup and verification of a correct
        user account.
        """
        signup_response = self.client.post(
            '/users/signup',
            data=json.dumps(self.user),
            content_type="application/json"
        )

        auth_token = signup_response.json['data']['tkn']
        verification_response = self.client.post(
            '/users/verify',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )

        return signup_response, verification_response
    
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
    
    def test_user_creation_and_verification(self):
        """
        test creation of a user in the system
        """
        signup_response, verification_response = self.signup_and_verify_user()
        self.assertEqual(signup_response.status_code, 201)
        self.assertEqual(verification_response.status_code, 200)

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
        self.signup_and_verify_user()

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
        self.signup_and_verify_user()
        
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
        self.signup_and_verify_user()

        duplicate_response = self.client.post(
            '/users/signup',
            data=json.dumps(self.user),
            content_type="application/json"
        )
        self.assertEqual(duplicate_response.status_code, 409)

    def test_password_update(self):
        """
        test password update for a given user
        """
        self.signup_and_verify_user()
        
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

    def test_password_update_with_an_unqualified_password(self):
        """
        test password update for a given user
        with a short password
        """
        self.signup_and_verify_user()

        resp = self.signin_user()
        auth_token = resp.json['data']['auth_token']
        response = self.client.put(
            '/users/update-password',
            data=json.dumps(self.unqualified_password),
            headers={'auth_token': auth_token},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_forgot_password(self):
        """
        test for  forgot password.
        """
        self.signup_and_verify_user()

        response = self.client.post(
            '/users/forgot',
            data=json.dumps(self.user_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 202)

    def test_forgot_password_with_invalid_email(self):
        """
        test forgot email with an invalid email
        """
        self.signup_and_verify_user()

        response = self.client.post(
            '/users/forgot',
            data=json.dumps(self.invalid_user_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_password_update_with_invalid_token(self):
        """
        test password update for a given user
        with an invalid token
        """
        self.signup_and_verify_user()

        auth_token = self.invalid_token
        print(auth_token)

        response = self.client.put(
            '/users/update-password',
            data=json.dumps(self.unqualified_password),
            headers={'auth_token': auth_token},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)


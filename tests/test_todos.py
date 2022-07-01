import json
from app.api.models import db
from .todosBaseTest import TodosBaseTest


class TestTodos(TodosBaseTest):
    """
    Test vairous actions on the todos resource
    """
    user = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "fireicewater"
    }
    user_with_no_todos = {
        "email": "kabaki.antony@gmail.com",
        "password": "bluewhaleschool"
    }
    todo = {
        "text": "finish all projects in flask.",
    }
    updated_todo = {
        "text": " finished all projects in flask"
    }
    todo_with_empty_body = {
        "text": "",
    }

    def signup_and_verify_user(self):
        """
        reusable user signup function
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

    def test_creating_todo(self):
        """
        test creating a new todo
        """
        self.signup_and_verify_user()

        signin_response = self.signin_user()
        self.assertEqual(signin_response.status_code, 200)
        auth_token = signin_response.json['data']['auth_token']

        create_todo_response = self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(create_todo_response.status_code, 201)

    def test_getting_all_todos_for_a_user(self):
        """
        test getting all todos for a given user
        """
        self.signup_and_verify_user()
        signin_response = self.signin_user()
        self.assertEqual(signin_response.status_code, 200)
        auth_token = signin_response.json['data']['auth_token']

        self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )

        get_user_todos_response = self.client.get(
            '/todos',
            headers={'auth_token': auth_token}
        )
        self.assertEqual(get_user_todos_response.status_code, 200)

    def test_getting_non_existent_todos_for_a_user(self):
        """
        test getting todos for user that has no todos
        """
        user_with_no_todos_response = self.client.post(
            '/users/signup',
            data=json.dumps(self.user_with_no_todos),
            content_type="application/json"
        )

        auth_token = user_with_no_todos_response.json['data']['tkn']
        self.client.post(
            '/users/verify',
            headers={'auth_token': auth_token},
            content_type="application/json"
            )

        self.assertEqual(user_with_no_todos_response.status_code, 201)
        signin_user_response = self.client.post(
            '/users/signin',
            data=json.dumps(self.user_with_no_todos),
            content_type="application/json"
        )
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        get_user_todos_response = self.client.get(
            '/todos',
            headers={'auth_token': auth_token}
        )
        self.assertEqual(get_user_todos_response.status_code, 404)

    def test_creating_todo_with_no_todo_body(self):
        """
        test creating todo with no body
        """
        self.signup_and_verify_user()
        signin_response = self.signin_user()
        self.assertEqual(signin_response.status_code, 200)
        auth_token = signin_response.json['data']['auth_token']
        create_todo_response = self.client.post(
            '/todos',
            data=json.dumps(self.todo_with_empty_body),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(create_todo_response.status_code, 400)

    def test_updating_a_todo(self):
        """
        test updating a todo
        """
        self.signup_and_verify_user()
        signin_response = self.signin_user()
        self.assertEqual(signin_response.status_code, 200)
        auth_token = signin_response.json['data']['auth_token']

        self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )

        update_todo_response = self.client.put(
            f'/todos/{1}',
            data=json.dumps(self.updated_todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(update_todo_response.status_code, 200)

    def test_getting_a_specific_todo(self):
        """
        test getting a specific todo with the todo id
        """
        self.signup_and_verify_user()
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']

        self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        
        get_todo_response = self.client.get(
            f'/todos/{1}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(get_todo_response.status_code, 200)

    def test_getting_a_non_existent_todo(self):
        """
        test getting a specific todo with the todo id
        """
        self.signup_and_verify_user()
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        get_todo_response = self.client.get(
            f'/todos/{10}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(get_todo_response.status_code, 404)

    def test_creating_todo_with_token_missing(self):
        """
        test creating a new todo
        """
        create_todo_response = self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            content_type="application/json"
        )
        self.assertEqual(create_todo_response.status_code, 403)

    def test_deleting_a_todo(self):
        """
        test deleting a specific todo given an id
        """
        self.signup_and_verify_user()
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']

        self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )

        delete_todo_response = self.client.delete(
            f'/todos/{1}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(delete_todo_response.status_code, 200)

    def test_updating_a_non_existent_todo(self):
        """
        test updating a tod that does not exist
        """
        self.signup_and_verify_user()
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        update_todo_response = self.client.put(
            f'/todos/{10}',
            data=json.dumps(self.updated_todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(update_todo_response.status_code, 404)

    def test_deleting_a_non_existent_todo(self):
        """
        test deleting a todo that does not exist
        """
        self.signup_and_verify_user()
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        delete_todo_response = self.client.delete(
            f'/todos/{10}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(delete_todo_response.status_code, 404)

    def test_updating_a_todo_with_token_missing(self):
        """
        test updating a todo with token missing
        """
        self.signup_and_verify_user()
        update_todo_response = self.client.put(
            f'/todos/{1}',
            data=json.dumps(self.updated_todo),
            content_type="application/json"
        )
        self.assertEqual(update_todo_response.status_code, 403)

    def test_deleting_a_todo_with_token_missing(self):
        """
        test deleting a todo with token missing
        """
        delete_todo_response = self.client.delete(
            f'/todos/{1}',
            content_type="application/json"
        )
        self.assertEqual(delete_todo_response.status_code, 403)


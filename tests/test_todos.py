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
        "todo": "finish all projects in flask.",
    }
    updated_todo = {
        "todo": " finished all projects in flask"
    }
    todo_with_empty_body = {
        "todo": "",
    }

    def signup_user(self):
        """
        reusable user signup function
        """
        response = self.client.post(
            '/users/signup',
            data=json.dumps(self.user),
            content_type="application/json"
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

    def test_a_creating_todo(self):
        """
        test creating a new todo
        """
        create_user_response = self.signup_user()
        self.assertEqual(create_user_response.status_code, 201)
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        create_todo_response = self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(create_todo_response.status_code, 201)

    def test_b_getting_all_todos_for_a_user(self):
        """
        test getting all todos for a given user
        """
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        get_user_todos_response = self.client.get(
            '/todos',
            headers={'auth_token': auth_token}
        )
        self.assertEqual(get_user_todos_response.status_code, 200)

    def test_c_getting_non_existent_todos_for_a_user(self):
        """
        test getting todos for user that has no todos
        """
        user_with_no_todos_response = self.client.post(
            '/users/signup',
            data=json.dumps(self.user_with_no_todos),
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

    def test_d_creating_todo_with_no_todo_body(self):
        """
        test creating todo with no body
        """
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        create_todo_response = self.client.post(
            '/todos',
            data=json.dumps(self.todo_with_empty_body),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(create_todo_response.status_code, 400)

    def test_e_updating_a_todo(self):
        """
        test updating a todo
        """
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        update_todo_response = self.client.put(
            f'/todos/{1}',
            data=json.dumps(self.updated_todo),
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(update_todo_response.status_code, 200)

    def test_f_getting_a_specific_todo(self):
        """
        test getting a specific todo with the todo id
        """
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        get_todo_response = self.client.get(
            f'/todos/{1}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(get_todo_response.status_code, 200)

    def test_g_getting_a_non_existent_todo(self):
        """
        test getting a specific todo with the todo id
        """
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        get_todo_response = self.client.get(
            f'/todos/{10}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(get_todo_response.status_code, 404)

    def test_h_creating_todo_with_token_missing(self):
        """
        test creating a new todo
        """
        create_todo_response = self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            content_type="application/json"
        )
        self.assertEqual(create_todo_response.status_code, 403)

    def test_i_deleting_a_todo(self):
        """
        test deleting a specific todo given an id
        """
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        delete_todo_response = self.client.delete(
            f'/todos/{1}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(delete_todo_response.status_code, 200)

    def test_j_updating_a_non_existent_todo(self):
        """
        test updating a tod that does not exist
        """
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

    def test_k_deleting_a_non_existent_todo(self):
        """
        test deleting a todo that does not exist
        """
        signin_user_response = self.signin_user()
        self.assertEqual(signin_user_response.status_code, 200)
        auth_token = signin_user_response.json['data']['auth_token']
        delete_todo_response = self.client.delete(
            f'/todos/{10}',
            headers={'auth_token': auth_token},
            content_type="application/json"
        )
        self.assertEqual(delete_todo_response.status_code, 404)

    def test_l_updating_a_todo_with_token_missing(self):
        """
        test updating a todo with token missing
        """
        update_todo_response = self.client.put(
            f'/todos/{1}',
            data=json.dumps(self.updated_todo),
            content_type="application/json"
        )
        self.assertEqual(update_todo_response.status_code, 403)

    def test_m_updating_a_non_existent_todo(self):
        """
        test updating a  non existent todo
        """
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

    def test_n_deleting_a_todo_with_token_missing(self):
        """
        test deleting a todo with token missing
        """
        delete_todo_response = self.client.delete(
            f'/todos/{1}',
            content_type="application/json"
        )
        self.assertEqual(delete_todo_response.status_code, 403)

    def test_o_creating_todo_with_token_missing(self):
        """
        test creating a new todo with token missing
        """
        create_todo_response = self.client.post(
            '/todos',
            data=json.dumps(self.todo),
            content_type="application/json"
        )
        self.assertEqual(create_todo_response.status_code, 403)

    def test_z_tearing_down(self):
        """
        tear down  the database after running this
        module to clear the data set up by this module.
        """
        db.session.remove()
        db.drop_all()

import os
import datetime
from app.api import todos
from app.api.models import db
from flask import request, abort
from app.api.models.todos import Todos, todosSchema, todoSchema
from app.api.utils import (
    check_for_whitespace,
    custom_make_response,
    token_required
)

# get environment variables
KEY = os.getenv("SECRET_KEY")


@todos.route('/todos', methods=["POST"])
@token_required
def create_todo(user):
    """
    Create a new todo
    :param user: a user parameter will be passed so that we
    can get a unique user object and from that we will get a
    user id that will be used as a foreign key to tie a particular
    user to a given todo or todos.
    """
    try:
        todo_data = request.get_json()
        todo = todo_data['todo']
        # creation_date = todo_data['creation_date']
        date_created = datetime.datetime.utcnow()
        creation_date = date_created.strftime("%Y-%m-%d")

        check_for_whitespace(todo_data, ["todo"])

        user_id = user['id']

        new_todo = Todos(
            user_id=user_id, creation_date=creation_date, todo=todo)
        db.session.add(new_todo)
        db.session.commit()

        return custom_make_response(
            "data",
            "New todo created successfully.",
            201
        )
    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)


@todos.route('/todos', methods=['GET'])
@token_required
def get_user_todos(user):
    """
    Get todos for a given user
    :param user:given a user object get a unique user id
    and return their todos
    """
    try:
        user_id = user['id']

        todos = Todos.query.filter_by(user_id=user_id).all()
        _todos = todosSchema.dump(todos)

        if not todos:
            abort(
                404,
                'You do not have any todos, please create some and try again.')

        return custom_make_response("data", _todos, 200)

    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)


@todos.route('/todos/<id>', methods=['PUT'])
@token_required
def edit_todo(user, id):
    """
    Edit the todo information
    :param user: a user object is passed to the function
    so that we can be able to get the user id and
    associate it with the given todo we are updating
    :param id: we have to have the unique for the given
    todo so that we can update it.
    """
    try:
        todo_data = request.get_json()
        todo_update = todo_data['todo']
        user_id = user['id']
        todo_id = id

        Todos.query.filter_by(id=todo_id).filter_by(user_id=user_id).update(
            dict(todo=f"{todo_update}")
        )
        db.session.commit()

        return custom_make_response(
            "data",
            "Todo updated successfully.",
            200
        )
    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)


@todos.route('/todos/<id>', methods=['GET'])
@token_required
def get_specific_user_todos(user, id):
    """
    Get todos for a given user
    :param user:given a user object get a unique user id
    and return their todos
    """
    try:
        user_id = user['id']

        todo = Todos.query.filter_by(user_id=user_id).filter_by(id=id).first()
        _todo = todoSchema.dump(todo)

        if not todo:
            abort(
                404,
                'The todo has not been found, please create and try again.')

        return custom_make_response("data", _todo, 200)

    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)


@todos.route('/todos/<id>', methods=['DELETE'])
@token_required
def delete_specific_user_todos(user, id):
    """
    Delete a given todo for a given user
    :param user:given a user object get a unique user id
    and return their todos
    """
    try:
        user_id = user['id']

        Todos.query.filter_by(user_id=user_id).filter_by(id=id).delete()
        db.session.commit()
        return custom_make_response("data", "Todo deleted successfully.", 200)

    except Exception as e:
        return custom_make_response("error", f"{str(e)}", e.code)

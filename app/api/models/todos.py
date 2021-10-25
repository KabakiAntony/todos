from app.api.models import db, ma
from datetime import datetime


class Todos(db.Model):
    """
    creating the todos model
    """
    __tablename__ = "Todos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey("Users.id"))
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    todo = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, creation_date, todo):
        self.user_id = user_id
        self.creation_date = creation_date
        self.todo = todo


class TodosSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "creation_date", "todo")


todoSchema = TodosSchema()
todosSchema = TodosSchema(many=True)

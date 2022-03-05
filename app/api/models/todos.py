from app.api.models import db, ma


class Todos(db.Model):
    """
    creating the todos model
    """
    __tablename__ = "Todos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey("Users.id"))
    text = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text


class TodosSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "text", "completed")


todoSchema = TodosSchema()
todosSchema = TodosSchema(many=True)

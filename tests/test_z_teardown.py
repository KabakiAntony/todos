from .todosBaseTest import TodosBaseTest
from app.api.models import db


class TestTearDown(TodosBaseTest):

    def test_tearing_down(self):
        print("tearing down the database")
        db.session.remove()
        db.drop_all()

from app.api.models import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    """
    creating users model
    """
    __tablename__ = "Users"
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.String(25), default="False", nullable=True)

    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = self.hash_password(password)

    def hash_password(self, password):
        """
        given a password string of any form or size
        hash it in preparation for storage
        """
        password_hash = generate_password_hash(str(password))
        return password_hash

    def compare_password(hashed_password, password):
        """
        given a plain string password generate a hash
        that will be used to compare with the stored
        password in the database
        """
        return check_password_hash(hashed_password, str(password))


class UsersSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "verified")


user_schema = UsersSchema()

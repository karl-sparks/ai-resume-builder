from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """
    A class representing a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, email, username):
        self.email = email
        self.username = username

    def __repr__(self):
        return f"<User : {self.id} : {self.username} : {self.email}>"

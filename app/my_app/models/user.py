from flask import request
from my_app import db

class UserModel(db.Model):
    """
    User Model Class

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password (str): The hashed password of the user.
        email (str): The email address of the user.
        activated (bool): A boolean indicating whether the user is activated.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        """
        Find a user by their username.

        Args:
            username (str): The username to search for.

        Returns:
            UserModel: The user with the given username, or None if not found.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        """
        Find a user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            UserModel: The user with the given email address, or None if not found.
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        """
        Find a user by their unique ID.

        Args:
            _id (int): The unique ID of the user to search for.

        Returns:
            UserModel: The user with the given ID, or None if not found.
        """
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        """
        Save the user object to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        Delete the user object from the database.
        """
        db.session.delete(self)
        db.session.commit()


class RevokeAccessToken(db.Model):
    """
    Model class for revoking access tokens.
    
    Attributes:
        id (int): The primary key column.
        jti (str): The JWT ID column, which is a unique identifier for each token.
    """
    
    # Specify the table name for the model
    __tablename__ = "revoked_access_tokens"

    # Define the columns for the model
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)

    def __init__(self, jti):
        """
        Initialize a new instance of the RevokeAccessToken model.
        
        Args:
            jti (str): The JWT ID to be associated with the token being revoked.
        """
        self.jti = jti

    def save_to_db(self):
        """
        Save the model instance to the database.
        
        This method adds the current instance to the database session and commits the changes.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """
        Check if a JWT ID is blacklisted.

        Args:
            jti (str): The JWT ID to check.

        Returns:
            bool: True if the JWT ID is blacklisted, False otherwise.
        """
        return cls.query.filter_by(jti=jti).first() is not None


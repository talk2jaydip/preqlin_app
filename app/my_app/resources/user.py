import traceback, requests
from flask_restful import Resource
from flask import request, render_template, make_response

from werkzeug.security import generate_password_hash, check_password_hash
from my_app import db
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
)
from my_app.models.user import UserModel
from my_app.schemas.user import UserSchema
from blacklist import BLACKLIST

USER_ALREADY_EXISTS = "A user with that username already exists."
EMAIL_ALREADY_EXISTS = "A user with that email already exists."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."
NOT_CONFIRMED_ERROR = (
    "You have not confirmed registration, please check your email <{}>."
)
FAILED_TO_CREATE = "Internal server error. Failed to create user."
SUCCESS_REGISTER_MESSAGE = "Account created successfully, an email with an activation link has been sent to your email address, please check."

user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    def post(cls):
        """
        Register a new user.

        Returns:
            dict: A message indicating the result of the registration.
        """
        user_json = request.get_json()
        user = user_schema.load(user_json, session=db.session)

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(user.email):
            return {"message": EMAIL_ALREADY_EXISTS}, 400

        try:
            user.password = generate_password_hash(user.password)
            user.save_to_db()
            return {"message": SUCCESS_REGISTER_MESSAGE}, 201
        except Exception:
            traceback.print_exc()
            return {"message": FAILED_TO_CREATE}, 500

class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        """
        Get user details by user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: The user details.
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        """
        Delete a user by user ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            dict: A message indicating the result of the deletion.
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.delete_from_db()
        return {"message": USER_DELETED}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        """
        Log in a user.

        Returns:
            dict: Access and refresh tokens.
        """
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",), session=db.session)

        user = UserModel.find_by_username(user_data.username)

        if user and check_password_hash(user.password, user_data.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return (
                    {"access_token": access_token, "refresh_token": refresh_token},
                    200,
                )
            return {"message": NOT_CONFIRMED_ERROR.format(user.email)}, 400

        return {"message": INVALID_CREDENTIALS}, 401

class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """
        Log out a user.

        Returns:
            dict: A message indicating the user has been logged out.
        """
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id=user_id)}, 200

class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        """
        Refresh the user's access token.

        Returns:
            dict: A new access token.
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        """
        Confirm a user's registration.

        Args:
            user_id (int): The ID of the user to confirm.

        Returns:
            dict: A message indicating the confirmation is complete.
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.activated = True
        user.save_to_db()
        

        return {"message": "Verification completed"}, 200

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from my_app.models.user import UserModel, RevokeAccessToken



# Define a schema class for User model
class UserSchema(SQLAlchemyAutoSchema):
    """
        A schema for serializing and deserializing User model.
    """
    # Specify the meta attributes for the schema
    class Meta:
        # Set the model class
        model = UserModel
        # Load the data into a model instance
        load_instance = True
        # Exclude the password field from loading
        load_only = ("password",)
        # Exclude the id and activated fields from dumping
        dump_only = ("id", "activated")

    


# Define a schema class for RevokeAccessToken model
class RevokeAccessTokenSchema(SQLAlchemyAutoSchema):
    """
        A schema for revoking access tokens using OAuth 2.0 token revocation endpoint
    """
    # Specify the meta attributes for the schema
    class Meta:
        # Set the model class
        model = RevokeAccessToken

    # Add a docstring for the schema class
    

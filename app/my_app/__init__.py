# Import Flask and other modules
import os, logging
from flask import Flask, render_template, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_marshmallow import Marshmallow

# Configure logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

# Initialize database and marshmallow
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

# Define error handler for 404 page not found
def page_not_found(error):
    return render_template('404.html'), 404

# Define application factory function
def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    # Import resources from my_app package
    from my_app.resources.user import (
        UserRegister,
        UserLogin,
        User,
        UserLogout,
        UserConfirm,
        TokenRefresh
    )
    from my_app.resources.random_array import RandomArray

    # Create Flask app object with config object
    flask_app = Flask(__name__)
    flask_app.config.from_object(object_name)

    # Use environment variable or random string for secret key
    flask_app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(16)

    # Create API object and add resources
    api = Api(flask_app)
    
    api.add_resource(UserRegister, "/register")
    api.add_resource(User, "/user/<int:user_id>")
    api.add_resource(UserLogin, "/login")
    api.add_resource(TokenRefresh, "/refresh")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")
    api.add_resource(RandomArray, '/generate_random_array')


    # Register error handler for 404 page not found
    flask_app.register_error_handler(404, page_not_found)

    # Return Flask app object
    return flask_app

# Get environment variable for Flask environment or use default value
env = os.environ.get('FLASK_ENV', 'test')

# Create app using application factory function with config object
app = create_app('config.%sConfig' % env.capitalize())

# Initialize database, marshmallow and migrate with app
db.init_app(app)
ma.init_app(app)

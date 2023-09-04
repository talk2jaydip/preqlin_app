# from my_app import app
# app.run(debug=True)
import os
from marshmallow import ValidationError
from flask import  jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from my_app import app, db, ma
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from blacklist import BLACKLIST

jwt = JWTManager(app)

with app.app_context():
    print("BUMP")
    db.create_all()

# def authorize():
#     try:
#         verify_jwt_in_request()
#         current_user = get_jwt_identity()
#         # You can perform additional authorization checks here if needed
#     except Exception as e:
#         return jsonify({'message': 'Unauthorized'}), 401
    
# # Register middleware for authorization
# @app.before_request
# def before_request():
#     authorize()

# Define a custom response for endpoint not available
@app.errorhandler(404)
def custom_not_found_response(error):
    return jsonify({'status': 'error', 'message': 'The requested resource or endpoint is not available'}), 404

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

# Add error handling for JWT authentication errors
@jwt.invalid_token_loader
@jwt.unauthorized_loader
def handle_invalid_token(error):
    return {"error": "Invalid or missing access token"}, 401

# Define a custom callback function that checks the blacklist before verifying the token expiration
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"] # Get the JWT ID from the payload
    return jti in BLACKLIST # Return True if the JWT ID is in the blacklist, False otherwise



# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Obtain a database connection from the engine
        conn = db.engine.raw_connection()
        
        # Check the database connection by executing a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        
        # Close the cursor and the connection
        cursor.close()
        conn.close()
        
        return jsonify({'status': 'ok', 'message': 'Database connection is healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'{e} Database connection error'}), 500


# API Status Check Endpoint
@app.route('/status', methods=['GET'])
def api_status():
    return jsonify({'message': 'API is up and running'}), 200



if __name__ == '__main__':
    app.run(port=5000, debug=True)

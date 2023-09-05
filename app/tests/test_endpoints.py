import unittest
from my_app import create_app,db,ma  # Import your Flask app
import json
from flask_jwt_extended import JWTManager
import unittest
import tempfile, os
import coverage

cov = coverage.coverage(
    omit = [
        
    ]
)
cov.start()

env ='test'
app = create_app('config.%sConfig' % env.capitalize())
db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        test_config = {}
        self.test_db_file = tempfile.mkstemp()[1]

        test_config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        test_config['TESTING'] = True

        with app.app_context():
            db.create_all()
        self.app = app.test_client()
    def tearDown(self):
        pass#os.remove(self.test_db_file)

    
    def get_access_token(self):
        # Simulate a login request and get an access token
        data = {"username": "testuser", "password": "testpassword"}
        response = self.app.post('/login', data=json.dumps(data), content_type='application/json')
        access_token = json.loads(response.data)['access_token']
        return access_token

    def test_user_existing_not_confirmed(self):
        data = {"username": "testuser", "password": "testpassword", "email": "test@example.com"}
        response = self.app.post('/register', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.data)
        expected_data = {'message': 'Account created successfully, an email with an activation link has been sent to your email address, please check.'}
        assert response_data == expected_data

    def test_user_register_existing(self):
        # Test the /register endpoint without authentication
        data = {"username": "testuser", "password": "testpassword", "email": "test@example.com"}
        response = self.app.post('/register', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.data)
        expected_data = {"message": "A user with that username already exists."}
        assert response_data == expected_data 
    def test_user_get(self):
        # Test the /user/<int:user_id> endpoint with authentication
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get('/user/4', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        # Test the /login endpoint without authentication
        data = {"username": "testuser", "password": "testpassword"}
        response = self.app.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_token_refresh(self):
        # Test the /refresh endpoint with authentication
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.post('/refresh', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        # Test the /logout endpoint with authentication
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.post('/logout', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_user_confirm(self):
        # Test the /user_confirm/<int:user_id> endpoint without authentication
        response = self.app.get('/user_confirm/4')
        self.assertEqual(response.status_code, 200)

    def test_generate_random_array(self):
        # Test the /generate_random_array endpoint with authentication
        access_token = self.get_access_token()
        data = {"sentence": "Hello Test!"}
        headers = {'Authorization': f'Bearer {access_token}','Content-Type':'application/json'}
        response = self.app.post('/generate_random_array',data=json.dumps(data), headers=headers, )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        cov.stop()
        cov.save()
        cov.report()
        cov.html_report(directory = './coverage')
        cov.erase()

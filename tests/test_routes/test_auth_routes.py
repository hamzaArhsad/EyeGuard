from tests.test_routes.base_test import RouteBaseTest
import json
import os

class TestAuthRoutes(RouteBaseTest):
    def setUp(self):
        super().setUp()
        # Create a test user first with debug prints
        print("\nCreating test user...")
        response = self.client.post('/api/users/create',
            json={
                'username': 'testuser',
                'password': 'testpass',
                'role': 'operator'
            }
        )
        print(f"User creation response: {response.status_code}")
        print(f"User creation data: {response.data}")
        self.assertEqual(response.status_code, 201, "User creation failed")

    def test_login_success(self):
        print("\nTesting login...")
        response = self.client.post('/api/auth/login',
            json={
                'username': 'testuser',
                'password': 'testpass'
            }
        )
        print(f"Login response status: {response.status_code}")
        print(f"Login response data: {response.data}")
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)

    def test_login_failure(self):
        response = self.client.post('/api/auth/login',
            json={
                'username': 'testuser',
                'password': 'wrongpass'
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        # Login first with debug prints
        print("\nLogging in for logout test...")
        login_response = self.client.post('/api/auth/login',
            json={
                'username': 'testuser',
                'password': 'testpass'
            }
        )
        print(f"Login response for logout test: {login_response.status_code}, {login_response.data}")
        self.assertEqual(login_response.status_code, 200)
        data = json.loads(login_response.data)
        token = data['token']

        # Test logout
        response = self.client.post('/api/auth/logout',
            headers={'Authorization': token}
        )
        self.assertEqual(response.status_code, 204)

    def test_validate_token(self):
        # Login first with debug prints
        print("\nLogging in for token validation test...")
        login_response = self.client.post('/api/auth/login',
            json={
                'username': 'testuser',
                'password': 'testpass'
            }
        )
        print(f"Login response for validation test: {login_response.status_code}, {login_response.data}")
        self.assertEqual(login_response.status_code, 200)
        data = json.loads(login_response.data)
        token = data['token']

        # Test token validation
        response = self.client.get('/api/auth/validate',
            headers={'Authorization': token}
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        if os.path.exists('local_token.txt'):
            os.remove('local_token.txt')
        super().tearDown() 
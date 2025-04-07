from tests.test_routes.base_test import RouteBaseTest
import json
class TestUserRoutes(RouteBaseTest):
    def test_create_user(self):
        response = self.client.post('/api/users',
            json={
                'username': 'testuser',
                'password': 'testpass',
                'role': 'operator'
            }
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['role'], 'operator')
        self.assertIn('id', data)

    def test_get_all_users(self):
        # Create a test user first
        self.client.post('/api/users',
            json={
                'username': 'testuser',
                'password': 'testpass',
                'role': 'operator'
            }
        )

        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['username'], 'testuser')

    def test_get_user_by_id(self):
        # Create a test user
        create_response = self.client.post('/api/users',
            json={
                'username': 'testuser',
                'password': 'testpass',
                'role': 'operator'
            }
        )
        user_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/api/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['id'], user_id)

    def test_update_user(self):
        # Create a test user
        create_response = self.client.post('/api/users',
            json={
                'username': 'testuser',
                'password': 'testpass',
                'role': 'operator'
            }
        )
        user_id = json.loads(create_response.data)['id']

        # Update the user
        response = self.client.put(f'/api/users/{user_id}',
            json={
                'username': 'updateduser',
                'role': 'admin'
            }
        )
        self.assertEqual(response.status_code, 204)

        # Verify the update
        get_response = self.client.get(f'/api/users/{user_id}')
        data = json.loads(get_response.data)
        self.assertEqual(data['username'], 'updateduser')
        self.assertEqual(data['role'], 'admin')

    def test_delete_user(self):
        # Create a test user
        create_response = self.client.post('/api/users',
            json={
                'username': 'testuser',
                'password': 'testpass',
                'role': 'operator'
            }
        )
        user_id = json.loads(create_response.data)['id']

        # Delete the user
        response = self.client.delete(f'/api/users/{user_id}')
        self.assertEqual(response.status_code, 204)

        # Verify the deletion
        get_response = self.client.get(f'/api/users/{user_id}')
        self.assertEqual(get_response.status_code, 404) 
from tests.test_routes.base_test import RouteBaseTest
import json

class TestCameraRoutes(RouteBaseTest):
    def test_create_camera(self):
        response = self.client.post('/api/cameras/create',
            json={
                'id': 'camera-001',
                'location': 'Test Location',
                'rtsp_url': 'rtsp://test.com/stream'
            }
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 'camera-001')
        self.assertEqual(data['location'], 'Test Location')
        self.assertEqual(data['status'], 'deactive')

    def test_get_all_cameras(self):
        # Create a test camera first
        self.client.post('/api/cameras/create',
            json={
                'id': 'camera-001',
                'location': 'Test Location',
                'rtsp_url': 'rtsp://test.com/stream'
            }
        )

        response = self.client.get('/api/cameras/get-all')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['id'], 'camera-001')

    def test_get_camera_by_id(self):
        # Create a test camera
        self.client.post('/api/cameras/create',
            json={
                'id': 'camera-001',
                'location': 'Test Location',
                'rtsp_url': 'rtsp://test.com/stream'
            }
        )

        response = self.client.get('/api/cameras/get-by-id/camera-001')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['location'], 'Test Location')
        self.assertEqual(data['id'], 'camera-001')

    def test_delete_camera(self):
        # Create a test camera
        self.client.post('/api/cameras/create',
            json={
                'id': 'camera-001',
                'location': 'Test Location',
                'rtsp_url': 'rtsp://test.com/stream'
            }
        )

        response = self.client.delete('/api/cameras/delete-by-id/camera-001')
        self.assertEqual(response.status_code, 204)

        # Verify deletion
        get_response = self.client.get('/api/cameras/camera-001')
        self.assertEqual(get_response.status_code, 404)

    def test_activate_camera(self):
        # Create a test camera
        self.client.post('/api/cameras/create',
            json={
                'id': 'camera-001',
                'location': 'Test Location',
                'rtsp_url': 'rtsp://test.com/stream'
            }
        )

        response = self.client.post('/api/cameras/activate-by-id/camera-001')
        self.assertEqual(response.status_code, 204)

        # Verify activation
        get_response = self.client.get('/api/cameras/get-by-id/camera-001')
        data = json.loads(get_response.data)
        self.assertEqual(data['status'], 'active')

    def test_deactivate_camera(self):
        # Create and activate a test camera
        self.client.post('/api/cameras/create',
            json={
                'id': 'camera-001',
                'location': 'Test Location',
                'rtsp_url': 'rtsp://test.com/stream'
            }
        )
        self.client.post('/api/cameras/activate-by-id/camera-001')

        # Test deactivation
        response = self.client.post('/api/cameras/deactivate-by-id/camera-001')
        self.assertEqual(response.status_code, 204)

        # Verify deactivation
        get_response = self.client.get('/api/cameras/get-by-id/camera-001')
        data = json.loads(get_response.data)
        self.assertEqual(data['status'], 'deactive') 
from rest_framework.test import APITestCase
from rest_framework import status

class EndpointVersionTestsGet(APITestCase):
    def test_get_version(self):
        response = self.client.get('/api/version')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data, {"version": "1.0.0"})


from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class EndpointTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username="superuser", 
            password="superpassword")
        cls.standard_user = User.objects.create_user(
            username="standard_user", 
            password="userpassword")

    def setUp(self):
        self.client.logout()
    
    def test_get_users_as_logged_out_user(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_users_as_standard_user(self):
        # Create low level user
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_users_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_user_as_standard_user(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_user_logged_out(self):
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_user_good_request(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_user_empty_password(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_user_empty_username(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.post(path='/api/users/', data={
            "username": "",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_standard_user(self):
        self.client.login(username="superuser", password="superpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.delete(f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        second_user = User.objects.create_superuser(username='testuser2', password='testpassword')
        response = self.client.delete(f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_self(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.delete(f'/api/users/{self.standard_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)        
        
    def test_put_user_logged_out(self):
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test2",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_put_user_as_standard_user(self):
        self.client.login(username="standard_user", password="userpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test2",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_put_user_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test2",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_put_user_good_request(self):
        self.client.login(username="superuser", password="superpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test",
            "password": "",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_put_user_empty_password(self):
        self.client.login(username="superuser", password="superpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test",
            "password": "",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_put_user_empty_username(self):
        self.client.login(username="superuser", password="superpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_user_by_id_logged_out(self):
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.get(path=f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_user_by_id_as_standard_user(self):
        self.client.login(username="standard_user", password="userpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.get(path=f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_user_by_id_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.get(path=f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
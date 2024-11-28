from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class SetUp():
    def create_and_login_as_superuser(self):
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    def create_and_login_as_standard_user(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

class EndpointAuthTestGetAll(APITestCase):  
    def test_get_users_logged_out(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_users_invalid_privilege(self):
        # Create low level user
        SetUp.create_and_login_as_standard_user(self)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_users_valid_privilege(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EndpointAuthTestCreate(APITestCase):        
    def test_create_user_max_privilege(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    # FAILING
    def test_create_user_as_standard_user(self):
        SetUp.create_and_login_as_standard_user(self)
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    # FAILING
    def test_create_user_logged_out(self):
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class EndpointBadRequestTestCreate(APITestCase):
    def test_create_user_good_request(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    # FAILING
    def test_create_user_empty_password(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # FAILING
    def test_create_user_empty_username(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.post(path='/api/users/', data={
            "username": "",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class EndpointAuthTestDelete(APITestCase):
    def test_delete_low_level_user(self):
        # Create low level user
        SetUp.create_and_login_as_superuser(self)
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.delete(f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    # FAILING
    def test_delete_superuser(self):
        SetUp.create_and_login_as_superuser(self)
        second_user = User.objects.create_superuser(username='testuser2', password='testpassword')
        response = self.client.delete(f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # FAILING
    def test_delete_self(self):
        # Create low level user
        SetUp.create_and_login_as_standard_user(self)
        response = self.client.delete(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)        
        
class EndpointAuthTestUpdate(APITestCase):
    def test_update_user_logged_out(self):
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test2",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_user_invalid_privilege(self):
        SetUp.create_and_login_as_standard_user(self)
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test2",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_user_valid_privilege(self):
        SetUp.create_and_login_as_superuser(self)
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.put(path=f'/api/users/{second_user.id}/', data={
            "username": "test2",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class EndpointBadRequestTestUpdate(APITestCase):
    def test_update_user_good_request(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_user_empty_password(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.post(path='/api/users/', data={
            "username": "test",
            "password": "",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_user_empty_username(self):
        SetUp.create_and_login_as_superuser(self)
        response = self.client.post(path='/api/users/', data={
            "username": "",
            "password": "9EMxLB]632p",
            "is_staff": False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class EndpointAuthTestGetById(APITestCase):
    def test_get_user_by_id_logged_out(self):
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.get(path=f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_user_by_id_invalid_privilege(self):
        SetUp.create_and_login_as_standard_user(self)
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.get(path=f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_user_by_id_valid_privilege(self):
        SetUp.create_and_login_as_superuser(self)
        second_user = User.objects.create_user(username='testuser2', password='testpassword')
        response = self.client.get(path=f'/api/users/{second_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
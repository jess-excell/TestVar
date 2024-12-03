from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from flashcard.models import FlashcardSet, FlashcardCollection, FlashCard

class EndpointTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Users
        cls.superuser = User.objects.create_superuser(
            username="super_user", 
            password="super_password")
        cls.collection_owner = User.objects.create_user(
            username="owner", 
            password="owner_password")
        cls.standard_user = User.objects.create_user(
            username="standard_user",
            password="standard_password"
        )
        
        # Public flashcard setup
        cls.flashcard_collection_public = FlashcardCollection.objects.create(
            title="Public Collection", 
            user=cls.collection_owner, 
            public=True)
        
        # Private flashcard setup
        cls.flashcard_collection_private = FlashcardCollection.objects.create(
            title="Private Collection", 
            user=cls.collection_owner, 
            public=False)
        
    def setUp(self):
        self.client.logout()

    # region Get
    # region Get all collections
    def test_get_collections_as_logged_out_user(self):
        response = self.client.get('/api/collections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_collection_public)
        self.assertNotContains(response, self.flashcard_collection_private)
    
    def test_get_collections_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.get('/api/collections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_collection_public)
        self.assertNotContains(response, self.flashcard_collection_private)
    
    def test_get_collections_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get('/api/collections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_collection_public)
        self.assertContains(response, self.flashcard_collection_private)
    
    def test_get_collections_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get('/api/collections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_collection_public)
        self.assertContains(response, self.flashcard_collection_private)
    # endregion
    # region Get public collection by ID
    def test_get_public_collection_by_id_as_logged_out_user(self):
        response = self.client.get(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_public_collection_by_id_as_standard_user(self):
        self.client.login(username="collections", password="standard_password")
        response = self.client.get(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_public_collection_by_id_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_public_collection_by_id_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # endregion    
    # region Get private collection by ID
    def test_get_private_collection_by_id_as_logged_out_user(self):
        response = self.client.get(f'/api/collections/{self.flashcard_collection_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_private_collection_by_id_as_standard_user(self):
        self.client.login(username="collections", password="standard_password")
        response = self.client.get(f'/api/collections/{self.flashcard_collection_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_private_collection_by_id_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get(f'/api/collections/{self.flashcard_collection_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_private_collection_by_id_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get(f'/api/collections/{self.flashcard_collection_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # endregion
    # endregion
    # region Post
    def test_create_collection_as_logged_out_user(self):
        response = self.client.post('/api/collections/', data={
            "title": "test",
            "description": "test description"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_collection_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.post('/api/collections/', data={
            "title": "test",
            "description": "test description"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_collection_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.post('/api/collections/', data={
            "title": "test",
            "description": "test description"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    # endregion
    # region Put
    def test_put_collection_as_logged_out_user(self):
        response = self.client.put(f'/api/collections/{self.flashcard_collection_public.id}/', data={
            "title": "Updated title",
            "description": "Updated description",
            "public": True
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_collection_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.put(f'/api/collections/{self.flashcard_collection_public.id}/', data={
            "title": "Updated title",
            "description": "Updated description",
            "public": True
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_collection_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.put(f'/api/collections/{self.flashcard_collection_public.id}/', data={
            "title": "Updated title",
            "description": "Updated description",
            "public": True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_put_collection_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.put(f'/api/collections/{self.flashcard_collection_public.id}/', data={
            "title": "Updated title",
            "description": "Updated description",
            "public": True
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    # endregion
    # region Delete
    def test_delete_collection_as_logged_out_user(self):
        response = self.client.delete(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_collection_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.delete(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_collection_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.delete(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_collection_as_super_user(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.delete(f'/api/collections/{self.flashcard_collection_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    # endregion
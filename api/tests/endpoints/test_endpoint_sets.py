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
        cls.set_owner = User.objects.create_user(
            username="owner", 
            password="owner_password")
        cls.standard_user = User.objects.create_user(
            username="standard_user",
            password="standard_password"
        )
        
        # Public setup
        cls.flashcard_collection_public = FlashcardCollection.objects.create(
            title="Public Collection", 
            user=cls.set_owner, 
            public=True)
        cls.flashcard_set_public = FlashcardSet.objects.create(
            title="Public Set",
            flashcard_collection=cls.flashcard_collection_public,
            description="Description for public set")
        
        # Private setup
        cls.flashcard_collection_private = FlashcardCollection.objects.create(
            title="Private Collection", 
            user=cls.set_owner, 
            public=False)
        cls.flashcard_set_private = FlashcardSet.objects.create(
            title="Private Set",
            flashcard_collection=cls.flashcard_collection_private,
            description="Description for private set")
        
    #region Get
    #region Get all sets
    def setUp(self):
        self.client.logout()
    
    def test_get_sets_as_logged_out_user(self):
        response = self.client.get('/api/sets/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_sets_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.get('/api/sets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_public)
        self.assertNotContains(response, self.flashcard_set_private)
        
    def test_get_sets_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get('/api/sets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_public)
        self.assertContains(response, self.flashcard_set_private)
    
    def test_get_sets_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get('/api/sets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_public)
        self.assertContains(response, self.flashcard_set_private)
    # endregion
    # region Get public flashcard by ID
    def test_get_public_set_by_id_as_logged_out_user(self):
        response = self.client.get(f'/api/sets/{self.flashcard_set_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_public_flashcard_set_by_id_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.get(f'/api/sets/{self.flashcard_set_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_public)
    
    def test_get_public_flashcard_set_by_id_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get(f'/api/sets/{self.flashcard_set_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_public)
        
    def test_get_public_flashcard_set_by_id_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get(f'/api/sets/{self.flashcard_set_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_public)
    # endregion
    # region Get private flashcards by ID
    def test_get_private_flashcard_set_by_id_as_logged_out_user(self):
        response = self.client.get(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Should be 404 not 403
    
    def test_get_private_flashcard_set_by_id_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.get(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_private_flashcard_set_by_id_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_private)
        
    def test_get_private_flashcard_set_by_id_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_set_private)
    # endregion
    # endregion
    # region Post
    def test_create_set_as_logged_out_user(self):
        response = self.client.post('/api/sets/', data={
            "title": "New test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_set_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.post('/api/sets/', data={
            "title": "New test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_set_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.post('/api/sets/', data={
            "title": "New test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_set_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.post('/api/sets/', data={
            "title": "New test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    # endregion
    
    # region Put
    def test_put_set_as_logged_out_user(self):
        response = self.client.put(f'/api/sets/{self.flashcard_set_public.id}/', data={
            "title": "Updated test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_set_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.put(f'/api/sets/{self.flashcard_set_public.id}/', data={
            "title": "Updated test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_set_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.put(f'/api/sets/{self.flashcard_set_public.id}/', data={
            "title": "Updated test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Depending on layout of JSON will need a whole load of FK validation to make sure 
        # user can't move comment between sets etc.
        # easiest to just make the field readonly
    
    def test_put_set_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.put(f'/api/sets/{self.flashcard_set_public.id}/', data={
            "title": "Updated test set",
            "description": "test",
            "flashcard_collection": 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    # endregion
    # region Delete
    def test_delete_as_logged_out_user(self):
        response = self.client.delete(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response =self.client.delete(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Actually returning 403 which isn't the end of the world
    
    def test_delete_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response =self.client.delete(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response =self.client.delete(f'/api/sets/{self.flashcard_set_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #endregion
    
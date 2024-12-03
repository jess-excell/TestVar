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
        
        # Public flashcard setup
        cls.flashcard_collection_public = FlashcardCollection.objects.create(
            title="Public Collection", 
            user=cls.set_owner, 
            public=True)
        cls.flashcard_set_public = FlashcardSet.objects.create(
            title="Public Set",
            flashcard_collection=cls.flashcard_collection_public,
            description="Description for public set")
        cls.flashcard_public = FlashCard.objects.create(
            question="Public question",
            answer="answer",
            difficulty="easy",
            flashcard_set=cls.flashcard_set_public)
        
        # Private flashcard setup
        cls.flashcard_collection_private = FlashcardCollection.objects.create(
            title="Private Collection", 
            user=cls.set_owner, 
            public=False)
        cls.flashcard_set_private = FlashcardSet.objects.create(
            title="Private Set",
            flashcard_collection=cls.flashcard_collection_private,
            description="Description for private set")
        cls.flashcard_private = FlashCard.objects.create(
            question="Private question",
            answer="answer",
            difficulty="easy",
            flashcard_set=cls.flashcard_set_private)
        
    def setUp(self):
        self.client.logout()
    
    # region Get
    # region Get all flashcards
    def test_get_flashcards_as_logged_out_user(self):
        response = self.client.get('/api/flashcards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_flashcards_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.get('/api/flashcards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_public)
        self.assertNotContains(response, self.flashcard_private)
    
    def test_get_flashcards_as_set_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get('/api/flashcards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_public)
        self.assertContains(response, self.flashcard_private)
    
    def test_get_flashcards_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get('/api/flashcards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_public)
        self.assertContains(response, self.flashcard_private)
    # endregion
    # region Get public flashcard by ID
    def test_get_public_flashcard_by_id_as_logged_out_user(self):
        response = self.client.get(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_public_flashcard_by_id_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.get(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_public)
    
    def test_get_public_flashcard_by_id_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_public)
        
    def test_get_public_flashcard_by_id_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_public)
    # endregion
    # region Get private flashcards by ID
    def test_get_private_flashcard_by_id_as_logged_out_user(self):
        response = self.client.get(f'/api/flashcards/{self.flashcard_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_private_flashcard_by_id_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.get(f'/api/flashcards/{self.flashcard_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_private_flashcard_by_id_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.get(f'/api/flashcards/{self.flashcard_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_private)
        
    def test_get_private_flashcard_by_id_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.get(f'/api/flashcards/{self.flashcard_private.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.flashcard_private)
    # endregion
    # endregion
    # region Post
    def test_create_flashcard_as_logged_out_user(self):
        response = self.client.post('/api/flashcards/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_create_flashcard_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.post('/api/flashcards/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_flashcard_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.post('/api/flashcards/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_flashcard_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.post('/api/flashcards/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    # endregion
    # region Put
    def test_put_flashcard_as_logged_out_user(self):
        response = self.client.put(f'/api/flashcards/{self.flashcard_public.id}/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_put_flashcard_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.put(f'/api/flashcards/{self.flashcard_public.id}/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_put_flashcard_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.put(f'/api/flashcards/{self.flashcard_public.id}/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_put_flashcard_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.put(f'/api/flashcards/{self.flashcard_public.id}/', data={
                "question": "Question 1",
                "answer": "Answer",
                "difficulty": "easy",
                "flashcard_set": 1
            })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    # endregion
    # region Delete
    def test_delete_flashcard_as_logged_out_user(self):
        response = self.client.delete(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_delete_flashcard_as_standard_user(self):
        self.client.login(username="standard_user", password="standard_password")
        response = self.client.delete(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_flashcard_as_owner(self):
        self.client.login(username="owner", password="owner_password")
        response = self.client.delete(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # Superusers should be able to delete cards but not modify them
    def test_delete_flashcard_as_superuser(self):
        self.client.login(username="super_user", password="super_password")
        response = self.client.delete(f'/api/flashcards/{self.flashcard_public.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    # endregion
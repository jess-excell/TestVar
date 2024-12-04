from django.test import TestCase
from django.contrib.auth.models import User
from flashcard.models import FlashCard, FlashcardSet, FlashcardCollection

class FlashcardCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.other_user = User.objects.create_user(username="standard_user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
        
        cls.public_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.public_set = FlashcardSet.objects.create(
            title="Public set title", 
            flashcard_collection=cls.public_collection, 
            description="Description" )
        cls.public_flashcard = FlashCard.objects.create(
            question="Public question", 
            answer="Public answer", 
            difficulty="easy",
            flashcard_set=cls.public_set)
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
        cls.private_flashcard = FlashCard.objects.create(
            question="Private question", 
            answer="Private answer", 
            difficulty="easy",
            flashcard_set=cls.private_set)
        
    def test_get_create_flashcard_as_logged_out_user(self):
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/create", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertContains(response, "Log in")
    
    def test_get_create_flashcard_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/create", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_create_flashcard_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/create", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_create_flashcard_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/create", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertEqual(response.status_code, 404)
        
class FlashcardReadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.other_user = User.objects.create_user(username="standard_user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
        
        cls.public_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.public_set = FlashcardSet.objects.create(
            title="Public set title", 
            flashcard_collection=cls.public_collection, 
            description="Description" )
        cls.public_flashcard = FlashCard.objects.create(
            question="Public question", 
            answer="Public answer", 
            difficulty="easy",
            flashcard_set=cls.public_set)
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
        cls.private_flashcard = FlashCard.objects.create(
            question="Private question", 
            answer="Private answer", 
            difficulty="easy",
            flashcard_set=cls.private_set)
    
    def test_get_public_listed_flashcards_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}")
        self.assertContains(response, self.public_flashcard)
    
    def test_get_private_listed_flashcards_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_listed_flashcards_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_listed_flashcards_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertContains(response, self.private_flashcard)
    
    def test_get_private_listed_flashcards_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertContains(response, self.private_flashcard)
        
    def test_get_public_flashcard_info_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}/{self.public_flashcard.id}")
        self.assertContains(response, self.public_flashcard)
    
    def test_get_private_flashcard_info_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_flashcard_info_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_flashcard_info_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}")
        self.assertContains(response, self.private_flashcard)
    
    def test_get_private_flashcard_info_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}")
        self.assertContains(response, self.private_flashcard)

class FlashcardUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.other_user = User.objects.create_user(username="standard_user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
        
        cls.public_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.public_set = FlashcardSet.objects.create(
            title="Public set title", 
            flashcard_collection=cls.public_collection, 
            description="Description" )
        cls.public_flashcard = FlashCard.objects.create(
            question="Public question", 
            answer="Public answer", 
            difficulty="easy",
            flashcard_set=cls.public_set)
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
        cls.private_flashcard = FlashCard.objects.create(
            question="Private question", 
            answer="Private answer", 
            difficulty="easy",
            flashcard_set=cls.private_set)
    
    def test_get_put_flashcard_as_logged_out_user(self):
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/update", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertContains(response, "Log in")

    def test_get_put_flashcard_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/update", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_put_flashcard_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/update", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_put_flashcard_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/update", data={
            "question": "Question 1",
            "answer": "Answer",
            "difficulty": "easy",
            "flashcard_set": self.private_set.id
        }, follow=True)
        self.assertEqual(response.status_code, 404)

class FlashcardDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.other_user = User.objects.create_user(username="standard_user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
        
        cls.public_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.public_set = FlashcardSet.objects.create(
            title="Public set title", 
            flashcard_collection=cls.public_collection, 
            description="Description" )
        cls.public_flashcard = FlashCard.objects.create(
            question="Public question", 
            answer="Public answer", 
            difficulty="easy",
            flashcard_set=cls.public_set)
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
        cls.private_flashcard = FlashCard.objects.create(
            question="Private question", 
            answer="Private answer", 
            difficulty="easy",
            flashcard_set=cls.private_set)
    
    def test_get_delete_flashcard_as_logged_out_user(self):
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/delete", follow=True)
        self.assertContains(response, "Log in")
    
    def test_get_delete_flashcard_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/delete", follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_delete_flashcard_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/delete", follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_delete_flashcard_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}/delete", follow=True)
        self.assertEqual(response.status_code, 200)
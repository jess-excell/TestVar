from django.test import TestCase
from django.contrib.auth.models import User
from flashcard.models import FlashCard, FlashcardSet, FlashcardCollection

class FlashcardTemplateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password")
        
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
    
    def test_template_used_read_public(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}/{self.public_flashcard.id}")
        self.assertTemplateUsed(response, "flashcard/flashcard_info.html")
    
    def test_templated_used_read_private(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}")
        self.assertTemplateUsed(response, "flashcard/flashcard_info.html")
    
    def test_template_used_404(self):
        # Didn't have time to add a custom 404 template but this would have been the same as the others if not
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/{self.private_flashcard.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_template_used_create(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}/create")
        self.assertTemplateUsed(response, "flashcard/flashcard_create.html")
    
    def test_template_used_update(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}/{self.private_flashcard.id}/update")
        self.assertTemplateUsed(response, "flashcard/flashcard_update.html")
    
    def test_template_used_delete(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}/{self.private_flashcard.id}/delete")
        self.assertTemplateUsed(response, "flashcard/flashcard_delete.html")
    
class FlashcardSetTemplateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password")
        
        cls.public_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.public_set = FlashcardSet.objects.create(
            title="Public set title", 
            flashcard_collection=cls.public_collection, 
            description="Description" )
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
    
    def test_template_used_read_public(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}")
        self.assertTemplateUsed(response, "flashcard/flashcard_list.html")
    
    def test_templated_used_read_private(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertTemplateUsed(response, "flashcard/flashcard_list.html")
    
    def test_template_used_404(self):
        # Didn't have time to add a custom 404 template but this would have been the same as the others if not
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_template_used_create(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/create")
        self.assertTemplateUsed(response, "flashcard/flashcard_set_create.html")
    
    def test_template_used_update(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}/update")
        self.assertTemplateUsed(response, "flashcard/flashcard_set_update.html")
    
    def test_template_used_delete(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}/delete")
        self.assertTemplateUsed(response, "flashcard/flashcard_set_delete.html")

class FlashcardCollectionTemplateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password")
        
        cls.public_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
    
    def test_template_used_read_public(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}")
        self.assertTemplateUsed(response, "flashcard/flashcard_set_list.html")
    
    def test_templated_used_read_private(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertTemplateUsed(response, "flashcard/flashcard_set_list.html")
    
    def test_template_used_404(self):
        # Didn't have time to add a custom 404 template but this would have been the same as the others if not
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_template_used_create(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/create")
        self.assertTemplateUsed(response, "flashcard/flashcard_collection_create.html")
    
    def test_template_used_update(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/update")
        self.assertTemplateUsed(response, "flashcard/flashcard_collection_update.html")
    
    def test_template_used_delete(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/delete")
        self.assertTemplateUsed(response, "flashcard/flashcard_collection_delete.html")
        
        # missing tests for comments
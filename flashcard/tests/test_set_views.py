from django.test import TestCase
from django.contrib.auth.models import User
from flashcard.models import FlashcardSet, FlashcardCollection

class SetCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.other_user = User.objects.create_user(username="standard_user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
        
        cls.public_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
    
    def test_get_create_set_as_logged_out_user(self):
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/create", data={
            "title": "TITLE",
            "description": "DESCRIPTION",
            "flashcard_collection": self.public_collection
        }, follow=True)
        self.assertContains(response, "Log in")
    
    def test_get_create_set_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/create", data={
            "title": "TITLE",
            "description": "DESCRIPTION",
            "flashcard_collection": self.public_collection
        }, follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_create_set_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/create", data={
            "title": "TITLE",
            "description": "DESCRIPTION",
            "flashcard_collection": self.public_collection
        }, follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, "TITLE")
        self.assertContains(response, "DESCRIPTION")
    
    def test_get_create_set_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.post(f"/flashcard/collections/{self.private_collection.id}/create", data={
            "title": "TITLE",
            "description": "DESCRIPTION",
            "flashcard_collection": self.public_collection
        }, follow=True)
        self.assertEqual(response.status_code, 404)

class SetReadTests(TestCase):
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
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
    
    def test_get_public_listed_sets_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}")
        self.assertContains(response, self.public_set)
    
    def test_get_private_listed_sets_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_listed_sets_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_listed_sets_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertContains(response, self.private_set)
    
    def test_get_private_listed_sets_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertContains(response, self.private_set)
        
    def test_get_public_set_info_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}/{self.public_set.id}")
        self.assertContains(response, self.public_set)
    
    def test_get_private_set_info_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_set_info_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_set_info_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertContains(response, self.private_set)
    
    def test_get_private_set_info_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}")
        self.assertContains(response, self.private_set)

class SetUpdateTests(TestCase):
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
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
    
    def test_get_put_set_as_logged_out_user(self):
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/update", data={
            "title": "Updated set title", 
            "flashcard_collection": self.private_collection, 
            "description": "Description"
        }, follow=True)
        self.assertContains(response, "Log in")

    def test_get_put_set_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/update", data={
            "title": "Updated set title", 
            "flashcard_collection": self.private_collection, 
            "description": "Description"
        }, follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_put_set_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/update", data={
            "title": "Updated set title", 
            "flashcard_collection": self.private_collection, 
            "description": "Description"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_put_set_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/update", data={
            "title": "Updated set title", 
            "flashcard_collection": self.private_collection, 
            "description": "Description"
        }, follow=True)
        self.assertEqual(response.status_code, 404)

class SetDeleteTests(TestCase):
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
        
        cls.private_collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=False)
        cls.private_set = FlashcardSet.objects.create(
            title="Private set", 
            flashcard_collection=cls.private_collection,
            description="Private description")
    
    def test_delete_set_as_logged_out_user(self):
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/delete", follow=True)
        self.assertContains(response, "Log in")
    
    def test_get_delete_set_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/delete", follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_delete_set_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/delete", follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_delete_set_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/{self.private_set.id}/delete", follow=True)
        self.assertEqual(response.status_code, 200)
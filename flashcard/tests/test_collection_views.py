from django.test import TestCase
from django.contrib.auth.models import User
from flashcard.models import FlashcardSet, FlashcardCollection

class CollectionCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.other_user = User.objects.create_user(username="standard_user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
    
    def test_get_create_collection_as_logged_out_user(self):
        response = self.client.post(f"/flashcard/collections/create", data={
            "title": "TITLE",
            "description": "DESCRIPTION"
        }, follow=True)
        self.assertContains(response, "Log in")
    
    def test_get_create_collection_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.post(f"/flashcard/collections/create", data={
            "title": "TITLE",
            "description": "DESCRIPTION"
        }, follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, "TITLE")
        self.assertContains(response, "DESCRIPTION")
    
    def test_get_create_collection_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.post(f"/flashcard/collections/create", data={
            "title": "TITLE",
            "description": "DESCRIPTION"
        }, follow=True)
        self.assertEqual(response.status_code, 201)

class CollectionReadTests(TestCase):
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
            title="Collection 2", 
            user=cls.user, 
            public=False)
    
    def test_get_all_collections_logged_out(self):
        response = self.client.get(f"/flashcard/collections")
        self.assertContains(response, self.public_collection)
        self.assertNotContains(response, self.private_collection)
    
    def test_get_all_collections_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.get(f"/flashcard/collections")
        self.assertContains(response, self.public_collection)
        self.assertNotContains(response, self.private_collection)
    
    def test_get_all_collections_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.get(f"/flashcard/collections")
        self.assertContains(response, self.public_collection)
        self.assertContains(response, self.private_collection)
    
    def test_get_all_collections_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collection")
        self.assertContains(response, self.public_collection)
        self.assertContains(response, self.private_collection)
        
    def test_get_public_set_info_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.public_collection.id}")
        self.assertContains(response, self.public_collection)
    
    def test_get_private_set_info_logged_out(self):
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_set_info_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertEqual(response.status_code, 404)
    
    def test_get_private_set_info_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertContains(response, self.private_collection)
    
    def test_get_private_set_info_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.private_collection.id}")
        self.assertContains(response, self.private_collection)

class CollectionUpdateTests(TestCase):
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
    
    def test_get_put_collection_as_logged_out_user(self):
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/update", data={
            "title": "Collection",
            "description": "new description",
            "public": True
        }, follow=True)
        self.assertContains(response, "Log in")

    def test_get_put_collection_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/update", data={
            "title": "Collection",
            "description": "new description",
            "public": True
        }, follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_put_collection_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/update", data={
            "title": "Collection",
            "description": "new description",
            "public": True
        }, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_put_collection_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.put(f"/flashcard/collections/{self.private_collection.id}/update", data={
            "title": "Collection",
            "description": "new description",
            "public": True
        }, follow=True)
        self.assertEqual(response.status_code, 404)

class CollectionDeleteTests(TestCase):
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
    
    def test_delete_set_as_logged_out_user(self):
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/delete", follow=True)
        self.assertContains(response, "Log in")
    
    def test_get_delete_set_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/delete", follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_get_delete_set_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/delete", follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_delete_set_as_admin(self):
        self.client.login(username="super_user", password="password")
        response = self.client.delete(f"/flashcard/collections/{self.private_collection.id}/delete", follow=True)
        self.assertEqual(response.status_code, 200)
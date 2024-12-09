from django.test import TestCase
from django.contrib.auth.models import User
from flashcard.models import FlashcardSet, FlashcardCollection, Comment

class CommentCreateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
        
        cls.collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.set = FlashcardSet.objects.create(
            title="Set", 
            flashcard_collection=cls.collection,
            description="Description")
    
    def test_create_comment_as_logged_out_user(self):
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/comments/create", data={
            "flashcard_set": self.set.id,
            "comment": "comment"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(response["Location"], f"/login?next=/flashcard/collections/{self.collection.id}/{self.set.id}/comments/create")
    
    def test_create_comment_as_standard_user(self):
        self.client.login(username="user", password="password")
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/comments/create", data={
            "flashcard_set": self.set.id,
            "comment": "comment"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/flashcard/collections/{self.collection.id}/{self.set.id}/comments")
        
class CommentReadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.other_user = User.objects.create_user(username="standard_user", password="password")
        cls.super_user = User.objects.create_superuser(username="super_user", password="password")
        
        cls.collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.set = FlashcardSet.objects.create(
            title="Set", 
            flashcard_collection=cls.collection,
            description="Description")
        cls.comment = Comment.objects.create(
            user=cls.user,
            flashcard_set=cls.set,
            comment="TEST"
        )
    
    def test_get_comments_as_logged_out_user(self):
        response = self.client.get(f"/flashcard/collections/{self.collection.id}/{self.set.id}/comments")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.comment.comment)
    
    def test_get_comments_as_standard_user(self):
        self.client.login(username="user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.collection.id}/{self.set.id}/comments")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.comment.comment)
    
    def test_get_comments_as_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.collection.id}/{self.set.id}/comments")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.comment.comment)

# Only need read and create (similar to post commets).    
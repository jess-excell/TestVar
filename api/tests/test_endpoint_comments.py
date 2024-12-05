from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from flashcard.models import FlashcardSet, FlashcardCollection, Comment

class TestCommentEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Shared setup for all tests
        cls.superuser = User.objects.create_superuser(
            username="superuser", 
            password="superpassword")
        cls.standard_user = User.objects.create_user(
            username="standard_user", 
            password="userpassword")
        cls.standard_user_flashcard_collection = FlashcardCollection.objects.create(
            title="Test Collection", 
            user=cls.standard_user, 
            public=True)
        cls.standard_user_flashcard_set = FlashcardSet.objects.create(
            title="Test Set",
            flashcard_collection=cls.standard_user_flashcard_collection,
            description="Unowned Flashcard Set"
        )

    def setUp(self):
        self.client.logout()

    def test_get_comments_as_logged_out_user(self):
        response = self.client.get("/api/comments/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_comment_as_logged_out_user(self):
        response = self.client.post("/api/comments/", data={"comment": "test", "flashcard_set": self.standard_user_flashcard_set.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comments_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.get("/api/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_comment_as_standard_user(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.post("/api/comments/", data={
            "comment": "TEST COMMENT",
            "flashcard_set": self.standard_user_flashcard_set.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment"], "TEST COMMENT")
        
    def test_post_comment_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.post("/api/comments/", data={
            "comment": "TEST COMMENT",
            "flashcard_set": self.standard_user_flashcard_set.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment"], "TEST COMMENT")

    def test_post_blank_comment_field(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.post("/api/comments/", data={
            "comment": "",
            "flashcard_set": self.standard_user_flashcard_set.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_post_nonexistent_set(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.post("/api/comments/", data={
            "comment": "TEST COMMENT",
            "flashcard_set": 999
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post_private_set(self):
        priv_collection = FlashcardCollection.objects.create(title="test col priv",
            description="",
            user=self.superuser,
            public=False
        )
        priv_set = FlashcardSet.objects.create(
            title="Test Set",
            flashcard_collection=priv_collection,
            description="Unowned Flashcard Set"
        )
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.post("/api/comments/", data={
            "comment": "TEST COMMENT",
            "flashcard_set": priv_set.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_own_comment(self):
        comment = Comment.objects.create(
            comment="Test", 
            flashcard_set=self.standard_user_flashcard_set, 
            user=self.standard_user)
        
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.patch(f"/api/comments/{comment.id}/", data={
            "comment": "updated comment",
            "flashcard_set": self.standard_user_flashcard_set,
            "user": self.standard_user
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["comment"], "updated comment")
    
    def test_put_different_user(self):
        comment = Comment.objects.create(
            comment="test",
            flashcard_set=self.standard_user_flashcard_set,
            user=self.superuser)
        
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.patch(f"/api/comments/{comment.id}/", data={
            "comment": "updated comment",
            "flashcard_set": self.standard_user_flashcard_set,
            "user": self.standard_user
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_unowned_comment(self):
        comment = Comment.objects.create(
            comment="test",
            flashcard_set=self.standard_user_flashcard_set,
            user=self.superuser)
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.delete(f"/api/comments/{comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(comment)
    
    def test_delete_owned_comment(self):
        comment = Comment.objects.create(
            comment="test",
            flashcard_set=self.standard_user_flashcard_set,
            user=self.standard_user)
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.delete(f"/api/comments/{comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.contains(comment))
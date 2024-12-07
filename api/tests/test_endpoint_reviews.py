from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from flashcard.models import FlashcardSet, FlashcardCollection, Review

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
        cls.other_user = User.objects.create_user(
            username="second_user", 
            password="userpassword")
        cls.collection = FlashcardCollection.objects.create(
            title="Test Collection", 
            user=cls.standard_user, 
            public=True)
        cls.set = FlashcardSet.objects.create(
            title="Test Set",
            flashcard_collection=cls.collection,
            description="Flashcard Set"
        )
        cls.other_set = FlashcardSet.objects.create(
            title="Other Set",
            flashcard_collection=cls.collection
        )
        cls.review=Review.objects.create(
            rating=3,
            user=cls.standard_user,
            comment="test comment",
            flashcard_set=cls.set
        )
    
    def test_get_reviews_as_logged_out_user(self):
        response = self.client.get("/api/reviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.review.rating)
        self.assertContains(response, self.review.user.id)
        self.assertContains(response, self.review.comment)
        self.assertContains(response, self.review.flashcard_set.id)
        # Arguably should check for private / public reviews but also private set reviews don't make sense. Although nothing stops users from creating reviews for private sets atm, this should be added in the future ideally
        
    def test_get_reviews_as_standard_user(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.get("/api/reviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.review.rating)
        self.assertContains(response, self.review.user.id)
        self.assertContains(response, self.review.comment)
        self.assertContains(response, self.review.flashcard_set.id)
    
    def test_get_reviews_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.get("/api/reviews/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.review.rating)
        self.assertContains(response, self.review.user.id)
        self.assertContains(response, self.review.comment)
        self.assertContains(response, self.review.flashcard_set.id)
    
    def test_post_second_review_same_set(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.post("/api/reviews/", data={
            "flashcard_set": self.set.id,
            "rating": 4,
            "comment": "Second comment",
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_review(self):
        self.client.login(username="second_user", password="userpassword")
        response = self.client.post("/api/reviews/", data={
            "flashcard_set": self.set.id,
            "rating": 4,
            "comment": "Second comment",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["comment"], "Second comment")
        self.assertEqual("Second comment", response.data["comment"])
    
    def test_post_review_nonexistent_set(self):
        self.client.login(username="second_user", password="userpassword")
        response = self.client.post("/api/reviews/", data={
            "flashcard_set": 444,
            "rating": 4,
            "comment": "Second comment",
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_nonextistent_comment(self):
        self.client.login(username="second_user", password="userpassword")
        response = self.client.put("/api/reviews/999/", data={
            "flashcard_set": 444,
            "rating": 4,
            "comment": "Second comment",
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_move_existing_review_to_other_set(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.put(f"/api/reviews/{self.review.id}/", data={
            "flashcard_set": self.other_set.id,
            "rating": "4",
            "comment": "Second comment",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["flashcard_set"], self.set.id)
    
    def test_put_unowned_review(self):
        self.client.login(username="second_user", password="userpassword")
        response = self.client.put(f"/api/reviews/{self.review.id}/", data={
            "flashcard_set": self.set.id,
            "rating": 3,
            "comment": "Second comment",
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_put_review_rating(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.put(f"/api/reviews/{self.review.id}/", data={
            "flashcard_set": self.set.id,
            "rating": 2,
            "comment": "Second comment",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["rating"], 2)
    
    def test_put_review_comment(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.put(f"/api/reviews/{self.review.id}/", data={
            "flashcard_set": self.set.id,
            "rating": 4,
            "comment": "Updated comment",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["comment"], "Updated comment")
    
    def test_delete_review(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.delete(f"/api/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_nonexistent_review(self):
        self.client.login(username="standard_user", password="userpassword")
        response = self.client.delete("/api/reviews/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_unowned_review_standard_user(self):
        self.client.login(username="second_user", password="userpassword")
        response = self.client.delete("/api/reviews/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)       
    
    def test_delete_review_as_superuser(self):
        self.client.login(username="superuser", password="superpassword")
        response = self.client.delete(f"/api/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)           
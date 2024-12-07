from django.test import TestCase
from django.contrib.auth.models import User
from flashcard.models import FlashcardSet, FlashcardCollection, Review

class ReviewCreateTests(TestCase):
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
    
    def test_create_reviews_as_logged_out_user(self):
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/create", data={
            "flashcard_set": self.set.id,
            "rating": 4,
            "comment": "comment"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/login?next=/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/create")
    
    def test_create_reviews_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/create", data={
            "flashcard_set": self.set.id,
            "rating": 4,
            "comment": "comment"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews")
    
    def test_create_reviews_as_owner(self):
        review = Review.objects.create(
            user=self.user,
            flashcard_set=self.set,
            comment="TEST",
            rating=2
        )
        self.client.login(username="owner", password="password")
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/create", data={
            "flashcard_set": self.set,
            "rating": 4,
            "comment": "comment"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{review.id}/update")
    
class ReviewReadTests(TestCase):
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
        cls.review = Review.objects.create(
            user=cls.user,
            flashcard_set=cls.set,
            comment="TEST",
            rating=2
        )
    
    def test_get_reviews_as_logged_out_user(self):
        response = self.client.get(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.comment)
    
    def test_get_reviews_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.comment)
    
    def test_get_reviews_as_superuser(self):
        self.client.login(username="super_user", password="password")
        response = self.client.get(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.comment)
    
class ReviewUpdateTests(TestCase):
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
        cls.review = Review.objects.create(
            user=cls.user,
            flashcard_set=cls.set,
            comment="TEST",
            rating=2
        )
    
    def test_put_review_as_logged_out_user(self):
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/update", data={
            "flashcard_set": self.set,
            "rating": 3,
            "comment": "comment"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/login?next=/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/update")
    
    def test_put_review_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/update", data={
            "flashcard_set": self.set,
            "rating": 3,
            "comment": "new comment"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews")

    def test_put_review_invalid_rating(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/update", data={
            "flashcard_set": self.set,
            "rating": "This is not a number",
            "comment": "new comment"
        })
        self.assertFormError(response, "form", "rating", "Enter a whole number.")
    
class ReviewDeleteTests(TestCase):
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
        cls.review = Review.objects.create(
            user=cls.user,
            flashcard_set=cls.set,
            comment="TEST",
            rating=2
        )
    
    def test_delete_review_as_logged_out_user(self):
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/delete")
        self.assertRedirects(response, f"/login?next=/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/delete")
    
    def test_delete_review_as_standard_user(self):
        self.client.login(username="standard_user", password="password")
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/delete", follow=True)
        self.assertEqual(response.status_code, 403)
    
    def test_delete_review_as_owner(self):
        self.client.login(username="owner", password="password")
        response = self.client.post(f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews/{self.review.id}/delete")
        self.assertRedirects(response, f"/flashcard/collections/{self.collection.id}/{self.set.id}/reviews", status_code=302, target_status_code=200)
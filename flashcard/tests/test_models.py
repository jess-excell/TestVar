from django.test import TestCase
from django.contrib.auth.models import User
from flashcard.models import FlashCard, FlashcardSet, FlashcardCollection, Comment
from django.utils import timezone

class TestFlashcard(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.set = FlashcardSet.objects.create(
            title="Set", 
            flashcard_collection=cls.collection, 
            description="Description")
        cls.flashcard = FlashCard.objects.create(
            question="Flashcard",
            answer="ANSWER",
            difficulty="hard",
            flashcard_set=cls.set
        )
    
    def test_get_set_from_flashcard(self):
        self.assertEqual(self.flashcard.flashcard_set, self.set)
    
    def test_get_collection_from_flashcard(self):
        self.assertEqual(self.flashcard.flashcard_set.flashcard_collection, self.collection)
    
    # region create
    def test_create_flashcard(self):
        initial_count = self.set.flashcard.all().count()
        FlashCard.objects.create(
            question="New flashcard",
            answer="ANSWER",
            difficulty="hard",
            flashcard_set=self.set
        )
        final_count = self.set.flashcard.all().count()
        self.assertEqual(initial_count + 1, final_count) # Can't do assertContains so this checks instead that the object has been added
    
    def test_create_flashcard_no_question(self):
        with self.assertRaises(Exception):
            FlashCard.objects.create(
                answer="ANSWER",
                difficulty="easy",
                flashcard_set=self.set
            )
    
    def test_create_flashcard_no_answer(self):
        with self.assertRaises(Exception):
            FlashCard.objects.create(
                question="New flashcard",
                difficulty="easy",
                flashcard_set=self.set
            )
            
    def test_create_flashcard_no_difficulty(self):
        with self.assertRaises(Exception):
            FlashCard.objects.create(
                question="New flashcard",
                answer="ANSWER",
                flashcard_set=self.set
            )
    
    def test_create_flashcard_no_set(self):
        with self.assertRaises(Exception):
            FlashCard.objects.create(
                question="New flashcard",
                answer="ANSWER",
                difficulty="easy",
            )
    
    def test_create_flashcard_invalid_difficulty(self):
        with self.assertRaises(Exception):
            FlashCard.objects.create(
                question="New flashcard",
                answer="ANSWER",
                difficulty="super easy",
                flashcard_set=self.set
            )
    
    def test_create_flashcard_invalid_set(self):
        with self.assertRaises(Exception):
            FlashCard.objects.create(
                question="New flashcard",
                answer="ANSWER",
                difficulty="easy",
                flashcard_set=88888
            )
    # endregion
    
    def test_delete_flashcard(self):
        initial_count = self.set.flashcard.all().count()
        self.flashcard.delete()
        final_count = self.set.flashcard.all().count()
        self.assertEqual(initial_count - 1, final_count)
        
        self.assertIsNotNone(FlashcardSet.objects.get(pk=self.set.id))
        self.assertIsNotNone(FlashcardCollection.objects.get(pk=self.collection.id))
        
    def test_to_string(self):
        self.assertEqual(str(self.flashcard), self.flashcard.question)

class TestFlashcardSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.set = FlashcardSet.objects.create(
            title="Public set title", 
            flashcard_collection=cls.collection, 
            description="Description" )
        FlashCard.objects.create(
            question="Card 1",
            answer="ANSWER",
            difficulty="hard",
            flashcard_set=cls.set
        )
        FlashCard.objects.create(
            question="Card 2",
            answer="ANSWER",
            difficulty="hard",
            flashcard_set=cls.set
        )
        cls.comment = Comment.objects.create(
            comment="Test comment",
            flashcard_set=cls.set,
            user=cls.user
        )
    
    def test_get_collection_from_set(self):
        self.assertEqual(self.collection, self.set.flashcard_collection)
    
    def test_get_flashcards_from_set(self):
        flashcards = self.set.flashcard.all()
        flashcards.get(question="Card 1")
        flashcards.get(question="Card 2")
    
    # region Create 
    def test_create_set(self):
        initial_count = self.collection.flashcard_set.all().count()
        new_set = FlashcardSet.objects.create(
            title="New set",
            flashcard_collection=self.collection,
            description="Description"
        )
        final_count = self.collection.flashcard_set.all().count()
        self.assertEqual(initial_count + 1, final_count) # Can't do assertContains so this checks instead that the object has been added
        
        self.assertIsNotNone(new_set.created_at)
        self.assertIsNotNone(new_set.updated_at)
        
        time = timezone.now() + timezone.timedelta(milliseconds=500) # Add some milliseconds just to be safe
        self.assertTrue(new_set.created_at<time)
        self.assertTrue(new_set.updated_at<time)
        self.assertTrue(time-new_set.created_at<timezone.timedelta(milliseconds=1000))
    
    def test_create_set_no_description(self):
        FlashcardSet.objects.create(
            title="New set",
            flashcard_collection=self.collection
        )
        
    def test_create_set_large_title(self):
        with self.assertRaises(Exception):
            FlashcardSet.objects.create(
                title="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                flashcard_collection=self.collection,
                description="Description"
            )  
    
    def test_create_set_no_title(self):
        with self.assertRaises(Exception):
            FlashcardSet.objects.create(
                flashcard_collection=self.collection,
                description="Description"
            )
    
    def test_create_set_no_collection(self):
        with self.assertRaises(Exception):
            FlashcardSet.objects.create(
                title="New set",
                description="Description"
            ) 
    
    def test_destroy_set(self):
        initial_count = self.collection.flashcard_set.all().count()
        self.set.delete()
        final_count = self.collection.flashcard_set.all().count()
        self.assertEqual(initial_count - 1, final_count)
        
        # Ensure delete cascades
        with self.assertRaises(Exception):
            FlashcardSet.objects.get(pk=self.set.id)
        with self.assertRaises(Exception):
            Comment.objects.get(pk=self.comment.id)
        self.assertIsNotNone(FlashcardCollection.objects.get(pk=self.collection.id))

    def test_to_string(self):
        self.assertEqual(str(self.set), self.set.title)

class TestFlashcardCollection(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.set = FlashcardSet.objects.create(
            title="Set", 
            flashcard_collection=cls.collection, 
            description="Description")
        cls.flashcard = FlashCard.objects.create(
            question="Flashcard",
            answer="ANSWER",
            difficulty="hard",
            flashcard_set=cls.set
        )
    
    def test_create_collection(self):
        count_before = FlashcardCollection.objects.count()
        FlashcardCollection.objects.create(
            title="New collection",
            user=self.user
        )
        count_after = FlashcardCollection.objects.count()
        self.assertEqual(count_before + 1, count_after)
    
    def test_create_collection_long_title(self):
        with self.assertRaises(Exception):
            FlashcardCollection.objects.create(
                title="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                user=self.user
            )
    
    def test_create_collection_invalid_user(self):
        with self.assertRaises(Exception):
            FlashcardCollection.objects.create(
                title="New collection",
                user=0
            )

    def test_delete_collection(self):
        count_before = FlashcardCollection.objects.count()
        self.collection.delete()
        count_after = FlashcardCollection.objects.count()
        self.assertEqual(count_before - 1, count_after)
        
        # Ensure delete cascades
        with self.assertRaises(Exception):
            FlashCard.objects.get(pk=self.flashcard.id)
        with self.assertRaises(Exception):
            FlashcardSet.objects.get(pk=self.set.id)

class TestComments(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="owner", password="password")
        cls.collection = FlashcardCollection.objects.create(
            title="Collection", 
            user=cls.user, 
            public=True)
        cls.set = FlashcardSet.objects.create(
            title="Set", 
            flashcard_collection=cls.collection, 
            description="Description")
        cls.comment = Comment.objects.create(
            comment="Test comment",
            flashcard_set=cls.set,
            user=cls.user
        )
    
    def test_create_comment(self):
        count_before = Comment.objects.count()
        Comment.objects.create(
            comment="New comment",
            user=self.user,
            flashcard_set=self.set
        )
        count_after = Comment.objects.count()
        self.assertEqual(count_before + 1, count_after)
    
    def test_create_comment_no_user(self):
        with self.assertRaises(Exception):
            Comment.objects.create(
            comment="New comment",
            flashcard_set=self.set
        )
    
    def test_create_comment_invalid_user(self):
        with self.assertRaises(Exception):
            Comment.objects.create(
            comment="New comment",
            user=999,
            flashcard_set=self.set
        )

    def test_create_comment_no_comment(self):
        with self.assertRaises(Exception):
            Comment.objects.create(
            user=self.user,
            flashcard_set=self.set
        )
    
    def test_create_comment_no_set(self):
        with self.assertRaises(Exception):
            Comment.objects.create(
            comment="New comment",
            user=self.user
        )
    
    def test_create_comment_invalid_set(self):
        with self.assertRaises(Exception):
            Comment.objects.create(
            comment="New comment",
            user=self.user,
            flashcard_set=999
        )
    
    def test_delete_comment(self):
        initial_count = Comment.objects.count()
        self.comment.delete()
        final_count = Comment.objects.count()
        self.assertEqual(initial_count - 1, final_count)
    
    def test_to_string(self):
        self.assertEqual(self.comment.comment, str(self.comment))
from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.
class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class FlashcardCollection(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flashcard_collection")
    description = models.TextField(default=None, blank=True, null=True)
    
class FlashcardSet(models.Model):
    title = models.CharField(max_length=100)
    flashcard_collection = models.ForeignKey(FlashcardCollection, on_delete=models.CASCADE, related_name="flashcard_set")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default=None, blank=True, null=True)

class FlashCard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.TextField(
        choices=[(tag.value, tag.name.title()) for tag in Difficulty]
    )
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name="flashcard")

# class Comment(models.Model):
#     comment = models.TextField()
#     set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name="comments")
#     author = models.User()
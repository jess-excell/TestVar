from django.db import models
from enum import Enum

# Create your models here.
class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class FlashCard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.TextField(
        choices=[(tag.value, tag.name.title()) for tag in Difficulty]
    )

# class FlashcardSet(models.Model):
#     name = models.TextField()
#     cards = models.ManyToOneField(FlashCard, related_name="sets")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)

# class Comment(models.Model):
#     comment = models.TextField()
#     set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name="comments")
#     author = models.User()
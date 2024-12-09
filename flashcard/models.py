from django.db import models
from enum import Enum
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

# Create your models here.
class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class FlashcardCollection(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flashcard_collection")
    description = models.TextField(default=None, blank=True, null=True)
    public = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
class FlashcardSet(models.Model):
    title = models.CharField(max_length=100)
    flashcard_collection = models.ForeignKey(FlashcardCollection, on_delete=models.CASCADE, related_name="flashcard_set")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(default=None, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class FlashCard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.TextField(
        choices=[(tag.value, tag.name.title()) for tag in Difficulty]
    )
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name="flashcard")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        self.flashcard_set.updated_at = now()
        self.flashcard_set.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.question

class Comment(models.Model):
    comment = models.TextField()
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.comment

class Review(models.Model):
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name="review")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(default=None, blank=True, null=True)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        if not self.rating.is_integer:
            raise ValidationError("Rating must be an integer.")
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "@" + self.user.username + " | Rating: " + str(self.rating)
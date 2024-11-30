from flashcard.models import FlashCard, FlashcardSet, FlashcardCollection, Comment
from django.contrib.auth.models import User
from rest_framework import serializers
import datetime

class FlashCardSerializer(serializers.ModelSerializer):
    flashcard_set = serializers.PrimaryKeyRelatedField(queryset=FlashcardSet.objects.all())
    user = serializers.ReadOnlyField(source="flashcard_set.flashcard_collection.user.username")
    
    class Meta:
        model = FlashCard
        fields = ["id", "question", "answer", "difficulty", "flashcard_set", "user"]
        read_only_fields = ["id", "user"]
        
class FlashcardSetSerializer(serializers.ModelSerializer):
    flashcard_collection = serializers.PrimaryKeyRelatedField(queryset=FlashcardCollection.objects.all())
    owner = serializers.ReadOnlyField(source="flashcard_collection.user.username")
    
    class Meta:
        model = FlashcardSet
        fields = ["id", "title", "description", "created_at", "updated_at", "owner", "flashcard_collection", "comments", "flashcard"]
        read_only_fields = ["created_at", "update_at", "owner", "flashcard", "comments"]
        
    # Update updated_at when modified
    def update(self, instance, validated_data):
        validated_data["updated_at"] = datetime.datetime.now()
        return super().update(instance, validated_data)

class FlashcardCollectionSerializer(serializers.ModelSerializer):        
    class Meta:
        model = FlashcardCollection
        fields = ["id", "title", "description", "public", "user", "flashcard_set"]
        read_only_fields = ["user", "flashcard_set"]
        
    # Add user id to created set
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):        
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ["id", "username", "password", "is_superuser", "is_staff", "comment"]
        read_only_fields = ["comment", "is_superuser"]
        
    def update(self, instance, validated_data):
        # Handle password not overwritten
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)   
        return super().update(instance, validated_data)
        
class CommentSerializer(serializers.ModelSerializer):
    flashcard_set = serializers.PrimaryKeyRelatedField(queryset=FlashcardSet.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ["id", "comment", "flashcard_set", "user"]
    
    # Add user id to created set
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    # Ensure you can only add a flashcard set when creating the comment, and can't change it after this
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["flashcard_set"].read_only = True
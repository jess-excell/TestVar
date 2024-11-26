#from django.contrib.auth.models import user
from flashcard.models import *
from .serializers import *
from rest_framework import viewsets, permissions
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return FlashCard.objects.all()
        else:
            return FlashCard.objects.filter(Q(flashcard_set__flashcard_collection__user=self.request.user) | Q(flashcard_set__flashcard_collection__public=True))
    
    def create(self, request, *args, **kwargs):
        flashcard_set = get_object_or_404(FlashcardSet, id=request.data.get("flashcard_set"))
        flashcard_collection = flashcard_set.flashcard_collection
        # if don't own set don't let them add to it
        if request.user != flashcard_collection.user:
            return HttpResponseNotAllowed("You are trying to add a set to a collection that you do not own.")
        else:
            return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)

class FlashcardSetViewSet(viewsets.ModelViewSet) :
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return FlashcardSet.objects.all()
        else:
            return FlashcardSet.objects.filter(Q(flashcard_collection__user=self.request.user) | Q(flashcard_collection__public=True))
    
    def create(self, request, *args, **kwargs):
        if FlashcardSet.objects.filter(created_at__date = datetime.datetime.now()).count() > 19:
            return HttpResponseNotAllowed("The daily limit for flashcards created has been reached. Please remove an existing set created today or try again tomorrow.")
        
        flashcard_collection = get_object_or_404(FlashcardCollection, id=request.data.get("flashcard_collection"))
        
        if request.user != flashcard_collection.user:
            return HttpResponseNotAllowed("You are trying to add a set to a collection that you do not own.")
        else:
            return super().create(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        flashcard_collection = get_object_or_404(FlashcardCollection, id=request.data.get("flashcard_collection"))
        
        if flashcard_collection.user != request.user:
            return HttpResponseNotAllowed("You are trying to move this set to a collection that you do not own.")
        # update time
        return super().update(request, *args, **kwargs)

class FlashcardCollectionViewSet(viewsets.ModelViewSet):
    queryset = FlashcardCollection.objects.all()
    serializer_class = FlashcardCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if (not self.request.user.is_superuser):
            return FlashcardCollection.objects.filter(Q(user=self.request.user) | Q(public=True))
        else:
            return FlashcardCollection.objects.all()
        
    def update(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseNotAllowed("You are trying to change the owner of a set. This is forbidden.")
        else:
            return super().update(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseNotAllowed("You do not have permission to delete this set.")
        else:
            return super().destroy(request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    
    def get_queryset(self):
        if (not self.request.user.is_superuser):
            return Comment.objects.filter(Q(user=self.request.user) | Q(flashcard_set__flashcard_collection__public=True))
        else:
            return Comment.objects.all()
    
    def update(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseNotAllowed("You do not have permission to modify this set.")
        else:
            return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseNotAllowed("You do not have permission to delete this set.")
        else:
            return super().destroy(request, *args, **kwargs)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
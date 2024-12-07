#from django.contrib.auth.models import user
from flashcard.models import *
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import get_object_or_404
import datetime
from .variables import API_VERSION

class FlashcardViewSet(viewsets.ModelViewSet):
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
    def get_queryset(self):
        if self.request.user.is_superuser:
            return FlashCard.objects.all()
        if self.request.user.is_authenticated:
            return FlashCard.objects.filter(Q(flashcard_set__flashcard_collection__user=self.request.user) | Q(flashcard_set__flashcard_collection__public=True))
        return FlashCard.objects.filter(flashcard_set__flashcard_collection__public=True)
    
    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have permission to add to this set.")
        
        flashcard_set = get_object_or_404(FlashcardSet, id=request.data.get("flashcard_set"))
        flashcard_collection = flashcard_set.flashcard_collection
        
        if self.request.user != flashcard_collection.user:
            return HttpResponseForbidden("You are trying to add a set to a collection that you do not own.")
        else:
            return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have permission to add to this set.")
        
        flashcard_set = get_object_or_404(FlashcardSet, id=request.data.get("flashcard_set"))
        flashcard_collection = flashcard_set.flashcard_collection
        
        if self.request.user != flashcard_collection.user:
            return HttpResponseForbidden("You do not have permission to modify this.")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have permission to add to this set.")
        
        flashcard = get_object_or_404(FlashCard, id=self.kwargs.get("pk"))
        flashcard_collection = flashcard.flashcard_set.flashcard_collection
        
        if not self.request.user.is_superuser and self.request.user != flashcard_collection.user:
            return HttpResponseForbidden("You do not have permission to modify this.")
        return super().destroy(request, *args, **kwargs)

class FlashcardSetViewSet(viewsets.ModelViewSet) :
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return FlashcardSet.objects.all()
        if self.request.user.is_authenticated:
            return FlashcardSet.objects.filter(Q(flashcard_collection__user=self.request.user) | Q(flashcard_collection__public=True))
        return FlashcardSet.objects.filter(flashcard_collection__public=True)
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseNotAllowed("Please log in to create a set.")
        
        if FlashcardSet.objects.filter(created_at__date = datetime.datetime.now()).count() > 19:
            return HttpResponseNotAllowed("The daily limit for flashcards created has been reached. Please remove an existing set created today or try again tomorrow.")
        
        flashcard_collection = get_object_or_404(FlashcardCollection, id=request.data.get("flashcard_collection"))
        
        if request.user != flashcard_collection.user:
            return HttpResponseForbidden("You are trying to add a set to a collection that you do not own.")
        else:
            return super().create(request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseForbidden("You do not have permission to modify this.")
        
        flashcard_set_id = self.kwargs.get("pk")
        flashcard_set = get_object_or_404(FlashcardSet, id=flashcard_set_id)
        
        if flashcard_set.flashcard_collection.user != request.user:
            return HttpResponseForbidden("You are trying to move this set to a collection that you do not own.")
        # update time
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseForbidden("You do not have permission to modify this.")
        
        flashcard_set_id = self.kwargs.get("pk")
        flashcard_set = get_object_or_404(FlashcardSet, id=flashcard_set_id)
        
        if not request.user.is_superuser and flashcard_set.flashcard_collection.user != request.user:
            return HttpResponseForbidden("You do not have permission to modify this.")
        return super().destroy(request, *args, **kwargs)

class FlashcardCollectionViewSet(viewsets.ModelViewSet):
    queryset = FlashcardCollection.objects.all()
    serializer_class = FlashcardCollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return FlashcardCollection.objects.all()
        if self.request.user.is_authenticated:
            return FlashcardCollection.objects.filter(Q(user=self.request.user) | Q(public=True))
        return FlashcardCollection.objects.filter(public=True)
    
    def update(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated or request.user != self.get_object().user:
            return HttpResponseForbidden("You don't have permission to modify this set.")
        return super().update(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You don't have permission to delete this.")
        if not self.request.user.is_superuser and request.user != self.get_object().user:
            return HttpResponseForbidden("You don't have permission to delete this.")
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
        
    def create(self, request, *args, **kwargs):
        flashcard_set = get_object_or_404(FlashcardSet, id=request.data.get("flashcard_set"))
        flashcard_collection = flashcard_set.flashcard_collection
        if ((request.user != flashcard_collection.user) and not flashcard_collection.public):
            return HttpResponseForbidden("You are trying to add a comment to a private set that you do not own.")
        else:
            return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseForbidden("You do not have permission to modify this set.")
        else:
            return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseForbidden("You do not have permission to delete this set.")
        else:
            return super().destroy(request, *args, **kwargs)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            if self.request.user == self.get_object():
                return super().destroy(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to delete another user.") 
        if self.get_object().is_superuser:
            return HttpResponseForbidden("You do not have permission to delete a superuser.")
        return super().destroy(request, *args, **kwargs)
    
    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        if self.action == "destroy":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Review.objects.all()
        if self.request.user.is_authenticated:
            return Review.objects.filter(Q(user=self.request.user) | Q(flashcard_set__flashcard_collection__public=True))
        return Review.objects.filter(flashcard_set__flashcard_collection__public=True)
    
    def create(self, request, *args, **kwargs):
        flashcard_set = get_object_or_404(FlashcardSet, id=request.data.get("flashcard_set"))
        flashcard_collection = flashcard_set.flashcard_collection
        if ((request.user != flashcard_collection.user) and not flashcard_collection.public):
            return HttpResponseForbidden("You are trying to add a review to a private set that you do not own.")
        
        x = Review.objects.filter(
            user=self.request.user, 
            flashcard_set__id=flashcard_set.id).first()
        if x is not None:
            return HttpResponseForbidden("You have already created a review for this set.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseForbidden("You do not have permission to modify this review.")
        else:
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user != self.get_object().user:
            return HttpResponseForbidden("You do not have permission to delete this set.")
        else:
            return super().destroy(request, *args, **kwargs)

# Get API doesn't need a modelviewset
class APIVersionView(APIView):
    def get(self, request):
        # Return the API version
        return Response({"version": API_VERSION})
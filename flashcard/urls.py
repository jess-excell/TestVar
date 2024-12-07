from django.urls import path
from .views import *
from flashcard import views

urlpatterns = [
    # Collections
    path('collections', FlashcardCollectionListView.as_view(), name="collection-list"),
    path('collections/create', FlashcardCollectionCreateView.as_view(), name="collection-create"),
    path('collections/<int:collection_id>/delete', FlashcardCollectionDeleteView.as_view(), name="collection-delete"),
    path('collections/<int:collection_id>/update', FlashcardCollectionUpdateView.as_view(), name="collection-update"),
    
    # Sets
    path("collections/<int:collection_id>", FlashcardSetListView.as_view(), name="set-list"),
    path('collections/<int:collection_id>/create', views.FlashcardSetCreateView.as_view(), name="set-create"),
    path('collections/<int:collection_id>/<int:set_id>/delete', FlashcardSetDeleteView.as_view(), name="set-delete"),
    path('collections/<int:collection_id>/<int:set_id>/update', FlashcardSetUpdateView.as_view(), name="set-update"),
    
    # Sets - comments
    path('collections/<int:collection_id>/<int:set_id>/comments', CommentListView.
    as_view(), name="comments-list"),
    path('collections/<int:collection_id>/<int:set_id>/comments/create', CommentCreateView.as_view(), name="comments-create"),
    
    # Sets - reviews
    path('collections/<int:collection_id>/<int:set_id>/reviews', ReviewListView.
    as_view(), name="review-list"),
    path('collections/<int:collection_id>/<int:set_id>/reviews/create', ReviewCreateView.as_view(), name="review-create"),
    path('collections/<int:collection_id>/<int:set_id>/reviews/<int:review_id>/update', ReviewUpdateView.as_view(), name="review-update"),
    path('collections/<int:collection_id>/<int:set_id>/reviews/<int:review_id>/delete', ReviewDeleteView.as_view(), name="review-delete"),
    
    # Flashcards
    path('collections/<int:collection_id>/<int:set_id>', FlashcardListView.as_view(), name="flashcard-list"),
    path('collections/<int:collection_id>/<int:set_id>/<int:flashcard_id>', FlashcardDetailView.as_view(), name="flashcard-detail"),
    path('collections/<int:collection_id>/<int:set_id>/create', views.FlashcardCreateView.as_view(), name="flashcard-create"),
    path('collections/<int:collection_id>/<int:set_id>/<int:flashcard_id>/delete', FlashCardDeleteView.as_view(), name="flashcard-delete"),
    path('collections/<int:collection_id>/<int:set_id>/<int:flashcard_id>/update', FlashCardUpdateView.as_view(), name="flashcard-update"),
]
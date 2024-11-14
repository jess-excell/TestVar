from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # Collections
    path('collections', FlashcardCollectionListView.as_view(), name="collection-list"),
    path('collections/create', FlashcardCollectionCreateView.as_view(), name="collection-create"),
    
    # Sets
    path("collections/<int:collection_id>", FlashcardSetListView.as_view(), name="set-list"),
    path('collections/<int:collection_id>/create', views.FlashcardSetCreateView.as_view(), name="set-create"),
    
    # Flashcards
    path('collections/<int:collection_id>/<int:set_id>', FlashcardListView.as_view(), name="flashcard-list"),
    path('collections/<int:collection_id>/<int:set_id>/<int:flashcard_id>', FlashcardDetailView.as_view(), name="flashcard-detail"),
    path('collections/<int:collection_id>/<int:set_id>/create', views.FlashcardCreateView.as_view(), name="flashcard-create"),
]
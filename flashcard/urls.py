from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # Add paths here
    path('', FlashcardListView.as_view(), name="flashcard-list"),
    path('<int:pk>', FlashcardDetailView.as_view(), name="flashcard-detail"),
]
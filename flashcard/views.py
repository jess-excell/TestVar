from django.views.generic import TemplateView, ListView, DetailView
from .models import FlashCard
from django.shortcuts import render

# Create your views here.
class FlashcardListView(ListView):
    model = FlashCard
    context_object_name = "flashcards"
    template_name="flashcard/flashcard_list.html"
    
class FlashcardDetailView(DetailView):
    model = FlashCard
    context_object_name = "flashcard"
    template_name = "flashcard/flashcard_info.html"

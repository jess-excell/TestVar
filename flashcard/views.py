from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import FlashCard, FlashcardSet, FlashcardCollection
from django.urls import reverse_lazy

# Collection views
class FlashcardCollectionListView(ListView):
    model = FlashcardCollection
    context_object_name = "collections"
    template_name="flashcard/flashcard_collection_list.html"

class FlashcardCollectionUpdateView(UpdateView):
    model = FlashcardCollection
    fields = ['title', 'description']
    template_name = "flashcard/flashcard_collection_update.html"
    
class FlashcardCollectionCreateView(CreateView):
    model=FlashcardCollection
    fields=['user', 'title', 'description']
    success_url="/flashcard/collections"
    template_name="flashcard/flashcard_collection_create.html"
    
# class FlashcardCollectionDetailView(DetailView):
#     model = FlashcardCollection
#     context_object_name = "collection"
#     template_name = "flashcard/flashcard_collection_info.html"

# Set views
class FlashcardSetListView(ListView):
    model = FlashcardSet
    context_object_name = "sets"
    template_name="flashcard/flashcard_set_list.html"
    
    def get_queryset(self):
        return FlashcardSet.objects.filter(flashcard_collection_id=self.kwargs.get('collection_id'))

class FlashcardSetCreateView(CreateView):
    model = FlashcardSet
    fields = ['title', 'description']
    template_name="flashcard/flashcard_set_create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs['collection_id']
        return context
    
    def form_valid(self, form):
        collection = FlashcardCollection.objects.get(pk=self.kwargs["collection_id"])
        form.instance.flashcard_collection = collection
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('set-list', kwargs={'pk': self.kwargs['collection_id']})

# class FlashcardSetDetailView(DetailView):
#     model = FlashcardSet
#     context_object_name = "set"
#     template_name="flashcard/flashcard_set_info.html"

# Flashcard views
class FlashcardListView(ListView):
    model = FlashCard
    context_object_name = "flashcards"
    template_name="flashcard/flashcard_list.html"
    
    def get_queryset(self):
        collection_id = self.kwargs.get('collection_id')
        set_id = self.kwargs.get('set_id')
    
class FlashcardDetailView(DetailView):
    model = FlashCard
    context_object_name = "flashcard"
    template_name = "flashcard/flashcard_info.html"

class FlashcardCreateView(CreateView):
    model = FlashCard
    fields = ['question', 'answer', 'difficulty']
    success_url = ''
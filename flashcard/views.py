from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import FlashCard, FlashcardSet, FlashcardCollection
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import Http404

# Collection views
class FlashcardCollectionListView(ListView):
    model = FlashcardCollection
    context_object_name = "collections"
    template_name="flashcard/flashcard_collection_list.html"
    
    # Only get public flashcards and user's private flashcards
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FlashcardCollection.objects.filter(Q(public=True) | Q(user=self.request.user))
        else:
            return FlashcardCollection.objects.filter(public=True)

class FlashcardCollectionUpdateView(UpdateView):
    model = FlashcardCollection
    fields = ['title', 'description']
    template_name = "flashcard/flashcard_collection_update.html"

class FlashcardCollectionCreateView(LoginRequiredMixin, CreateView):
    model=FlashcardCollection
    fields=['title', 'description', 'public']
    template_name="flashcard/flashcard_collection_create.html"
    login_url="/login"
    success_url='/'
    
    # Add user to collection info
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# Set views
class FlashcardSetListView(ListView):
    model = FlashcardSet
    context_object_name = "sets"
    template_name="flashcard/flashcard_set_list.html"
    
    def get_queryset(self):
        return FlashcardSet.objects.filter(flashcard_collection_id=self.kwargs.get('collection_id'))

    # Get flashcard collection info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        if context['flashcard_collection'].user != self.request.user and context['flashcard_collection'].public != True:
            raise Http404("You do not have permission to view this collection.")

        return context

class FlashcardSetCreateView(LoginRequiredMixin, CreateView):
    model = FlashcardSet
    fields = ['title', 'description']
    template_name="flashcard/flashcard_set_create.html"
    login_url="/login"
    success_url="/"

    # Get just flashcard collection id
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs['collection_id']
        return context
    
    def form_valid(self, form):
        collection = FlashcardCollection.objects.get(pk=self.kwargs["collection_id"])
        form.instance.flashcard_collection = collection
        return super().form_valid(form)

# Flashcard views
class FlashcardListView(ListView):
    model = FlashCard
    context_object_name = "flashcards"
    template_name="flashcard/flashcard_list.html"
    
    def get_queryset(self):
        return FlashCard.objects.filter(
            flashcard_set__flashcard_collection_id=self.kwargs.get('collection_id'), flashcard_set_id=self.kwargs.get('set_id'))

    # Get flashcard collection info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        set_id = self.kwargs.get('set_id')
        
        context['collection_id'] = collection_id
        context['set_id'] = set_id
        collection = get_object_or_404(FlashcardCollection, id=collection_id)
        
        if collection.user != self.request.user and not collection.public:
            raise Http404("You do not have permission to view this collection.")
        
        context['flashcard_set'] = get_object_or_404(FlashcardSet, id=set_id)
        return context

class FlashcardDetailView(DetailView):
    model = FlashCard
    context_object_name = "flashcard"
    template_name = "flashcard/flashcard_info.html"
    pk_url_kwarg = 'flashcard_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs.get('collection_id')
        context['set_id'] = self.kwargs.get('set_id')
        
        collection_id = self.kwargs.get('collection_id')
        collection = get_object_or_404(FlashcardCollection, id=collection_id)

        if not collection.public and collection.user != self.request.user:
            raise Http404("You do not have permission to view this collection.")
        
        return context


class FlashcardCreateView(LoginRequiredMixin, CreateView):
    model = FlashCard
    fields = ['question', 'answer', 'difficulty']
    # template????
    success_url = '/'
    login_url="/login"
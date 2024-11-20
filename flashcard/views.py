from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import FlashCard, FlashcardSet, FlashcardCollection, Comment
from django.urls import reverse
import datetime

#region CreateViews (Create)
class FlashcardCollectionCreateView(LoginRequiredMixin, CreateView):
    model=FlashcardCollection
    fields=['title', 'description', 'public']
    template_name="flashcard/flashcard_collection_create.html"
    login_url="/login"
    
    # Add user to collection info
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("collection-list")
    
class FlashcardSetCreateView(LoginRequiredMixin, CreateView):
    model = FlashcardSet
    fields = ['title', 'description']
    template_name="flashcard/flashcard_set_create.html"
    login_url="/login"

    # Get just flashcard collection id
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs['collection_id']
        return context
    
    def form_valid(self, form):
        collection = FlashcardCollection.objects.get(pk=self.kwargs["collection_id"])
        form.instance.flashcard_collection = collection
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("set-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
        })
    
class FlashcardCreateView(LoginRequiredMixin, CreateView):
    model = FlashCard
    fields = ['question', 'answer', 'difficulty']
    template_name="flashcard/flashcard_create.html"
    login_url="/login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs.get('collection_id')
        context['set_id'] = self.kwargs.get('set_id')
        collection = get_object_or_404(FlashcardCollection, id=context['collection_id'])

        if not collection.public and collection.user != self.request.user:
            raise Http404("You do not have permission to edit this set.")
        
        return context
    
    # Add user to collection info
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.flashcard_set = get_object_or_404(FlashcardSet, id=self.kwargs.get('set_id'))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("flashcard-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get("set_id"),
        })
        
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["comment"]
    template_name="flashcard/comment_create.html"
    login_url="/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs['collection_id']
        context['set_id'] = self.kwargs['set_id']
        collection = get_object_or_404(FlashcardCollection, id=context['collection_id'])
        
        if not collection.public and collection.user != self.request.user:
            raise Http404("You do not have permission to edit this set.")
        return context
    
    def form_valid(self, form):
        form.instance.flashcard_set = FlashcardSet.objects.get(pk=self.kwargs["set_id"])
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("flashcard-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get('set_id')
        })
# endregion

# region ListViews and FlashcardDetailView (Read)
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
        context["flashcard_collection"] = get_object_or_404(FlashcardCollection, id=collection_id)
        
        if context["flashcard_collection"].user != self.request.user and not context["flashcard_collection"].public:
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
        collection = get_object_or_404(FlashcardCollection, id=context['collection_id'])

        if not collection.public and collection.user != self.request.user:
            raise Http404("You do not have permission to view this collection.")
        
        return context
    
class CommentListView(ListView):
    model = Comment
    context_object_name = "comments"
    template_name = "flashcard/comment_list.html"
    
    def get_queryset(self):
        return Comment.objects.filter(flashcard_set_id=self.kwargs.get('set_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs.get('collection_id')
        context['set_id'] = self.kwargs.get('set_id')
        collection = get_object_or_404(FlashcardCollection, id=context['collection_id'])

        if not collection.public and collection.user != self.request.user:
            raise Http404("You do not have permission to view this collection.")
        
        context["flashcard_set"] = get_object_or_404(FlashcardSet, id=context['set_id'])
        
        return context
# endregion

# region UpdateViews (Update)
class FlashcardCollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = FlashcardCollection
    template_name = "flashcard/flashcard_collection_update.html"
    pk_url_kwarg = "collection_id"
    login_url = "/login"
    fields = ["title", "description", "public"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        if context['flashcard_collection'].user != self.request.user:
            raise Http404("You do not have permission to modify this collection.")
        return context
    
    def get_success_url(self):
        return reverse("set-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
        })
    
class FlashcardSetUpdateView(LoginRequiredMixin, UpdateView):
    model = FlashcardSet
    template_name = "flashcard/flashcard_set_update.html"
    pk_url_kwarg = "set_id"
    login_url = "/login"
    fields = ["title", "description"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        set_id = self.kwargs.get('set_id')
        
        context['collection_id'] = collection_id
        context['set_id'] = set_id
        collection = get_object_or_404(FlashcardCollection, id=collection_id)
        
        if collection.user != self.request.user:
            raise Http404("You do not have permission to modify this set.")
        
        context['flashcard_set'] = get_object_or_404(FlashcardSet, id=set_id)
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        return context    
    
    # Add updated date to set info
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.datetime.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("flashcard-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get("set_id"),
        })

class FlashCardUpdateView(LoginRequiredMixin, UpdateView):
    model = FlashCard
    template_name = "flashcard/flashcard_update.html"
    pk_url_kwarg = "flashcard_id"
    login_url = "/login"
    fields = ["question", "answer", "difficulty"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        set_id = self.kwargs.get('set_id')
        flashcard_id = self.kwargs.get('flashcard_id')
        
        context['collection_id'] = collection_id
        context['set_id'] = set_id
        context['flashcard_id'] = flashcard_id
        collection = get_object_or_404(FlashcardCollection, id=collection_id)
        
        if collection.user != self.request.user:
            raise Http404("You do not have permission to modify this set.")
        
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        context['flashcard'] = get_object_or_404(FlashCard, id=flashcard_id)
        return context    
    
    def get_success_url(self):
        return reverse("flashcard-detail", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get("set_id"),
            "flashcard_id": self.kwargs.get("flashcard_id")
        })
# endregion

# region DeleteViews (Delete)
class FlashcardCollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = FlashcardCollection
    template_name = "flashcard/flashcard_collection_delete.html"
    pk_url_kwarg = "collection_id"
    login_url = "/login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        if context['flashcard_collection'].user != self.request.user:
            raise Http404("You do not have permission to modify this collection.")

        return context
    
    def get_success_url(self):
        return reverse("collection-list")

class FlashcardSetDeleteView(LoginRequiredMixin, DeleteView):
    model = FlashcardSet
    template_name = "flashcard/flashcard_set_delete.html"
    pk_url_kwarg = "set_id"
    login_url = "/login"
    
    # Get flashcard collection info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        set_id = self.kwargs.get('set_id')
        
        context['collection_id'] = collection_id
        context['set_id'] = set_id
        collection = get_object_or_404(FlashcardCollection, id=collection_id)
        
        if collection.user != self.request.user and not collection.public:
            raise Http404("You do not have permission to modify this set.")
        
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        context['flashcard_set'] = get_object_or_404(FlashcardSet, id=set_id)
        return context
    
    def get_success_url(self):
        return reverse("set-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
        })
    
class FlashCardDeleteView(LoginRequiredMixin, DeleteView):
    model = FlashCard
    template_name = "flashcard/flashcard_delete.html"
    pk_url_kwarg="flashcard_id"
    login_url = "/login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs.get('collection_id')
        context['set_id'] = self.kwargs.get('set_id')
        context["flashcard_collection"] = get_object_or_404(FlashcardCollection, id=context['collection_id'])

        if context["flashcard_collection"].user != self.request.user:
            raise Http404("You do not have permission to edit this set.")
        
        return context
    
    def get_success_url(self):
        return reverse("flashcard-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get("set_id")
        })
# endregion
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.db.models import Q, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import FlashCard, FlashcardSet, FlashcardCollection, Comment, Review
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
        if FlashcardSet.objects.filter(created_at__date = datetime.datetime.now()).count() > 19:
            raise Http404("The daily limit for flashcards created has been reached. Please remove an existing set created today or try again tomorrow.")
        elif collection.user != self.request.user:
            raise Http404("You do not have permission to edit this set.")
        else:
            self.object = form.save(commit=False)
            self.object.flashcard_collection = collection
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
    
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
        return context
    
    # Add user to collection info
    def form_valid(self, form):
        collection = get_object_or_404(FlashcardCollection, id=self.kwargs.get('collection_id'))
        if collection.user != self.request.user:
            raise Http404("You do not have permission to edit this set.")
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
        self.object = form.save(commit=False)
        self.object.flashcard_set = FlashcardSet.objects.get(pk=self.kwargs["set_id"])
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("comments-list", kwargs={
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
        if self.request.user.is_superuser:
            return FlashcardCollection.objects.all()
        elif self.request.user.is_authenticated:
            return FlashcardCollection.objects.filter(Q(public=True) | Q(user=self.request.user))
        else:
            return FlashcardCollection.objects.filter(public=True)
        
class FlashcardSetListView(ListView):
    model = FlashcardSet
    context_object_name = "sets"
    template_name="flashcard/flashcard_set_list.html"
    
    def get_queryset(self):
        return FlashcardSet.objects.filter(flashcard_collection_id=self.kwargs.get('collection_id')).annotate(avg_rating=Avg("review__rating")).order_by("-avg_rating")

    # Get flashcard collection info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        if context['flashcard_collection'].user != self.request.user and context['flashcard_collection'].public != True and not self.request.user.is_superuser:
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

        
        if context["flashcard_collection"].user != self.request.user and not context["flashcard_collection"].public and not self.request.user.is_superuser:
            raise Http404("You do not have permission to view this collection.")
        
        context['flashcard_set'] = get_object_or_404(FlashcardSet, id=set_id)
        context['avg_rating'] = Review.objects.filter(flashcard_set=context["flashcard_set"]).aggregate(Avg("rating"))["rating__avg"]
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

        if not collection.public and collection.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("You do not have permission to view this collection.")
        context["collection"]=collection
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
        context['flashcard_id'] = self.kwargs.get('flashcard_id')
        context['set_id'] = self.kwargs.get('set_id')
        context['collection_id'] = self.kwargs.get('collection_id')
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=context['collection_id'])
        
        if context["flashcard_collection"].user != self.request.user:
            raise Http404("The flashcard could not be found.")
        
        context['flashcard'] = get_object_or_404(FlashCard, id=context['flashcard_id'])
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
    
    def get_queryset(self):
        collection_id = self.kwargs.get('collection_id')
        collection = get_object_or_404(FlashcardCollection, id=collection_id)
        if collection.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("You do not have permission to modify this collection.")
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        context['flashcard_collection'] = get_object_or_404(FlashcardCollection, id=collection_id)
        return context
    
    def get_success_url(self):
        return reverse("collection-list")

class FlashcardSetDeleteView(LoginRequiredMixin, DeleteView):
    model = FlashcardSet
    template_name = "flashcard/flashcard_set_delete.html"
    pk_url_kwarg = "set_id"
    login_url = "/login"
    
    def get_queryset(self):
        collection = get_object_or_404(FlashcardCollection, id=self.kwargs.get('collection_id'))
        if collection.user != self.request.user and not self.request.user.is_superuser:
            raise Http404()
        return super().get_queryset()
    
    # Get flashcard collection info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection_id = self.kwargs.get('collection_id')
        set_id = self.kwargs.get('set_id')
        context['collection_id'] = collection_id
        context['set_id'] = set_id
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
        return context
    
    def get_queryset(self):
        collection = get_object_or_404(FlashcardCollection, id=self.kwargs.get('collection_id'))
        if collection.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("Not found")
        return super().get_queryset()
    
    def get_success_url(self):
        return reverse("flashcard-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get("set_id")
        })
# endregion

# region Review
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model=Review
    fields=["rating", "comment"]
    template_name="flashcard/review_create.html"
    login_url="/login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs['collection_id']
        context['set_id'] = self.kwargs['set_id']
        
        context["set"] = get_object_or_404(FlashcardSet, id=context["set_id"])
        return context        

    def dispatch(self, request, *args, **kwargs):
        collection_id=self.kwargs.get("collection_id")
        set_id=self.kwargs.get("set_id")
        collection = get_object_or_404(FlashcardCollection, id=collection_id)
        
        if not collection.public and collection.user != self.request.user:
            raise Http404("Could not find set.")

        if self.request.user.is_anonymous:
            return super().dispatch(request, *args, **kwargs)
        
        x = Review.objects.filter(
            user=self.request.user, 
            flashcard_set__id=set_id).first()
        if x is not None:
            return HttpResponseRedirect(reverse("review-update", kwargs={
                "collection_id": collection_id,
                "set_id": set_id,
                "review_id": x.id
            }))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Add check for number rating
        self.object.user = self.request.user
        self.object.flashcard_set = FlashcardSet.objects.get(pk=self.kwargs["set_id"])
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("review-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get('set_id')
        })

class ReviewListView(ListView):
    model=Review
    context_object_name="review"
    template_name="flashcard/review_list.html"
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Review.objects.filter(flashcard_set__id=self.kwargs.get("set_id"))
        else:
            return Review.objects.filter(flashcard_set__id=self.kwargs.get("set_id"), flashcard_set__flashcard_collection__public=True)
    
    def dispatch(self, request, *args, **kwargs):
        collection_id=self.kwargs.get("collection_id")
        set_id=self.kwargs.get("set_id")
        collection = get_object_or_404(FlashcardCollection, id=collection_id)
        
        if not collection.public and collection.user != self.request.user:
            raise Http404("Could not find set.")
                    
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs.get('collection_id')
        context['set_id'] = self.kwargs.get('set_id')
        context["flashcard_set"] = get_object_or_404(FlashcardSet, id=context['set_id'])
        
        if self.request.user.is_anonymous:
            context["reviewed"] = False
            return context
        
        x = Review.objects.filter(
            user=self.request.user, 
            flashcard_set__id=self.kwargs.get('set_id')).first()
        if x is not None:
            context["reviewed"] = True
            context["review_id"]=x.id
        else:
            context["reviewed"] = False
        return context

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model=Review
    fields=["rating", "comment"]
    template_name="flashcard/review_update.html"
    pk_url_kwarg="review_id"
    login_url="/login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs['collection_id']
        context['set_id'] = self.kwargs['set_id']
        context["set"] = get_object_or_404(FlashcardSet, id=context['set_id'])
        return context
    
    def get_object(self, queryset = None):
        review = super().get_object(queryset)
        collection = get_object_or_404(FlashcardCollection, id=self.kwargs['collection_id'])
        
        if collection.user != self.request.user:
            raise PermissionDenied("You don't have permission to modify this.")
        return review
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("review-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get('set_id')
        })

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model=Review
    template_name="flashcard/review_delete.html"
    pk_url_kwarg="review_id"
    login_url="/login"
    
    def get_object(self, queryset = None):
        review = super().get_object(queryset)
        collection = get_object_or_404(FlashcardCollection, id=self.kwargs['collection_id'])
        
        if collection.user != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You don't have permission to delete this.")
        return review
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_id'] = self.kwargs['collection_id']
        context['set_id'] = self.kwargs['set_id']
        return context
    
    def get_success_url(self):
        return reverse("review-list", kwargs={
            "collection_id": self.kwargs.get('collection_id'),
            "set_id": self.kwargs.get('set_id')
        })
# endregion
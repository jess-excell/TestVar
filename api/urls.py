from django.urls import path, include
from rest_framework import routers
from .views import APIVersionView
from api import views

router = routers.DefaultRouter()
router.register(r'flashcards', views.FlashcardViewSet)
router.register(r'sets', views.FlashcardSetViewSet)
router.register(r'collections', views.FlashcardCollectionViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('version', APIVersionView.as_view(), name='api')
]
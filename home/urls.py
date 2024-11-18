from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', LoginInterfaceView.as_view(), name='login'),
    path('logout', LogoutInterfaceView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('creation-success', CreationSuccessView.as_view(), name='creation-success'),
]
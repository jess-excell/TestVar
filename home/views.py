from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse

# Create your views here.
class LoginInterfaceView(LoginView):
    template_name="home/login.html"

class LogoutInterfaceView(LogoutView):
    template_name="home/logout.html"
    
class RegisterView(CreateView):
    form_class=UserCreationForm
    template_name="home/register.html"
    def get_success_url(self):
        return reverse("creation-success")  

class CreationSuccessView(TemplateView):
    template_name='home/creation-success.html'

class HomeView(TemplateView):
    template_name='home/hello-world.html'
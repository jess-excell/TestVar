from django.test import TestCase
from django.urls import reverse

class TemplateTests(TestCase):
    def test_homepage_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home/hello-world.html')
        self.assertContains(response, 'TestVar')
        
    def test_login_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'home/login.html')
        self.assertContains(response, 'Log in')
        
    def test_logout_template(self):
        response = self.client.get('/logout')
        self.assertTemplateUsed(response, 'home/logout.html')
        self.assertContains(response, "You've been logged out")
        
    def test_register_template(self):
        response = self.client.get('/register')
        self.assertTemplateUsed(response, 'home/register.html')
        self.assertContains(response, 'Create account')
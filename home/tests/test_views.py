from django.test import TestCase
from django.contrib.auth.models import User

class HomeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password")
    
    def test_home_context_logged_out(self):
        response = self.client.get("/")
        self.assertContains(response, "Log in")
        self.assertNotContains(response, "Log out")
    
    def test_home_context_logged_in(self):
        self.client.login(username="user", password="password")
        response = self.client.get("/")
        self.assertNotContains(response, "Log in")
        self.assertContains(response, "Log out")
        self.assertContains(response, f"Hey there, {self.user}!")
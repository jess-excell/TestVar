from django.test import TestCase

class HomePageTemplateTests(TestCase):
    def test_template_used(self):
        response = self.client.get("")
        self.assertTemplateUsed(response, "home/hello-world.html")
    
    # Checks that the title, subheading, main content and footer are all there
    def test_template_content(self):
        response = self.client.get("")
        self.assertContains(response, "TestVar")
        self.assertContains(response, "Studying - made simple.")
        self.assertContains(response, "TestVar presents a state of the art flashcard learning experience, featuring the ability to share and collaborate with fellow students.")
        self.assertContains(response, "© TestVar (2024). All rights reserved.")

class LoginPageTemplateTests(TestCase):
    def test_template_used(self):
        response = self.client.get("/login")
        self.assertTemplateUsed(response, "home/login.html")
        
    def test_template_content(self):
        response = self.client.get("/login")
        self.assertContains(response, "Log in")
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")
        self.assertContains(response, "Submit")

class LogoutPageTemplateTests(TestCase):
    def test_template_used(self):
        response = self.client.get("/logout")
        self.assertTemplateUsed(response, "home/logout.html")
    
    def test_template_content(self):
        response = self.client.get("/logout")
        self.assertContains(response, "You've been logged out")
        self.assertContains(response, "Back to home")

class RegisterPageTemplateTests(TestCase):
    def test_template_used(self):
        response = self.client.get("/register")
        self.assertTemplateUsed(response, "home/register.html")
        self.assertContains(response, "Create account")
    
    def test_template_content(self):
        response = self.client.get("/register")
        self.assertContains(response, "Create account")
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")
        self.assertContains(response, "Password confirmation:")
        self.assertContains(response, "Submit")
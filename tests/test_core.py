from django.urls import reverse
from django.test import TestCase


"""
    This tests all main parts of the website: the library,
    the blog, the about page, the error pages, etc.
"""
class CoreTestCase(TestCase):
    def test_404(self):
        response = self.client.get('/url_does_not_exists')
        self.assertContains(response, 'Malheureusement, cette page n\'existe pas !')
        self.assertEqual(response.status_code, 200)

    def test_voiture_noire_view(self):
        response = self.client.get(reverse("voiture_noire:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("library:index"))

    def test_library_view(self):
        response = self.client.get(reverse("library:index"))
        self.assertContains(response, 'Petite Voiture Noire')
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, 'My Name, grande autrice')
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, 'Bibliographie')
        self.assertEqual(response.status_code, 200)

    def test_gadget_view(self):
        response = self.client.get(reverse("gadgets:index"))
        self.assertContains(response, 'Coquecigrues : trucs, gadgets et machins')
        self.assertEqual(response.status_code, 200)
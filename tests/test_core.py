from django.urls import reverse
from django.test import TestCase

from accounts.models import Member


class CoreTestCase(TestCase):
    def setUp(self):
        Member.objects.create_user("Jean-Bob", email="jeanbobdupont@mail.fr", password="motdepasse")

    def test_page_does_not_exist(self):
        response = self.client.get('/url_does_not_exists')
        self.assertContains(response, 'Malheureusement, cette page n\'existe pas !')
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, 'Autrice M/M | Romans BL et fantasy')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, 'Bibliographie')
        self.assertEqual(response.status_code, 200)

    def test_gadget_view(self):
        response = self.client.get(reverse("gadgets:index"))
        self.assertContains(response, 'Coquecigrues : trucs, gadgets et machins')
        self.assertEqual(response.status_code, 200)

    def test_library_view(self):
        response = self.client.get(reverse("voiture_noire:index"))
        self.assertContains(response, 'Une Petite Voiture Noire')
        self.assertEqual(response.status_code, 200)

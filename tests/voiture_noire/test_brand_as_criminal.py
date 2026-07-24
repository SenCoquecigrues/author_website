from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author

class BrandAsCrminalTestCase(TestCase):
    def setUp(self):
        author = Member.objects.create_user('User Author', password='pass')
        Author.objects.create(member=author, nickname=author.username)
        Member.objects.create_user('Random User', password='pass')

    def test_unlogged(self):
        response = self.client.get(
            reverse("voiture_noire:brand_as_criminal", kwargs={'author_id':1})
        )
        self.assertEqual(response.status_code, 302)
        author = Author.objects.get(pk=1)
        self.assertEqual(author.criminal, False)

    def test_logged_but_is_not_target(self):
        test_client = Client()
        test_client.login(username='Random User', password='pass')
        response = test_client.get(
            reverse("voiture_noire:brand_as_criminal", kwargs={'author_id':1})
        )
        self.assertEqual(response.status_code, 403)
        author = Author.objects.get(pk=1)
        self.assertEqual(author.criminal, False)

    def test_logged_and_is_target(self):
        test_client = Client()
        test_client.login(username='User Author', password='pass')
        response = test_client.get(
            reverse("voiture_noire:brand_as_criminal", kwargs={'author_id':1})
        )
        self.assertEqual(response.status_code, 200)
        author = Author.objects.get(pk=1)
        self.assertEqual(author.criminal, True)

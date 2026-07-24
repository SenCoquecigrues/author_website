from django.http import Http404

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author

class OtherMemberProfileTestCase(TestCase):
    def setUp(self):
        author = Member.objects.create_user('User Author', password='pass')
        Author.objects.create(member=author, nickname=author.username)
        Member.objects.create_user('Random User', password='pass')
        Member.objects.create_user('Discord User', password='pass', discord_id="dkjs")

    def test_unlogged(self):
        response = self.client.get(
            reverse("voiture_noire:member_profile", kwargs={'member_id':1})
        )
        self.assertEqual(response.status_code, 302)

    def test_logged_but_is_not_discord_user(self):
        test_client = Client()
        test_client.login(username='Random User', password='pass')
        response = test_client.get(
            reverse("voiture_noire:member_profile", kwargs={'member_id':1})
        )
        self.assertEqual(response.status_code, 403)

    def test_logged_is_discord_user(self):
        test_client = Client()
        test_client.login(username='Discord User', password='pass')
        response = test_client.get(
            reverse("voiture_noire:member_profile", kwargs={'member_id':1})
        )
        self.assertEqual(response.status_code, 200)

    def test_member_does_not_exists(self):
        test_client = Client()
        test_client.login(username='Discord User', password='pass')
        test_client.get(
            reverse("voiture_noire:member_profile", kwargs={'member_id':4})
        )
        self.assertRaises(Http404)

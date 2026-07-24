from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author
from voiture_noire.models import ExchangeParticipant


class ProfileTestCase(TestCase):
    def setUp(self):
        Member.objects.create_user('noDiscordnoExchange', password='pass')
        is_author = Member.objects.create_user('isAuthor', password='pass')
        is_exchange_participant = Member.objects.create_user(
            'exchangeParticipantNoDiscord', password='pass'
        )
        Member.objects.create_user(
            'hasDiscordNoExchange', email='sara@mail.fr', password='pass', discord_id='discord_id'
        )
        ExchangeParticipant.objects.create(member=is_exchange_participant)
        Author.objects.create(member=is_author, nickname=is_author.username)

    def test_access_unlogged(self):
        response = self.client.get(reverse("voiture_noire:profile"))
        self.assertEqual(response.status_code, 302)

    def test_no_discord_no_exchange(self):
        test_client = Client()
        test_client.login(username='noDiscordnoExchange', password='pass')
        response = test_client.get(reverse('voiture_noire:profile'))

        self.assertNotContains(response, "Profil d'échange")
        self.assertNotContains(response, "Profil d'auteur/d'autrice")
        self.assertNotContains(response, "Votre anniversaire")
        self.assertContains(response, "Paramètres du site")
        self.assertEqual(response.status_code, 200)

    def test_has_discord_ids(self):
        test_client = Client()
        test_client.login(username='hasDiscordNoExchange', password='pass')
        response = test_client.get(reverse('voiture_noire:profile'))

        self.assertNotContains(response, "Profil d'échange")
        self.assertNotContains(response, "Profil d'auteur/d'autrice")
        self.assertContains(response, "Paramètres du site")
        self.assertContains(response, "Votre anniversaire")
        self.assertEqual(response.status_code, 200)

    def test_is_exchange_participant(self):
        test_client = Client()
        test_client.login(
            username='exchangeParticipantNoDiscord', password='pass'
        )
        response = test_client.get(reverse('voiture_noire:profile'))

        self.assertNotContains(response, "Profil d'auteur/d'autrice")
        self.assertNotContains(response, "Votre anniversaire")
        self.assertContains(response, "Profil d'échange")
        self.assertContains(response, "Paramètres du site")
        self.assertEqual(response.status_code, 200)

    def test_is_author(self):
        test_client = Client()
        test_client.login(
            username='isAuthor', password='pass'
        )
        response = test_client.get(reverse('voiture_noire:profile'))

        self.assertNotContains(response, "Votre anniversaire")
        self.assertNotContains(response, "Profil d'échange")
        self.assertContains(response, "Profil d'autrice/d'auteur")
        self.assertContains(response, "Paramètres du site")
        self.assertEqual(response.status_code, 200)

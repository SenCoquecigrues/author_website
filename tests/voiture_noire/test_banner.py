from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member  
from voiture_noire.models import ExchangeParticipant


class BannerTestCase(TestCase):
    def setUp(self):
        Member.objects.create_user('noDiscordnoExchange', email='lucie@mail.fr', password='pass')
        is_exchange_participant = Member.objects.create_user(
            'exchangeParticipantNoDiscord', email='faris@mail.fr', password='pass'
        )
        Member.objects.create_user(
            'hasDiscordNoExchange', email='sara@mail.fr', password='pass', discord_id='discord_id'
        )
        ExchangeParticipant.objects.create(member=is_exchange_participant)

    def test_banner_not_logged_in(self):
        response = self.client.get(reverse('voiture_noire:index'), follow=True)

        self.assertContains(response, 'Se connecter</a></li>')
        self.assertNotContains(response, 'Bibliothèque</a></li>')
        self.assertNotContains(response, 'Thèmes</a></li>')
        self.assertNotContains(response, 'Membres</a></li>')
        self.assertNotContains(response, 'Paramètres</a></li>')
        self.assertEqual(response.status_code, 200)

    def test_banner_no_discord_no_exchange(self):
        # Can't see exchange-specific pages. Accesses Bibliothèque.
        test_client = Client()
        test_client.login(username='noDiscordnoExchange', password='pass')
        response = test_client.get(reverse('voiture_noire:index'), follow=True)

        self.assertContains(response, 'Se déconnecter</button>')
        self.assertContains(response, 'Bibliothèque</a></li>')
        self.assertNotContains(response, 'Thèmes</a></li>')
        self.assertNotContains(response, 'Membres</a></li>')
        self.assertContains(response, 'Paramètres</a></li>')
        self.assertEqual(response.status_code, 200)

    def test_banner_has_discord_ids(self):
        test_client = Client()
        test_client.login(username='hasDiscordNoExchange', password='pass')
        response = test_client.get(reverse('voiture_noire:index'), follow=True)

        self.assertContains(response, 'Se déconnecter</button>')
        self.assertContains(response, 'Bibliothèque</a></li>')
        self.assertContains(response, 'Paramètres</a></li>')
        self.assertContains(response, 'Membres</a></li>')

        self.assertNotContains(response, 'Thèmes</a></li>')

        self.assertEqual(response.status_code, 200)

    def test_banner_is_exchange_participant(self):
        test_client = Client()
        test_client.login(
            username='exchangeParticipantNoDiscord', password='pass'
        )
        response = test_client.get(reverse('voiture_noire:index'), follow=True)

        self.assertContains(response, 'Se déconnecter</button>')
        self.assertContains(response, 'Bibliothèque</a></li>')
        self.assertContains(response, 'Thèmes</a></li>')
        self.assertContains(response, 'Paramètres</a></li>')

        self.assertNotContains(response, 'Membres</a></li>')

        self.assertEqual(response.status_code, 200)
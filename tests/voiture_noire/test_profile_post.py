from django.test import TestCase

from accounts.models import Member
from archives.models import Author
from voiture_noire.models import ExchangeParticipant


class ProfilePostTestCase(TestCase):
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

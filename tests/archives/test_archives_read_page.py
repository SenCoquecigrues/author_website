from datetime import date, timedelta

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author, PairingType, Story

class ArchivesReadPageTestCase(TestCase):
    def setUp(self):
        PairingType.objects.create(pairing_type="oth", label="Autre")
        PairingType.objects.create(pairing_type="het", label="Hétéro")
        PairingType.objects.create(pairing_type="mm", label="M/M")
        PairingType.objects.create(pairing_type="ff", label="F/F")
        PairingType.objects.create(pairing_type="gen", label="Aucun")

        Member.objects.create_user(
            'Author1', email='author1@mail.fr', password='pass'
        )
        Member.objects.create_user(
            'Author2', email='author2@mail.fr', password='pass'
        )
        Author.objects.create(
            member=Member.objects.get(username="Author1"),
            nickname="Author1"
        )
        Author.objects.create(
            member=Member.objects.get(username="Author2"),
            nickname="Author2"
        )

        tomorrow = date.today() + timedelta(days=1)

        story1 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Visible By All Title", summary="Visible by all summary",
            rating="g", visibility="Everyone"
        )
        story1.pairing_type.set(PairingType.objects.filter(label="M/M"))

        story2 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Member Only Title", summary="Member Only Summary",
            rating="g", visibility="Member only"
        )
        story2.pairing_type.set(PairingType.objects.filter(label="F/F"))
        story2.pairing_type.set(PairingType.objects.filter(label="M/M"))

        story3 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Private", summary="Private",
            rating="g", visibility="Private"
        )
        story3.pairing_type.set(PairingType.objects.filter(label="Hétéro"))

        story4 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=tomorrow,
            story_title="Future Title Author 2", summary="Future Summary",
            rating="g", visibility="Everyone"
        )
        story4.pairing_type.set(PairingType.objects.filter(label="Autre"))

        story5 = Story.objects.create(
            author=Author.objects.get(nickname="Author1"), story_date=tomorrow,
            story_title="Future Title Author 1", summary="Future Summary",
            rating="g", visibility="Everyone"
        )
        story5.pairing_type.set(PairingType.objects.filter(label="Aucun"))

    def test_voiture_noire_unlogged_user_can_only_see_fic_visible_for_everyone(self):
        # Story visible by everyone
        response = self.client.get(reverse("archives:read_story", kwargs={'story_id':1, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)

        # Story member_only
        response = self.client.get(reverse("archives:read_story", kwargs={'story_id':2, 'chapter_number': 1}))
        self.assertRedirects(response, reverse("archives:index"))

        # Story is private
        response = self.client.get(reverse("archives:read_story", kwargs={'story_id':1, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 302)

    def test_voiture_noire_logged_user_behaviour(self):
        test_client = Client()
        test_client.login(username="Mr NoAccounts", password="motdepasse")
        # Non-visible, non-visible by outsider story
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':31, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 302)
        # Visible, non-visible by outsider story
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':30, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)
        # Visible by everyone story
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':2, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)

    def test_voiture_noire_author_can_see_non_visible_fic(self):
        test_client = Client()
        test_client.login(username="MrsDiscordMemberAndAuthor", password="hypatia")
        # Non-visible, non-visible by outsider story
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':31, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)
        # Visible, non-visible by outsider story
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':30, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)
        # Visible by everyone story
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':2, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)


from datetime import date, timedelta

from django.http import Http404
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author, Chapter, PairingType, Story

class StoryAccessTestCase(TestCase):
    """
        This tests access to a story page specifically.
        The focus is solely on permissions working right.
    """
    def setUp(self):
        PairingType.objects.create(pairing_type="oth", label="Autre")
        PairingType.objects.create(pairing_type="het", label="Hétéro")
        PairingType.objects.create(pairing_type="mm", label="M/M")
        PairingType.objects.create(pairing_type="ff", label="F/F")
        PairingType.objects.create(pairing_type="gen", label="Aucun")

        Member.objects.create_user(
            'Author1', password='pass'
        )
        Member.objects.create_user(
            'Author2', password='pass'
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
            story_title="Visible Everyone", summary="Visible Everyone summary",
            rating="g", visibility="Everyone"
        )
        story1.pairing_type.set(PairingType.objects.filter(label="M/M"))
        Chapter.objects.create(story=story1, content="Test Content Story 1", number=1)

        story2 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Member Only Title", summary="Member Only Summary",
            rating="g", visibility="Member only"
        )
        story2.pairing_type.set(PairingType.objects.filter(label="F/F"))
        story2.pairing_type.set(PairingType.objects.filter(label="M/M"))
        Chapter.objects.create(story=story2, content="Test Content Story 2", number=1)

        story3 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Private", summary="Private",
            rating="g", visibility="Private"
        )
        story3.pairing_type.set(PairingType.objects.filter(label="Hétéro"))
        Chapter.objects.create(story=story3, content="Test Content Story 3", number=1)

        story4 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=tomorrow,
            story_title="Future Title Author 2", summary="Future Summary",
            rating="g", visibility="Everyone"
        )
        story4.pairing_type.set(PairingType.objects.filter(label="Autre"))
        Chapter.objects.create(story=story4, content="Test Content Story 4", number=1)

        story5 = Story.objects.create(
            author=Author.objects.get(nickname="Author1"), story_date=tomorrow,
            story_title="Future Title Author 1", summary="Future Summary",
            rating="g", visibility="Everyone"
        )
        story5.pairing_type.set(PairingType.objects.filter(label="Aucun"))
        Chapter.objects.create(story=story5, content="Test Content Story 5", number=1)


    """
        ANON USERS
        Can only access stories visible by everyone, if the date is not set in the future.
    """
    def test_anon_access_visibility_everyone(self):
        response = self.client.get(reverse("archives:read_story", kwargs={'story_id':1, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Content Story 1")

        # Story set in the future = 404 error
        response = self.client.get(reverse("archives:read_story", kwargs={'story_id':4, 'chapter_number': 1}))
        self.assertRaises(Http404)

    def test_anon_access_visibility_member(self):
        response = self.client.get(
            reverse("archives:read_story", kwargs={'story_id':2, 'chapter_number': 1})
        )
        self.assertRedirects(response, reverse("library:index"))

    def test_anon_access_visibility_private(self):
        response = self.client.get(reverse("archives:read_story", kwargs={'story_id':3, 'chapter_number': 1}))
        self.assertRedirects(response, reverse("library:index"))

    """
        MEMBERS
        Can access stories visible by everyone IF the date is not set in the future.
        Can access stories visible by members IF the date is not set in the future.
        Can access private stories IF they are the author.
        Can access stories set in the future IF they are the author.
    """
    def test_member_access_visibility_everyone(self):
        test_client = Client()
        test_client.login(username="Author1", password="pass")
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':1, 'chapter_number': 1}))
        self.assertContains(response, "Test Content Story 1")
        self.assertEqual(response.status_code, 200)

        # Story set in the future = redirect
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':4, 'chapter_number': 1}))
        self.assertRedirects(response, reverse("library:index"))

        # Unless user wrote it!
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':5, 'chapter_number': 1}))
        self.assertContains(response, "Test Content Story 5")
        self.assertEqual(response.status_code, 200)

    def test_member_access_visibility_member(self):
        test_client = Client()
        test_client.login(username="Author1", password="pass")

        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':2, 'chapter_number': 1}))
        self.assertEqual(response.status_code, 200)

    def test_member_access_visibility_private(self):
        # Cannot access private story
        test_client = Client()
        test_client.login(username="Author1", password="pass")
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':3, 'chapter_number': 1}))
        self.assertRedirects(response, reverse("library:index"))

        # Unless user is the author
        test_client = Client()
        test_client.login(username="Author2", password="pass")
        response = test_client.get(reverse("archives:read_story", kwargs={'story_id':3, 'chapter_number': 1}))
        self.assertContains(response, "Test Content Story 3")
        self.assertEqual(response.status_code, 200)
        


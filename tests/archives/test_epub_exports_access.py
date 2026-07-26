

from datetime import date, timedelta

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author, Chapter, PairingType, Story


class EpubExportsAccessTestCase(TestCase):
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
            rating="g", visibility="Everyone", story_author_note="An author note"
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

    """
        TEST ACCESS
        Not very in-depth, because it's the same system used to get stories.
    """
    def test_export_access_everyone(self):
        response = self.client.get(
            reverse("archives:export_epub", kwargs={'story_id':1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/epub+zip")

    def test_export_access_member_only(self):
        # As anon
        response = self.client.get(
            reverse("archives:export_epub", kwargs={'story_id':2})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/plain")

        # As member
        test_client = Client()
        test_client.login(username="Author1", password="pass")

        response = test_client.get(
            reverse("archives:export_epub", kwargs={'story_id':2})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/epub+zip")

    def test_export_access_private(self):
        # As anon
        response = self.client.get(
            reverse("archives:export_epub", kwargs={'story_id':3})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/plain")

        # As member
        test_client = Client()
        test_client.login(username="Author1", password="pass")

        response = test_client.get(
            reverse("archives:export_epub", kwargs={'story_id':3})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/plain")

        # As author
        test_client = Client()
        test_client.login(username="Author2", password="pass")

        response = test_client.get(
            reverse("archives:export_epub", kwargs={'story_id':3})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/epub+zip")

    def test_export_access_future(self):
        # As anon
        response = self.client.get(
            reverse("archives:export_epub", kwargs={'story_id':4})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/plain")

        # As member
        test_client = Client()
        test_client.login(username="Author1", password="pass")

        response = test_client.get(
            reverse("archives:export_epub", kwargs={'story_id':4})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/plain")

        # As author
        test_client = Client()
        test_client.login(username="Author2", password="pass")

        response = test_client.get(
            reverse("archives:export_epub", kwargs={'story_id':4})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/epub+zip")

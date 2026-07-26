from datetime import date, timedelta

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author, Chapter, PairingType, Story

class ChapterTestCase(TestCase):
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
        PUBLISHING
    """
        #TODO

    """
        EDITING
    """
        #TODO

    """
        DELETING
    """
    def test_anon_delete_chapter(self):
        response = self.client.get(
            reverse("archives:chapter_delete", kwargs={'chapter_id':1}), follow=True
        )
        self.assertEqual(Chapter.objects.count(), 5)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Page de connexion')


    def test_not_author_delete_chapter(self):
        test_client = Client()
        test_client.login(username="Author1", password="pass")

        response = test_client.get(reverse("archives:chapter_delete", kwargs={'chapter_id':2}))
        self.assertEqual(Chapter.objects.count(), 5)
        self.assertEqual(response.status_code, 403)

    def test_author_delete_chapter(self):
        test_client = Client()
        test_client.login(username="Author2", password="pass")
        response = test_client.get(
            reverse("archives:chapter_delete", kwargs={'chapter_id':2}),
            follow=True)

        self.assertEqual(Chapter.objects.count(), 4)
        self.assertContains(response, "Votre profil")
        self.assertEqual(response.status_code, 200)
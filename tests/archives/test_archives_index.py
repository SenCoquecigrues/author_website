from datetime import date, timedelta


from django.db.models import Q
from django.test import Client, TestCase
from django.urls import reverse
from accounts.models import Member
from archives.models import Author, PairingType, Story


class ArchivesIndexTestCase(TestCase):
    # Note: will await definitive data structure
    # fixtures = ["accounts.json", "archives.json"]

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


    def test_voiture_noire_index_redirect_properly(self):
        response = self.client.get(reverse("voiture_noire:index"))
        self.assertEqual(response.status_code, 302)

    def test_voiture_noire_index_unlogged(self):
        # Unlogged users only see stories available to everyone.
        # Future stories are not displayed.
        response = self.client.get(reverse("archives:index"))
        fetched_stories = response.context_data['stories']
        visibility_status = {story.visibility for story in fetched_stories}
        expected_stories = Story.objects.filter(
            Q(visibility='Everyone') & (Q(story_date__lte=date.today()))
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Private", visibility_status) 
        self.assertNotIn("Members only", visibility_status) 
        self.assertIn("Everyone", visibility_status)
        self.assertEqual(fetched_stories[0], expected_stories[0])
        self.assertEqual(len(fetched_stories), 1)

    def test_voiture_noire_index_logged(self):
        # Members see all available stories except the others' Private ones.
        # Future stories are not displayed.
        test_client = Client()
        test_client.login(username="Author2", password="pass")

        response = test_client.get(reverse("archives:index"))
        fetched_stories = response.context_data['stories']
        story_titles = {story.story_title for story in fetched_stories}
        user_id = Member.objects.get(username="Author2").id
        count_relevant_stories = Story.objects.filter(
            Q(author__member_id=user_id) | ((~Q(visibility='Private') & Q(story_date__lte=date.today())))
        ).count()

        self.assertEqual(len(fetched_stories), 4)
        self.assertEqual(len(fetched_stories), count_relevant_stories)
        self.assertIn("Private", story_titles)
        self.assertNotIn("Future Title Author 1", story_titles)
        self.assertIn("Future Title Author 2", story_titles)
        self.assertEqual(response.status_code, 200)

    def test_voiture_noire_index_test_filters(self):
        test_client = Client()
        test_client.login(username="Author2", password="pass")

        response = test_client.get(
            reverse("archives:index"), query_params={"filter_ratings": "g", "filter_pairing_types": "1"}
        )
        fetched_stories = response.context_data['stories']
        story_titles = {story.story_title for story in fetched_stories}

        self.assertEqual(len(fetched_stories), 1)
        self.assertIn("Future Title Author 2", story_titles)
        self.assertEqual(fetched_stories[0].pairing_type.all()[0].id, 1)
        self.assertEqual(response.status_code, 200)

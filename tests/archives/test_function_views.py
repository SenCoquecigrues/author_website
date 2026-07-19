import json

from datetime import date


from django.test import Client, TestCase
from django.urls import reverse
from accounts.models import Member
from archives.models import Author, Chapter, PairingType, Reaction, ReactionsRelationships, Story


class FunctionViewsTestCase(TestCase):
    def setUp(self):
        PairingType.objects.create(pairing_type="mm", label="M/M")
        PairingType.objects.create(pairing_type="ff", label="F/F")

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

        Reaction.objects.create(text_emoji="=)", text_legend="A smile")
        story1 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Visible By All Title", summary="Visible by all summary",
            rating="g", visibility="Everyone"
        )
        story1.pairing_type.set(PairingType.objects.filter(label="M/M"))
        Chapter.objects.create(
            story=story1, content="Placeholder content"
        )

        story2 = Story.objects.create(
            author=Author.objects.get(nickname="Author2"), story_date=date.today(),
            story_title="Member Only Title", summary="Member Only Summary",
            rating="g", visibility="Member only"
        )
        story2.pairing_type.set(PairingType.objects.filter(label="F/F"))
        story2.pairing_type.set(PairingType.objects.filter(label="M/M"))

    def test_clap_story(self):
        test_client = Client()
        test_client.login(username="Author1", password="pass")

        response = test_client.get(reverse("archives:clap", kwargs={'story_id':1}))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {"code": 200})

    def test_clap_story_wrong_arg(self):
        test_client = Client()
        test_client.login(username="Author1", password="pass")

        response = test_client.get(reverse("archives:clap", kwargs={'story_id': 999}))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {"code": 500})

    def test_react_to_chapter_user_use_new_reaction(self):
        test_client = Client()
        test_client.login(username="Author2", password="pass")
        json_data = json.dumps({ "reaction_id": 1 })
        response = test_client.post(
            reverse("archives:react_to_chapter", kwargs={'chapter_id': 1}), json_data, content_type="application/json"
        )
        all_reactions = Chapter.objects.get(id=1).chapter_reacted_as.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(all_reactions), 1)
        self.assertEqual(all_reactions[0].reaction.text_emoji, "=)")

    """
        User can use multiple reactions for one chapter
    """
    def test_react_to_chapter_user_use_another_reaction(self):
        test_client = Client()
        test_client.login(username="Author2", password="pass")
        Reaction.objects.create(text_emoji="=(", text_legend="A frown")
        ReactionsRelationships.objects.create(
            member = Member.objects.get(username="Author2"),
            chapter=Chapter.objects.get(id=1),
            reaction=Reaction.objects.get(id=1)
        )

        json_data = json.dumps({ "reaction_id": 2 })
        response = test_client.post(
            reverse("archives:react_to_chapter", kwargs={'chapter_id': 1}), json_data, content_type="application/json"
        )
        all_reactions = Chapter.objects.get(id=1).chapter_reacted_as.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(all_reactions), 2)
        self.assertEqual(all_reactions[0].reaction.text_emoji, "=)")
        self.assertEqual(all_reactions[1].reaction.text_emoji, "=(")

    """
        Posting to view a second time with a reaction already used will remove it. 
    """
    def test_react_to_chapter_reaction_user_never_reacted(self):
        test_client = Client()
        test_client.login(username="Author2", password="pass")
        ReactionsRelationships.objects.create(
            member = Member.objects.get(username="Author2"),
            chapter=Chapter.objects.get(id=1),
            reaction=Reaction.objects.get(id=1)
        )

        json_data = json.dumps({ "reaction_id": 1 })
        response = test_client.post(
            reverse("archives:react_to_chapter", kwargs={'chapter_id': 1}), json_data, content_type="application/json"
        )
        all_reactions = Chapter.objects.get(id=1).chapter_reacted_as.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(all_reactions), 0)

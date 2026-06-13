from datetime import date, timedelta


from django.db.models import Q
from django.test import Client, TestCase
from django.urls import reverse
from accounts.models import Member
from coquecigrues.models import Roleplayer, World


class IndexTestCase(TestCase):
    # Note: will await definitive data structure
    # fixtures = ["accounts.json", "archives.json"]
    def setUp(self):
        babette = Member.objects.create_user(
            'Babette', email='babette@mail.fr', password='pass'
        )
        is_child = Member.objects.create_user(
            'Is Child', email='is_child@mail.fr', password='pass'
        )

        jeanne = Member.objects.create_user(
            'Jeanne', email='jeanne@mail.fr', password='pass'
        )

        Roleplayer.objects.create(member=babette)
        jeanne_player = Roleplayer.objects.create(member=jeanne, is_adult=True)
        is_child_player = Roleplayer.objects.create(member=is_child, is_adult=False)

        World.objects.create(
            visibility="p", open_for_play=True,
            name="Private World", description="Visible by founder only",
            creator=jeanne_player, rating='t')
        World.objects.create(
            visibility="e", open_for_play=True,
            name="Everyone World", description="Visible by all",
            creator=jeanne_player, rating='a')
        World.objects.create(
            visibility="e", open_for_play=True,
            name="Explicit Everyone World", description="Visible by all",
            creator=jeanne_player, rating='e')


    def test_given_unlogged_redirect_properly(self):
        response = self.client.get(reverse("coquecigrues:index"))
        self.assertEqual(response.status_code, 302)

    def test_given_logged_load_page(self):
        test_client = Client()
        test_client.login(username="Babette", password="pass")

        response = test_client.get(reverse("coquecigrues:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Everyone World')
        # TODO: change to not contains
        self.assertContains(response, 'Private World')

    def test_given_underage_do_not_load_adult(self):
        test_client = Client()
        test_client.login(username="Babette", password="pass")

        response = test_client.get(reverse("coquecigrues:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Everyone World')
        # TODO: change to not contains
        self.assertContains(response, 'Private World')


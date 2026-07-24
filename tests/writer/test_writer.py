import datetime
import json

from unittest.mock import patch, mock_open

from django.test import TestCase
from django.urls import reverse

from writer.models import Post


class WriterTestCase(TestCase):
    def test_homepage(self):
        # Set up
        date_today = datetime.date.today()
        tomorrow = date_today + datetime.timedelta(days=1)
        yesterday = date_today - datetime.timedelta(days=1)
        two_days_ago = date_today - datetime.timedelta(days=2)

        Post.objects.create(
            body="Two days ago, this was posted",
            date=two_days_ago
        )
        Post.objects.create(
            body="Yesterday, this was posted",
            date=yesterday
        )
        Post.objects.create(
            title="Title 3",
            body="Today, this was posted",
            post_type="AU",
            date=date_today
        )
        Post.objects.create(
            body="This is dated tomorrow and shouldn't show up.",
            post_type="WR",
            date=tomorrow
        )

        # Test itself
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'Two days ago, this was posted')
        self.assertContains(response, 'Yesterday, this was posted')
        self.assertContains(response, 'Today, this was posted')
        self.assertContains(response, 'Title 3')
        self.assertNotContains(response, "This is dated tomorrow and shouldn't show up.")
        self.assertEqual(response.status_code, 200)

    @patch(
        "writer.views.open",
        side_effect=FileNotFoundError
    )
    def test_about_no_profile_json(self, mock_open):
        response = self.client.get(reverse("about"))
        self.assertContains(response, 'My Name<')
        self.assertContains(response, 'My Name, a Splendid Wordsmith')
        self.assertContains(response, '<p>My Name has had a')
        self.assertContains(response, '<li>Book 1</li>')
        self.assertContains(response, 'Category 2')
        self.assertContains(response, '<li>Book 2</li>')
        self.assertEqual(response.status_code, 200)

    @patch(
        "writer.views.open",
        new_callable=mock_open,
        read_data=json.dumps({
            "author_name": "My Existing Name",
            "author_blurb": "My Existing Name, a Splendid Wordsmith",
            "author_bio": "<p>My Existing Name has had a life.</p>",
            "bibliography": {
                "Existing Category 1": ["Existing Book 1"],
                "Existing Category 2": ["Existing Book 2"],}
        })
    )
    def test_about_with_profile_json(self, mock_open):
        response = self.client.get(reverse("about"))
        self.assertContains(response, 'My Existing Name<')
        self.assertContains(response, 'My Existing Name, a Splendid Wordsmith')
        self.assertContains(response, '<p>My Existing Name has had a')
        self.assertContains(response, '<li>Existing Book 1</li>')
        self.assertContains(response, 'Existing Category 2')
        self.assertContains(response, '<li>Existing Book 2</li>')
        self.assertEqual(response.status_code, 200)

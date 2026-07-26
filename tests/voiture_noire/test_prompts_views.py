from django.http import Http404
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Member
from archives.models import Author
from voiture_noire.models import ExchangeParticipant, Prompt


class PromptsViewsTestCase(TestCase):
    def setUp(self):
        Member.objects.create_user('User', password='pass')
        is_author = Member.objects.create_user('isAuthor', password='pass')
        is_exchange_participant = Member.objects.create_user(
            'exchangeParticipantNoDiscord', password='pass'
        )
        Member.objects.create_user(
            'hasDiscordNoExchange', email='sara@mail.fr', password='pass', discord_id='discord_id'
        )
        ExchangeParticipant.objects.create(member=is_exchange_participant)
        Author.objects.create(member=is_author, nickname=is_author.username)
        Prompt.objects.create(body="A prompt body")

    def test_get_prompts(self):
        prompt_one = Prompt.objects.get(pk=1)
        prompt_two = Prompt.objects.create(body="another prompt")
        prompt_three = Prompt.objects.create(body="another another prompt")

        test_client = Client()
        test_client.login(username='User', password='pass')
        response = test_client.get(
            reverse('voiture_noire:prompts')
        )
        self.assertContains(response, prompt_one.body)
        self.assertContains(response, prompt_two.body)
        self.assertContains(response, prompt_three.body)

    def test_post_prompt(self):
        test_client = Client()
        test_client.login(username='User', password='pass')

        response = test_client.post(
            reverse('voiture_noire:post_prompt'), {'body': 'A test body', 'pairing_type': 'FF'}
        )
        self.assertRedirects(response, reverse("voiture_noire:prompts"))
        prompts = Prompt.objects.all()
        self.assertEqual(len(prompts), 2)
        self.assertEqual(prompts[1].body, 'A test body')
        self.assertEqual(prompts[1].pairing_type, 'FF')

    def test_post_bad_prompt(self):
        test_client = Client()
        test_client.login(username='User', password='pass')

        response = test_client.post(
            reverse('voiture_noire:post_prompt'), {'body': 'A test body'}
        )
        self.assertEqual(response.status_code, 400)
        prompts = Prompt.objects.all()
        self.assertEqual(len(prompts), 1)

    def test_sort_prompts_by_id(self):
        Prompt.objects.get(pk=1)
        Prompt.objects.create(body="another prompt")
        Prompt.objects.create(body="another another prompt")

        test_client = Client()
        test_client.login(username='User', password='pass')

        response = test_client.post(
            reverse('voiture_noire:prompts'), {'sort_value': 'prompt_id'}
        )
        self.assertEqual(response.status_code, 200)

    def test_sort_prompts_by_any_valid_field(self):
        Prompt.objects.get(pk=1)
        Prompt.objects.create(body="another prompt")
        Prompt.objects.create(body="another another prompt")

        test_client = Client()
        test_client.login(username='User', password='pass')

        response = test_client.post(
            reverse('voiture_noire:prompts'), {'sort_value': 'body'}
        )
        self.assertEqual(response.status_code, 200)

    def test_sort_prompts_bad_format(self):
        test_client = Client()
        test_client.login(username='User', password='pass')

        response = test_client.post(
            reverse('voiture_noire:prompts'), {'not_sort_value': 'Ha-HA!'}
        )
        self.assertEqual(response.status_code, 400)

    def test_would_create(self):
        prompt = Prompt.objects.get(pk=1)
        member = Member.objects.get(pk=1)

        test_client = Client()
        test_client.login(username='User', password='pass')

        # Prompt does not exists
        response = test_client.post(
            reverse('voiture_noire:would_create', kwargs={'prompt_id':2})
        )
        self.assertRaises(Http404)

        # Everything ok
        response = test_client.post(
            reverse('voiture_noire:would_create', kwargs={'prompt_id':1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(member, prompt.would_create.all())

        # Process is idempotent
        response = test_client.post(
            reverse('voiture_noire:would_create', kwargs={'prompt_id':1})
        )
        self.assertEqual(len(prompt.would_create.all()), 1)

    def test_would_not_create(self):
        prompt = Prompt.objects.get(pk=1)
        member = Member.objects.get(pk=1)

        test_client = Client()
        test_client.login(username='User', password='pass')

        response = test_client.post(
            reverse('voiture_noire:would_create', kwargs={'prompt_id':1})
        )
        self.assertIn(member, prompt.would_create.all())
        self.assertIn(prompt, member.would_create.all())

        # Prompt does not exists
        response = test_client.post(
            reverse('voiture_noire:would_not_create', kwargs={'prompt_id':2})
        )
        self.assertRaises(Http404)

        # Everything ok
        response = test_client.post(
            reverse('voiture_noire:would_not_create', kwargs={'prompt_id':1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(member, prompt.would_create.all())
        self.assertNotIn(prompt, member.would_create.all())

        # Process is idempotent
        response = test_client.post(
            reverse('voiture_noire:would_not_create', kwargs={'prompt_id':1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(prompt.would_create.all()), 0)

    def test_would_receive(self):
        prompt = Prompt.objects.get(pk=1)
        member = Member.objects.get(pk=1)

        test_client = Client()
        test_client.login(username='User', password='pass')

        # Prompt does not exists
        response = test_client.post(
            reverse('voiture_noire:would_receive', kwargs={'prompt_id':2})
        )
        self.assertRaises(Http404)

        # Everything ok
        response = test_client.post(
            reverse('voiture_noire:would_receive', kwargs={'prompt_id':1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(member, prompt.would_receive.all())
        self.assertIn(prompt, member.would_receive.all())

        # Process is idempotent
        response = test_client.post(
            reverse('voiture_noire:would_receive', kwargs={'prompt_id':1})
        )
        self.assertEqual(len(prompt.would_receive.all()), 1)

    def test_would_not_receive(self):
        prompt = Prompt.objects.get(pk=1)
        member = Member.objects.get(pk=1)

        test_client = Client()
        test_client.login(username='User', password='pass')

        response = test_client.post(
            reverse('voiture_noire:would_receive', kwargs={'prompt_id':1})
        )
        self.assertIn(member, prompt.would_receive.all())
        self.assertIn(prompt, member.would_receive.all())

        # Prompt does not exists
        response = test_client.post(
            reverse('voiture_noire:would_not_receive', kwargs={'prompt_id':2})
        )
        self.assertRaises(Http404)

        # Everything ok
        response = test_client.post(
            reverse('voiture_noire:would_not_receive', kwargs={'prompt_id':1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(member, prompt.would_receive.all())
        self.assertNotIn(prompt, member.would_receive.all())

        # Process is idempotent
        response = test_client.post(
            reverse('voiture_noire:would_not_receive', kwargs={'prompt_id':1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(prompt.would_receive.all()), 0)

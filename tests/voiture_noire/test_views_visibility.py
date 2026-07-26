from django.urls import reverse
from django.test import Client, TestCase
from accounts.models import Member  

"""
    None of these pages should be accessibles for non-members.
    Library access is not tested here, as it actually belong to
    another module.
"""
class ViewsVisibilityTestCase(TestCase):
    def setUp(self):
        Member.objects.create_user(
            "Test Member",
            email="jeanbobdupont@mail.fr",
            password="pass"
        )

    def test_voiture_noire_index(self):
        response = self.client.get(reverse("voiture_noire:index"), follow=True)
        self.assertRedirects(response, reverse("library:index"))
        self.assertEqual(response.status_code, 200)
    
    def test_voiture_noire_members(self):
        response = self.client.get(reverse("voiture_noire:members"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.headers["Location"].startswith(reverse("login"))
        )

        test_client = Client()
        test_client.login(username='Test member', password='pass')
        response = test_client.get(reverse('voiture_noire:members'))
        self.assertContains(response, 'Tout le monde, et le reste')
        self.assertEqual(response.status_code, 200)

    def test_voiture_noire_profile(self):
        response = self.client.get(reverse("voiture_noire:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.headers["Location"].startswith(reverse("login"))
        )

        test_client = Client()
        test_client.login(username='Test member', password='pass')
        response = test_client.get(reverse('voiture_noire:profile'))
        self.assertContains(response, 'Votre profil')
        self.assertEqual(response.status_code, 200)

    def test_voiture_noire_prompts(self):
        response = self.client.get(reverse("voiture_noire:prompts"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.headers["Location"].startswith(reverse("login"))
        )

        test_client = Client()
        test_client.login(username='Test member', password='pass')
        response = test_client.get(reverse('voiture_noire:prompts'))
        self.assertContains(response, 'Proposer un ')
        self.assertEqual(response.status_code, 200)


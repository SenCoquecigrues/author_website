from django.urls import reverse
from django.test import TestCase


"""
    This tests the gadget pages.
    Tests are sparse because the meat of gadget lie
    in its javascript code.
"""
class GadgetsTestCase(TestCase):
    def test_ecritoire(self):
        response = self.client.get(reverse("gadgets:ecritoire"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "critoire")

from django.test import TestCase
from contact.apps import ContactConfig


class ContactTests(TestCase):
    def test_app_name(self):
        app_name = ContactConfig.name
        self.assertEqual(app_name, 'contact')

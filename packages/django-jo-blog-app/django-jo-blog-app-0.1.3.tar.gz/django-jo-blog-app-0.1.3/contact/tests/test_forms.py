# contact/tests.py
from django.test import TestCase
from contact.forms import ContactForm


class ContactTests(TestCase):
    def test_forms_is_valid(self):
        form_data = {'email': 'test@gmail.com', 'message': 'some message'}
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_forms_is_invalid(self):
        form_data = {'email': 'testgmail.com', 'message': 'some message'}
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_send_email(self):
        form_data = {'email': 'test@gmail.com', 'message': 'some message'}
        form = ContactForm(data=form_data)
        self.assertTrue(form.send_email)

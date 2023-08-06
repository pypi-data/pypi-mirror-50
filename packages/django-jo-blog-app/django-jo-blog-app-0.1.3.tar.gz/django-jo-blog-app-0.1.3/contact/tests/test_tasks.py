# from contact.tasks import send_contact_email
# from django.test import TestCase


# class TestAddTask(TestCase):
#     def setUp(self):
#         self.task = send_contact_email.delay(
#             args=['test@gmail.com', 'some message']
#         )
#         self.results = self.task.get()

#     def test_task_state(self):
#         self.assertEqual(self.task.state, 'SUCCESS')

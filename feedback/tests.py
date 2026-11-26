from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from feedback.models import Feedback


class FeedbackTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="feedbackuser", password="Password123!")

    def test_feedback_page_requires_login(self):
        resp = self.client.get(reverse("feedback"))
        self.assertEqual(resp.status_code, 302)

    def test_submit_valid_feedback(self):
        self.client.login(username="feedbackuser", password="Password123!")
        resp = self.client.post(reverse("feedback"), {
            "subject": "Great prediction interface",
            "category": "prediction",
            "rating": 5,
            "message": "The heart disease parameters were very clearly explained and easy to fill out."
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Feedback.objects.filter(user=self.user).exists())
        fb = Feedback.objects.get(user=self.user)
        self.assertEqual(fb.rating, 5)
        self.assertEqual(fb.category, "prediction")

    def test_short_message_validation_error(self):
        self.client.login(username="feedbackuser", password="Password123!")
        resp = self.client.post(reverse("feedback"), {
            "subject": "Hi",
            "category": "general",
            "rating": 4,
            "message": "Too short"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Feedback.objects.filter(user=self.user).exists())

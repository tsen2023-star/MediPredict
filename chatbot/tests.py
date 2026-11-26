import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class ChatbotTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="chatuser", password="Password123!")

    def test_chat_page_requires_login(self):
        resp = self.client.get(reverse("chatbot"))
        self.assertEqual(resp.status_code, 302)

    def test_chatbot_emergency_triage(self):
        self.client.login(username="chatuser", password="Password123!")
        resp = self.client.post(
            reverse("chatbot_api"),
            data=json.dumps({"message": "I am having severe chest pain and cannot breathe"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("EMERGENCY ADVISORY", data["reply"])
        self.assertIn("112", data["reply"])

    def test_chatbot_system_inquiry(self):
        self.client.login(username="chatuser", password="Password123!")
        resp = self.client.post(
            reverse("chatbot_api"),
            data=json.dumps({"message": "What is MediPredict and how do I use it?"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("MediPredict", data["reply"])

    def test_chatbot_invalid_empty_input(self):
        self.client.login(username="chatuser", password="Password123!")
        resp = self.client.post(
            reverse("chatbot_api"),
            data=json.dumps({"message": "   "}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

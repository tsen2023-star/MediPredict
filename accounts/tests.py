from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Profile


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testpatient",
            email="patient@example.com",
            password="StrongPassword123!"
        )
        self.user.first_name = "Jane"
        self.user.last_name = "Doe"
        self.user.save()
        Profile.objects.update_or_create(user=self.user, defaults={"city": "Mumbai", "phone": "9876543210"})

    def test_user_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone": "9999988888",
            "city": "Bengaluru",
            "password1": "SecurePass2026!",
            "password2": "SecurePass2026!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_u = User.objects.get(username="newuser")
        self.assertEqual(new_u.profile.city, "Bengaluru")

    def test_duplicate_email_registration_rejected(self):
        response = self.client.post(reverse("register"), {
            "username": "differentuser",
            "email": "patient@example.com",
            "password1": "SecurePass2026!",
            "password2": "SecurePass2026!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="differentuser").exists())

    def test_login_and_logout(self):
        login_resp = self.client.post(reverse("login"), {
            "username": "testpatient",
            "password": "StrongPassword123!"
        })
        self.assertEqual(login_resp.status_code, 302)
        self.assertRedirects(login_resp, reverse("dashboard"))

        logout_resp = self.client.post(reverse("logout"))
        self.assertEqual(logout_resp.status_code, 302)
        self.assertRedirects(logout_resp, reverse("home"))

    def test_profile_view_and_edit(self):
        self.client.login(username="testpatient", password="StrongPassword123!")
        resp = self.client.get(reverse("profile"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "testpatient")
        self.assertContains(resp, "Mumbai")

        edit_resp = self.client.post(reverse("profile_edit"), {
            "first_name": "Janet",
            "last_name": "Smith",
            "email": "janet@example.com",
            "phone": "1122334455",
            "city": "New Delhi"
        })
        self.assertEqual(edit_resp.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Janet")
        self.assertEqual(self.user.profile.city, "New Delhi")

    def test_password_reset_request(self):
        resp = self.client.post(reverse("password_reset"), {
            "email": "patient@example.com"
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("password_reset_done"))

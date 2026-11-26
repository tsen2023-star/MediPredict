from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from hospitals.models import Hospital


class HospitalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="Password123!")
        self.h1 = Hospital.objects.create(
            name="AIIMS New Delhi",
            address="Ansari Nagar",
            city="New Delhi",
            state="Delhi",
            phone="011-26588500",
            emergency_contact="011-26593677",
            specialties="Cardiology, Nephrology, Oncology"
        )
        self.h2 = Hospital.objects.create(
            name="Apollo Hospital",
            address="Greams Road",
            city="Chennai",
            state="Tamil Nadu",
            phone="044-28290200",
            emergency_contact="1066",
            specialties="Cardiology, Hepatology, Organ Transplant"
        )

    def test_hospital_list_requires_login(self):
        resp = self.client.get(reverse("hospitals"))
        self.assertEqual(resp.status_code, 302)

    def test_hospital_list_authenticated(self):
        self.client.login(username="testuser", password="Password123!")
        resp = self.client.get(reverse("hospitals"))
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.context["total_count"], 2)
        self.assertTrue(len(resp.context["page_obj"]) > 0)

    def test_hospital_search_by_state(self):
        self.client.login(username="testuser", password="Password123!")
        resp = self.client.get(reverse("hospitals"), {"state": "Tamil Nadu"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Apollo Hospital")
        self.assertNotContains(resp, "AIIMS New Delhi")

    def test_hospital_search_by_city(self):
        self.client.login(username="testuser", password="Password123!")
        resp = self.client.get(reverse("hospitals"), {"city": "Chennai"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Apollo Hospital")
        self.assertNotContains(resp, "AIIMS New Delhi")

    def test_hospital_search_by_specialty(self):
        self.client.login(username="testuser", password="Password123!")
        resp = self.client.get(reverse("hospitals"), {"q": "Hepatology"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Apollo Hospital")

    def test_hospital_detail(self):
        self.client.login(username="testuser", password="Password123!")
        resp = self.client.get(reverse("hospital_detail", args=[self.h1.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "AIIMS New Delhi")
        self.assertContains(resp, "011-26588500")

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from prediction.models import PredictionRecord


class PredictionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="patient1", password="Password123!")
        self.user2 = User.objects.create_user(username="patient2", password="Password123!")

    def test_predict_requires_login(self):
        resp = self.client.get(reverse("predict_heart"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("login", resp.url)

    def test_heart_prediction_evaluation(self):
        self.client.login(username="patient1", password="Password123!")
        payload = {
            "age": 58,
            "sex": 1,
            "cp": 0,
            "trestbps": 140,
            "chol": 240,
            "fbs": 0,
            "restecg": 0,
            "thalach": 145,
            "exang": 1,
            "oldpeak": 2.0,
            "slope": 1,
            "ca": 1,
            "thal": 2,
        }
        resp = self.client.post(reverse("predict_heart"), payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Prediction Outcome")
        self.assertTrue(PredictionRecord.objects.filter(user=self.user1, disease="heart").exists())
        record = PredictionRecord.objects.get(user=self.user1, disease="heart")
        self.assertGreater(record.risk_score, 0)
        self.assertIn(record.risk_level, ["Low", "Moderate", "High"])

    def test_diabetes_prediction_evaluation(self):
        self.client.login(username="patient1", password="Password123!")
        payload = {
            "pregnancies": 2,
            "glucose": 145,
            "blood_pressure": 76,
            "skin_thickness": 30,
            "insulin": 120,
            "bmi": 32.5,
            "diabetes_pedigree_function": 0.65,
            "age": 45,
        }
        resp = self.client.post(reverse("predict_diabetes"), payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Prediction Outcome")
        self.assertTrue(PredictionRecord.objects.filter(user=self.user1, disease="diabetes").exists())

    def test_liver_prediction_evaluation(self):
        self.client.login(username="patient1", password="Password123!")
        payload = {
            "age": 50,
            "gender": 1,
            "total_bilirubin": 2.5,
            "direct_bilirubin": 1.1,
            "alkaline_phosphotase": 290,
            "alamine_aminotransferase": 65,
            "aspartate_aminotransferase": 75,
            "total_proteins": 6.2,
            "albumin": 2.8,
            "albumin_and_globulin_ratio": 0.8,
        }
        resp = self.client.post(reverse("predict_liver"), payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Prediction Outcome")
        self.assertTrue(PredictionRecord.objects.filter(user=self.user1, disease="liver").exists())

    def test_kidney_prediction_evaluation(self):
        self.client.login(username="patient1", password="Password123!")
        payload = {
            "age": 55,
            "bp": 80,
            "sg": 1.020,
            "al": 0,
            "su": 0,
            "bgr": 115,
            "bu": 38,
            "sc": 1.1,
            "sod": 140,
            "pot": 4.4,
            "hemo": 14.5,
            "pcv": 44,
            "htn": 0,
        }
        resp = self.client.post(reverse("predict_kidney"), payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Prediction Outcome")
        self.assertTrue(PredictionRecord.objects.filter(user=self.user1, disease="kidney").exists())
        record = PredictionRecord.objects.get(user=self.user1, disease="kidney")
        self.assertIn(record.risk_level, ["Low", "Moderate", "High"])

    def test_breast_cancer_prediction_evaluation(self):
        self.client.login(username="patient1", password="Password123!")
        payload = {
            "radius_mean": 17.99,
            "texture_mean": 10.38,
            "perimeter_mean": 122.8,
            "area_mean": 1001.0,
            "smoothness_mean": 0.1184,
            "compactness_mean": 0.2776,
            "concavity_mean": 0.3001,
            "concave_points_mean": 0.1471,
            "symmetry_mean": 0.2419,
            "fractal_dimension_mean": 0.07871,
        }
        resp = self.client.post(reverse("predict_breast_cancer"), payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Prediction Outcome")
        self.assertTrue(PredictionRecord.objects.filter(user=self.user1, disease="breast_cancer").exists())
        record = PredictionRecord.objects.get(user=self.user1, disease="breast_cancer")
        self.assertIn(record.risk_level, ["Low", "Moderate", "High"])

    def test_prediction_detail_authorization_protection(self):
        record1 = PredictionRecord.objects.create(
            user=self.user1,
            disease="heart",
            input_data={"age": 55},
            risk_score=75.5,
            risk_level="High",
            model_used="Random Forest"
        )

        # User 1 can view own record
        self.client.login(username="patient1", password="Password123!")
        resp1 = self.client.get(reverse("prediction_detail", args=[record1.id]))
        self.assertEqual(resp1.status_code, 200)
        self.assertContains(resp1, "High Risk")

        # User 2 CANNOT view User 1's record (Strict 403 Forbidden)
        self.client.login(username="patient2", password="Password123!")
        resp2 = self.client.get(reverse("prediction_detail", args=[record1.id]))
        self.assertEqual(resp2.status_code, 403)

    def test_delete_prediction_record(self):
        record1 = PredictionRecord.objects.create(
            user=self.user1,
            disease="diabetes",
            input_data={"glucose": 110},
            risk_score=25.0,
            risk_level="Low",
            model_used="Random Forest"
        )

        # User 2 cannot delete User 1's record
        self.client.login(username="patient2", password="Password123!")
        resp_del_unauth = self.client.post(reverse("prediction_delete", args=[record1.id]))
        self.assertEqual(resp_del_unauth.status_code, 403)
        self.assertTrue(PredictionRecord.objects.filter(id=record1.id).exists())

        # User 1 can delete their own record
        self.client.login(username="patient1", password="Password123!")
        resp_del_auth = self.client.post(reverse("prediction_delete", args=[record1.id]))
        self.assertEqual(resp_del_auth.status_code, 302)
        self.assertFalse(PredictionRecord.objects.filter(id=record1.id).exists())

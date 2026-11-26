from django.db import models
from django.contrib.auth.models import User

class PredictionRecord(models.Model):
    DISEASES = [
        ("heart", "Heart Disease"),
        ("liver", "Liver Disease"),
        ("diabetes", "Diabetes"),
        ("kidney", "Kidney Disease"),
        ("breast_cancer", "Breast Cancer (Diagnostic)"),
    ]
    LEVELS = [("Low", "Low"), ("Moderate", "Moderate"), ("High", "High")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.CharField(max_length=20, choices=DISEASES)
    input_data = models.JSONField()
    risk_score = models.FloatField()
    risk_level = models.CharField(max_length=10, choices=LEVELS)
    model_used = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} - {self.get_disease_display()} - {self.risk_level}"

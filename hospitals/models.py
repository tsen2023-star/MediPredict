from django.db import models
class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100, db_index=True)
    phone = models.CharField(max_length=30)
    specialties = models.CharField(max_length=300, help_text="Comma-separated specialties")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self): return f"{self.name} ({self.city})"

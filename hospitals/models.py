import urllib.parse
from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100, db_index=True)
    phone = models.CharField(max_length=50)
    emergency_contact = models.CharField(max_length=50, blank=True, help_text="Emergency / Ambulance helpline")
    website = models.URLField(blank=True, help_text="Official hospital website")
    specialties = models.CharField(max_length=300, help_text="Comma-separated specialties (e.g. Cardiology, Hepatology, Endocrinology)")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def specialties_list(self):
        if self.specialties:
            return [s.strip() for s in self.specialties.split(",") if s.strip()]
        return []

    def get_map_url(self):
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
        query = f"{self.name}, {self.city}"
        return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(query)}"

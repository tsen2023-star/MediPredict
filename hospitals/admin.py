from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "phone", "is_verified", "created_at")
    list_filter = ("state", "city", "is_verified")
    search_fields = ("name", "city", "state", "address", "specialties")

from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "is_verified", "created_at")
    list_filter = ("city", "is_verified")
    search_fields = ("name", "city", "address", "specialties")

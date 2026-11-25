from django.contrib import admin
from .models import PredictionRecord
@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "disease", "risk_score", "risk_level", "model_used", "created_at")
    list_filter = ("disease", "risk_level", "created_at")
    readonly_fields = ("created_at",)

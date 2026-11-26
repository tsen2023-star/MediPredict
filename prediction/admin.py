from django.contrib import admin
from django.utils.html import format_html
import json
from .models import PredictionRecord


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "get_disease_display", "colored_risk", "risk_score_display", "model_used", "created_at")
    list_filter = ("disease", "risk_level", "created_at")
    search_fields = ("user__username", "user__email", "disease", "model_used")
    readonly_fields = ("created_at", "formatted_input_data")
    date_hierarchy = "created_at"

    def risk_score_display(self, obj):
        return f"{obj.risk_score}%"
    risk_score_display.short_description = "Score"

    def colored_risk(self, obj):
        colors = {
            "High": "#dc3545",
            "Moderate": "#fd7e14",
            "Low": "#198754"
        }
        color = colors.get(obj.risk_level, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold;">{}</span>',
            color,
            obj.risk_level
        )
    colored_risk.short_description = "Risk Level"

    def formatted_input_data(self, obj):
        return format_html(
            '<pre style="background: #f8f9fa; padding: 12px; border-radius: 6px; max-height: 400px; overflow-y: auto;">{}</pre>',
            json.dumps(obj.input_data, indent=2)
        )
    formatted_input_data.short_description = "Biometric Input Parameters (JSON)"

from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "category", "rating", "is_reviewed", "created_at")
    list_filter = ("rating", "category", "is_reviewed", "created_at")
    search_fields = ("user__username", "user__email", "subject", "message", "admin_response")
    readonly_fields = ("created_at",)
    list_editable = ("is_reviewed",)

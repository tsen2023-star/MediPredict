from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    CATEGORIES = [
        ("general", "General Experience"),
        ("prediction", "Prediction Accuracy & Insights"),
        ("ui_ux", "Design, Navigation & Usability"),
        ("bug", "Bug Report / Technical Issue"),
        ("feature", "Feature Request / Suggestion"),
    ]

    RATING_CHOICES = [
        (5, "5 Stars - Excellent"),
        (4, "4 Stars - Very Good"),
        (3, "3 Stars - Good / Average"),
        (2, "2 Stars - Needs Improvement"),
        (1, "1 Star - Poor Experience"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    subject = models.CharField(max_length=150, default="General Feedback")
    category = models.CharField(max_length=50, choices=CATEGORIES, default="general")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    message = models.TextField()
    is_reviewed = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.get_category_display()} ({self.rating}★) on {self.created_at:%Y-%m-%d}"

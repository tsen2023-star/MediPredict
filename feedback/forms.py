from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    subject = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Brief title or summary of your feedback"
        })
    )
    category = forms.ChoiceField(
        choices=Feedback.CATEGORIES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    rating = forms.TypedChoiceField(
        choices=Feedback.RATING_CHOICES,
        coerce=int,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Tell us what worked well or what we can improve..."
        })
    )

    class Meta:
        model = Feedback
        fields = ["subject", "category", "rating", "message"]

    def clean_message(self):
        msg = self.cleaned_data.get("message", "").strip()
        if len(msg) < 10:
            raise forms.ValidationError("Please provide at least 10 characters describing your feedback.")
        return msg

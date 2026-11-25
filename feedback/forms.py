from django import forms
from .models import Feedback
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["message"]
        widgets = {"message": forms.Textarea(attrs={"class":"form-control", "rows":5, "placeholder":"Share your feedback..."})}

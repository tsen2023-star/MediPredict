from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback


@login_required
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Thank you! Your feedback has been received and will help improve MediPredict.")
            return redirect("feedback")
        else:
            messages.error(request, "Please correct the errors in the feedback form.")
    else:
        form = FeedbackForm()

    user_feedbacks = Feedback.objects.filter(user=request.user)[:5]

    return render(
        request,
        "feedback/form.html",
        {
            "form": form,
            "user_feedbacks": user_feedbacks,
        }
    )

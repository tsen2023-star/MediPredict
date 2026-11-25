from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import FeedbackForm
@login_required
def feedback_view(request):
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Thank you. Your feedback has been submitted.")
        return redirect("feedback")
    return render(request, "feedback/form.html", {"form": form})

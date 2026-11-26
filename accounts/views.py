from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from prediction.models import PredictionRecord
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def home(request):
    total_records = PredictionRecord.objects.count()
    return render(request, "home.html", {"total_records": total_records})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Welcome to MediPredict, {user.username}! Your account has been created. Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the registration errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.POST.get("next") or request.GET.get("next") or "dashboard"
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out securely.")
        return redirect("home")
    return render(request, "accounts/logout_confirm.html")


@login_required
def dashboard(request):
    user_predictions = PredictionRecord.objects.filter(user=request.user)
    total_predictions = user_predictions.count()
    heart_count = user_predictions.filter(disease="heart").count()
    diabetes_count = user_predictions.filter(disease="diabetes").count()
    liver_count = user_predictions.filter(disease="liver").count()
    kidney_count = user_predictions.filter(disease="kidney").count()
    breast_cancer_count = user_predictions.filter(disease="breast_cancer").count()

    recent_history = user_predictions.order_by("-created_at")[:6]
    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(
        request,
        "accounts/dashboard.html",
        {
            "profile": profile,
            "total_predictions": total_predictions,
            "heart_count": heart_count,
            "diabetes_count": diabetes_count,
            "liver_count": liver_count,
            "kidney_count": kidney_count,
            "breast_cancer_count": breast_cancer_count,
            "recent_history": recent_history,
        }
    )


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_predictions = PredictionRecord.objects.filter(user=request.user)
    total_predictions = user_predictions.count()
    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "total_predictions": total_predictions,
        }
    )


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors in the profile form.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/profile_edit.html",
        {
            "u_form": u_form,
            "p_form": p_form,
        }
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password was changed successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})

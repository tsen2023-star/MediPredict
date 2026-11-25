from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from prediction.models import PredictionRecord
from .forms import RegisterForm

def home(request):
    return render(request, "home.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return render(request, "accounts/logout_confirm.html")

@login_required
def dashboard(request):
    history = PredictionRecord.objects.filter(user=request.user).order_by("-created_at")[:20]
    return render(request, "accounts/dashboard.html", {"history": history})

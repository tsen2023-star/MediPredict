from django.contrib import admin
from django.urls import path, include
from accounts.views import home, dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("accounts/", include("accounts.urls")),
    path("", include("prediction.urls")),
    path("hospitals/", include("hospitals.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("feedback/", include("feedback.urls")),
]

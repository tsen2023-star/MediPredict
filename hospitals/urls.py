from django.urls import path
from . import views

urlpatterns = [
    path("", views.hospital_list, name="hospitals"),
    path("<int:pk>/", views.hospital_detail, name="hospital_detail"),
]

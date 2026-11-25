from django.urls import path
from . import views
urlpatterns = [
 path("predict/heart/", views.heart, name="predict_heart"),
 path("predict/liver/", views.liver, name="predict_liver"),
 path("predict/diabetes/", views.diabetes, name="predict_diabetes"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("predict/heart/", views.heart, name="predict_heart"),
    path("predict/liver/", views.liver, name="predict_liver"),
    path("predict/diabetes/", views.diabetes, name="predict_diabetes"),
    path("predictions/history/", views.history_list, name="prediction_history"),
    path("predictions/<int:pk>/", views.prediction_detail, name="prediction_detail"),
    path("predictions/<int:pk>/delete/", views.prediction_delete, name="prediction_delete"),
]

import json
from pathlib import Path
import joblib
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import HeartForm, LiverForm, DiabetesForm
from .models import PredictionRecord

MODEL_DIR = Path(settings.BASE_DIR) / "prediction" / "ml"
CONFIG = {
 "heart": (HeartForm, "heart_model.pkl", "Heart Disease"),
 "liver": (LiverForm, "liver_model.pkl", "Liver Disease"),
 "diabetes": (DiabetesForm, "diabetes_model.pkl", "Diabetes"),
}

def risk_level(score):
    if score < 0.30: return "Low"
    if score < 0.60: return "Moderate"
    return "High"

@login_required
def predict(request, disease):
    if disease not in CONFIG:
        messages.error(request, "Unknown prediction type.")
        return render(request, "prediction/predict.html", {"disease": "Prediction", "form": None})
    form_class, filename, title = CONFIG[disease]
    form = form_class(request.POST or None)
    result = None
    if request.method == "POST" and form.is_valid():
        model_path = MODEL_DIR / filename
        if not model_path.exists():
            messages.error(request, f"The {title} model is not trained yet. Follow the ML setup instructions.")
        else:
            try:
                bundle = joblib.load(model_path)
                model = bundle["model"] if isinstance(bundle, dict) else bundle
                feature_names = bundle.get("features") if isinstance(bundle, dict) else None
                row = pd.DataFrame([form.cleaned_data])
                if feature_names:
                    row = row.reindex(columns=feature_names)
                probability = model.predict_proba(row)[0][1]
                score = float(probability)
                level = risk_level(score)
                record = PredictionRecord.objects.create(
                    user=request.user, disease=disease, input_data=form.cleaned_data,
                    risk_score=round(score * 100, 2), risk_level=level,
                    model_used=bundle.get("model_name", model.__class__.__name__) if isinstance(bundle, dict) else model.__class__.__name__
                )
                result = {"score": round(score * 100, 1), "level": level, "record": record}
            except Exception:
                messages.error(request, "Prediction could not be completed. Check that the model and form features match.")
    return render(request, "prediction/predict.html", {"form": form, "disease": title, "result": result})

@login_required
def heart(request): return predict(request, "heart")
@login_required
def liver(request): return predict(request, "liver")
@login_required
def diabetes(request): return predict(request, "diabetes")

import json
from pathlib import Path
import joblib
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import HeartForm, LiverForm, DiabetesForm, KidneyForm, BreastCancerForm
from .models import PredictionRecord

MODEL_DIR = Path(settings.BASE_DIR) / "prediction" / "ml"

CONFIG = {
    "heart": {
        "form": HeartForm,
        "file": "heart_model.pkl",
        "title": "Heart Disease",
        "icon": "bi-heart-pulse-fill",
        "badge": "Cardiovascular",
        "description": "Assess cardiovascular indicators against benchmark clinical data."
    },
    "liver": {
        "form": LiverForm,
        "file": "liver_model.pkl",
        "title": "Liver Disease",
        "icon": "bi-bandaid-fill",
        "badge": "Hepatic",
        "description": "Evaluate liver enzymes, bilirubin, and protein levels."
    },
    "diabetes": {
        "form": DiabetesForm,
        "file": "diabetes_model.pkl",
        "title": "Diabetes",
        "icon": "bi-droplet-fill",
        "badge": "Metabolic",
        "description": "Examine glucose, BMI, and metabolic markers."
    },
    "kidney": {
        "form": KidneyForm,
        "file": "kidney_model.pkl",
        "title": "Kidney Disease (CKD)",
        "icon": "bi-shield-plus",
        "badge": "Renal",
        "description": "Assess kidney filtration efficiency, urea, creatinine, and urinalysis markers."
    },
    "breast_cancer": {
        "form": BreastCancerForm,
        "file": "breast_cancer_model.pkl",
        "title": "Breast Cancer (Diagnostic)",
        "icon": "bi-activity",
        "badge": "Oncology",
        "description": "Analyze fine needle aspirate (FNA) cell nucleus characteristics."
    },
}

SAMPLE_DATA = {
    "heart": {
        "normal": {
            "age": 36, "sex": 1, "cp": 0, "trestbps": 118, "chol": 190,
            "fbs": 0, "restecg": 0, "thalach": 165, "exang": 0, "oldpeak": 0.2,
            "slope": 0, "ca": 0, "thal": 0
        },
        "risk": {
            "age": 62, "sex": 1, "cp": 2, "trestbps": 155, "chol": 280,
            "fbs": 1, "restecg": 1, "thalach": 122, "exang": 1, "oldpeak": 2.8,
            "slope": 2, "ca": 2, "thal": 2
        }
    },
    "diabetes": {
        "normal": {
            "pregnancies": 1, "glucose": 95, "blood_pressure": 72, "skin_thickness": 18,
            "insulin": 45, "bmi": 22.4, "diabetes_pedigree_function": 0.25, "age": 28
        },
        "risk": {
            "pregnancies": 4, "glucose": 168, "blood_pressure": 88, "skin_thickness": 34,
            "insulin": 190, "bmi": 35.8, "diabetes_pedigree_function": 0.85, "age": 52
        }
    },
    "liver": {
        "normal": {
            "age": 32, "gender": 1, "total_bilirubin": 0.8, "direct_bilirubin": 0.2,
            "alkaline_phosphotase": 110, "alamine_aminotransferase": 22,
            "aspartate_aminotransferase": 24, "total_proteins": 7.2, "albumin": 4.1,
            "albumin_and_globulin_ratio": 1.3
        },
        "risk": {
            "age": 56, "gender": 1, "total_bilirubin": 3.4, "direct_bilirubin": 1.6,
            "alkaline_phosphotase": 380, "alamine_aminotransferase": 85,
            "aspartate_aminotransferase": 110, "total_proteins": 5.8, "albumin": 2.5,
            "albumin_and_globulin_ratio": 0.75
        }
    },
    "kidney": {
        "normal": {
            "age": 42, "bp": 75, "sg": 1.020, "al": 0, "su": 0,
            "bgr": 105, "bu": 24, "sc": 0.9, "sod": 140, "pot": 4.5, "hemo": 15.2
        },
        "risk": {
            "age": 64, "bp": 90, "sg": 1.010, "al": 3, "su": 2,
            "bgr": 210, "bu": 85, "sc": 3.8, "sod": 130, "pot": 5.8, "hemo": 9.4
        }
    },
    "breast_cancer": {
        "normal": {
            "radius_mean": 11.85, "texture_mean": 17.26, "perimeter_mean": 76.53, "area_mean": 434.0,
            "smoothness_mean": 0.090, "compactness_mean": 0.071, "concavity_mean": 0.038,
            "concave_points_mean": 0.021, "symmetry_mean": 0.173, "fractal_dimension_mean": 0.062
        },
        "risk": {
            "radius_mean": 17.99, "texture_mean": 21.60, "perimeter_mean": 122.8, "area_mean": 1001.0,
            "smoothness_mean": 0.118, "compactness_mean": 0.277, "concavity_mean": 0.300,
            "concave_points_mean": 0.147, "symmetry_mean": 0.241, "fractal_dimension_mean": 0.078
        }
    }
}

HEALTH_GUIDANCE = {
    "heart": {
        "High": {
            "summary": "Your submitted cardiovascular parameters indicate an elevated statistical risk profile.",
            "recommendations": [
                "Schedule a clinical evaluation with a cardiologist or physician promptly.",
                "Discuss diagnostic tests such as a 12-lead ECG, Lipid Profile panel, and Echocardiogram.",
                "Monitor resting blood pressure daily and record readings for your doctor.",
                "Limit saturated fats, sodium intake, and avoid tobacco exposure completely."
            ],
            "lifestyle": "Prioritize heart-healthy nutrition, low-intensity guided walking, and stress-reduction techniques.",
            "status_color": "danger"
        },
        "Moderate": {
            "summary": "Certain cardiovascular metrics (such as blood pressure, cholesterol, or age) are borderline.",
            "recommendations": [
                "Consult your primary care physician for a routine cardiovascular screening.",
                "Request a comprehensive lipid profile to check LDL, HDL, and Triglycerides.",
                "Review daily dietary sodium and saturated fat consumption."
            ],
            "lifestyle": "Incorporate 30 minutes of moderate aerobic exercise 5 days a week and maintain optimal hydration.",
            "status_color": "warning"
        },
        "Low": {
            "summary": "Your submitted cardiovascular metrics align with a lower estimated risk category.",
            "recommendations": [
                "Maintain periodic routine health check-ups and annual blood pressure monitoring.",
                "Continue balanced cardiovascular lifestyle practices."
            ],
            "lifestyle": "Sustain a balanced diet rich in leafy vegetables, whole grains, lean proteins, and stay physically active.",
            "status_color": "success"
        }
    },
    "liver": {
        "High": {
            "summary": "Your reported liver enzymes (ALT, AST, ALP) or bilirubin levels show marked elevations.",
            "recommendations": [
                "Seek medical consultation with a gastroenterologist or hepatologist.",
                "Undergo a complete Liver Function Test (LFT) panel and abdominal ultrasound.",
                "Refrain from alcohol consumption and avoid unprescribed medications or hepatotoxic substances."
            ],
            "lifestyle": "Stay hydrated, maintain low-sodium and antioxidant-rich meals, and avoid processed fast foods.",
            "status_color": "danger"
        },
        "Moderate": {
            "summary": "Some liver parameters indicate mild enzyme elevation or suboptimal protein ratios.",
            "recommendations": [
                "Discuss these findings with a general physician for an LFT review.",
                "Recheck enzyme levels in 4–6 weeks as advised by your healthcare provider.",
                "Limit alcohol intake and review over-the-counter painkillers (such as acetaminophen)."
            ],
            "lifestyle": "Engage in regular physical activity to reduce hepatic fat accumulation and consume a fiber-rich diet.",
            "status_color": "warning"
        },
        "Low": {
            "summary": "Your liver enzyme and protein values fall largely within expected normal limits.",
            "recommendations": [
                "Continue routine preventive annual health examinations.",
                "Stay mindful of alcohol moderation and medication guidelines."
            ],
            "lifestyle": "Maintain adequate daily water intake, a nutrient-dense diet, and a healthy body weight.",
            "status_color": "success"
        }
    },
    "diabetes": {
        "High": {
            "summary": "Your glucose, BMI, and insulin-related markers indicate an elevated likelihood of diabetes or insulin resistance.",
            "recommendations": [
                "Consult an endocrinologist or primary care physician for confirmatory clinical testing.",
                "Request Glycated Hemoglobin (HbA1c) and Fasting Blood Glucose (FBG) lab tests.",
                "Discuss glucose self-monitoring and professional dietary counseling."
            ],
            "lifestyle": "Significantly reduce refined carbohydrates and sugary beverages; implement portion control.",
            "status_color": "danger"
        },
        "Moderate": {
            "summary": "Your submitted metrics suggest borderline or pre-diabetic risk factors.",
            "recommendations": [
                "Schedule a checkup to assess fasting blood glucose and HbA1c levels.",
                "Explore early lifestyle interventions that can halt progression to type 2 diabetes.",
                "Evaluate family history predisposition with your physician."
            ],
            "lifestyle": "Engage in regular post-meal walking, increase dietary soluble fiber, and manage body weight.",
            "status_color": "warning"
        },
        "Low": {
            "summary": "Your submitted metabolic indicators correspond to a lower estimated risk category.",
            "recommendations": [
                "Continue standard periodic screening during annual check-ups.",
                "Stay active and keep blood sugar and blood pressure within target ranges."
            ],
            "lifestyle": "Enjoy a balanced diet of unrefined whole foods, prioritize 7–8 hours of restful sleep, and stay active.",
            "status_color": "success"
        }
    },
    "kidney": {
        "High": {
            "summary": "Your renal parameters (creatinine, blood urea, albuminuria) indicate elevated risk of chronic kidney impairment.",
            "recommendations": [
                "Consult a nephrologist or physician for a comprehensive Renal Function Test (RFT).",
                "Measure estimated Glomerular Filtration Rate (eGFR) and urine protein-creatinine ratio.",
                "Strictly manage blood pressure, avoid NSAID painkillers, and restrict excessive dietary sodium."
            ],
            "lifestyle": "Ensure appropriate daily fluid intake as advised by your physician, reduce sodium, and monitor blood pressure.",
            "status_color": "danger"
        },
        "Moderate": {
            "summary": "Some kidney markers (such as borderline urea, specific gravity, or blood pressure) warrant clinical review.",
            "recommendations": [
                "Discuss repeat urinalysis and creatinine screening with your primary care provider.",
                "Review daily medication regimens and ensure optimal hydration."
            ],
            "lifestyle": "Maintain a low-sodium, plant-forward diet and avoid unprescribed over-the-counter pain medications.",
            "status_color": "warning"
        },
        "Low": {
            "summary": "Your kidney filtration markers and urinalysis values align with healthy control reference ranges.",
            "recommendations": [
                "Maintain routine periodic health checkups and monitor blood pressure annually.",
                "Stay mindful of adequate daily hydration."
            ],
            "lifestyle": "Drink 2–3 liters of water daily, consume whole fruits and vegetables, and maintain an active routine.",
            "status_color": "success"
        }
    },
    "breast_cancer": {
        "High": {
            "summary": "The cytological nuclear measurements exhibit statistical characteristics associated with tissue malignancy.",
            "recommendations": [
                "Consult a specialist surgical oncologist or breast specialist promptly.",
                "Proceed with clinical breast examination, bilateral digital diagnostic mammography, and ultrasound.",
                "Discuss histopathological core needle biopsy confirmation with your oncologist."
            ],
            "lifestyle": "Follow specialist recommendations promptly and review family history with a medical genetics counselor.",
            "status_color": "danger"
        },
        "Moderate": {
            "summary": "Some nuclear morphology parameters show borderline variations requiring further diagnostic imaging.",
            "recommendations": [
                "Schedule a clinical evaluation and follow-up high-resolution breast ultrasound.",
                "Review prior imaging for baseline comparison."
            ],
            "lifestyle": "Maintain monthly breast self-awareness, an active lifestyle, and scheduled clinical screenings.",
            "status_color": "warning"
        },
        "Low": {
            "summary": "Your reported cellular nucleus parameters correspond to benign baseline tissue characteristics.",
            "recommendations": [
                "Continue standard age-appropriate clinical screening mammograms.",
                "Maintain periodic routine breast self-awareness."
            ],
            "lifestyle": "Maintain regular physical activity, a nutritious balanced diet, and avoid tobacco exposure.",
            "status_color": "success"
        }
    }
}


def risk_level(score):
    if score < 0.35:
        return "Low"
    if score < 0.65:
        return "Moderate"
    return "High"


def ensure_model_trained(disease):
    """Fallback to train model on-the-fly if missing from disk."""
    cfg = CONFIG[disease]
    filename = cfg["file"]
    model_path = MODEL_DIR / filename
    if not model_path.exists():
        try:
            from .ml.train_models import train_one, FILES
            fn, tgt = FILES[disease]
            train_one(disease, fn, tgt)
        except Exception:
            pass
    return model_path


@login_required
def predict(request, disease):
    if disease not in CONFIG:
        messages.error(request, "Unknown prediction type requested.")
        return redirect("dashboard")

    cfg = CONFIG[disease]
    form_class = cfg["form"]
    filename = cfg["file"]
    title = cfg["title"]

    form = form_class(request.POST or None)
    result = None
    guidance = None

    if request.method == "POST":
        if form.is_valid():
            model_path = ensure_model_trained(disease)
            if not model_path.exists():
                messages.error(
                    request,
                    f"The {title} trained model artifact ({filename}) is not found on the server. "
                    "Please ensure the ML pipeline has been run."
                )
            else:
                try:
                    bundle = joblib.load(model_path)
                    model = bundle["model"] if isinstance(bundle, dict) else bundle
                    feature_names = bundle.get("features") if isinstance(bundle, dict) else None

                    # Clean data row as DataFrame
                    clean_dict = dict(form.cleaned_data)
                    row = pd.DataFrame([clean_dict])
                    if feature_names:
                        row = row.reindex(columns=feature_names)

                    # Compute genuine model prediction probability
                    if hasattr(model, "predict_proba"):
                        proba = model.predict_proba(row)[0]
                        # Target class 1 is index 1
                        score = float(proba[1]) if len(proba) > 1 else float(proba[0])
                    else:
                        pred = model.predict(row)[0]
                        score = 1.0 if pred == 1 else 0.0

                    level = risk_level(score)
                    percentage = round(score * 100, 1)
                    model_name = bundle.get("model_name", model.__class__.__name__) if isinstance(bundle, dict) else model.__class__.__name__

                    is_positive = (score >= 0.50)
                    if is_positive:
                        outcome_text = f"Elevated Risk Detected ({percentage}%)"
                        outcome_badge = "Positive"
                    else:
                        outcome_text = f"Low Risk / Within Normal Bounds ({percentage}%)"
                        outcome_badge = "Negative"

                    record = PredictionRecord.objects.create(
                        user=request.user,
                        disease=disease,
                        input_data=clean_dict,
                        risk_score=percentage,
                        risk_level=level,
                        model_used=model_name
                    )

                    guidance = HEALTH_GUIDANCE.get(disease, {}).get(level, {})

                    result = {
                        "score": percentage,
                        "level": level,
                        "record": record,
                        "guidance": guidance,
                        "model_used": model_name,
                        "outcome_text": outcome_text,
                        "outcome_badge": outcome_badge,
                        "is_positive": is_positive,
                    }
                    messages.success(request, f"Preliminary {title} risk assessment generated successfully.")

                except Exception as ex:
                    messages.error(
                        request,
                        f"An error occurred while evaluating the model: {str(ex)}. Please review your inputs."
                    )
        else:
            err_list = []
            for field, errs in form.errors.items():
                label = form.fields[field].label if field in form.fields else field
                err_list.append(f"{label}: {', '.join(errs)}")
            summary = "; ".join(err_list[:3])
            messages.error(request, f"Please correct the following errors: {summary}")

    samples = SAMPLE_DATA.get(disease, {})

    return render(
        request,
        "prediction/predict.html",
        {
            "form": form,
            "disease": title,
            "disease_key": disease,
            "config": cfg,
            "result": result,
            "guidance": guidance,
            "samples_json": json.dumps(samples),
        }
    )


@login_required
def heart(request):
    return predict(request, "heart")


@login_required
def liver(request):
    return predict(request, "liver")


@login_required
def diabetes(request):
    return predict(request, "diabetes")


@login_required
def kidney(request):
    return predict(request, "kidney")


@login_required
def breast_cancer(request):
    return predict(request, "breast_cancer")


@login_required
def history_list(request):
    """Full prediction history list with pagination and disease filter."""
    disease_filter = request.GET.get("disease", "").strip()
    records = PredictionRecord.objects.filter(user=request.user)

    if disease_filter in CONFIG:
        records = records.filter(disease=disease_filter)

    records = records.order_by("-created_at")
    paginator = Paginator(records, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "prediction/history.html",
        {
            "page_obj": page_obj,
            "disease_filter": disease_filter,
            "configs": CONFIG,
            "total_count": paginator.count,
        }
    )


@login_required
def prediction_detail(request, pk):
    """View individual prediction details with inputs and clinical guidance."""
    record = get_object_or_404(PredictionRecord, pk=pk)

    # Strict authorization check: prevent unauthorized access across accounts
    if record.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this prediction record.")

    cfg = CONFIG.get(record.disease, {})
    guidance = HEALTH_GUIDANCE.get(record.disease, {}).get(record.risk_level, {})

    return render(
        request,
        "prediction/detail.html",
        {
            "record": record,
            "config": cfg,
            "guidance": guidance,
        }
    )


@login_required
@require_POST
def prediction_delete(request, pk):
    """Securely delete a prediction record owned by the authenticated user."""
    record = get_object_or_404(PredictionRecord, pk=pk)

    # Strict ownership check
    if record.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete another user's prediction record.")

    disease_name = record.get_disease_display()
    record.delete()
    messages.success(request, f"Prediction record for {disease_name} was removed successfully.")
    return redirect("prediction_history")

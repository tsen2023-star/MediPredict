import json
import os
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

# Medical emergency keywords requiring immediate triage
EMERGENCY_TRIGGERS = [
    "severe chest pain", "chest pressure", "crushing chest", "heart attack",
    "difficulty breathing", "cannot breathe", "breathing difficulty", "shortness of breath",
    "fainting", "passed out", "unconscious", "stroke", "face drooping",
    "slurred speech", "paralysis", "weakness on one side", "coughing blood",
    "vomiting blood", "severe bleeding", "overdose", "suicide", "suicidal"
]

DISCLAIMER_SUFFIX = "\n\n(Notice: MediPredict Assistant provides educational health awareness only. It cannot diagnose conditions or replace evaluation by a qualified medical professional.)"


def get_rule_based_response(text):
    clean = text.lower().strip()

    # 1. Emergency safety check
    if any(trigger in clean for trigger in EMERGENCY_TRIGGERS):
        return (
            "EMERGENCY ADVISORY: The symptoms you described may be life-threatening indicators "
            "(such as acute coronary syndrome, stroke, or severe respiratory failure). "
            "Please call local emergency services immediately (112 / 102 in India, 911 in North America) "
            "or proceed to the nearest hospital Emergency Room immediately. Do not rely on online tools."
            + DISCLAIMER_SUFFIX
        )

    # 2. About MediPredict & Project Scope
    if any(k in clean for k in ["what is medipredict", "about this", "purpose", "who are you", "what can you do"]):
        return (
            "MediPredict is an intelligent health-awareness web platform designed to assist individuals in "
            "understanding preliminary clinical risk factors for Heart Disease, Liver Disease, and Diabetes. "
            "Using machine learning models trained on benchmark clinical datasets, it calculates statistical risk "
            "probabilities, visualizes health metrics, explains laboratory parameters, and guides you to verified "
            "healthcare centers."
            + DISCLAIMER_SUFFIX
        )

    # 3. How to use prediction modules
    if any(k in clean for k in ["how to use", "how do i use", "how does it work", "how to predict"]):
        return (
            "To use MediPredict:\n"
            "1. Navigate to your Dashboard or select a disease module (Heart, Diabetes, or Liver).\n"
            "2. Fill in the biometric parameters from your recent laboratory reports (such as blood pressure, glucose, or cholesterol).\n"
            "3. Click 'Compute Prediction' to generate a preliminary statistical risk evaluation.\n"
            "4. Review the educational guidance, parameter breakdowns, and recommended tests to discuss with your doctor.\n"
            "5. Access previous assessments anytime via the 'Prediction History' page."
            + DISCLAIMER_SUFFIX
        )

    # 4. Heart Disease Information
    if "heart" in clean or "cardio" in clean or "angina" in clean or "chest pain" in clean or "cholesterol" in clean:
        return (
            "Cardiovascular Health Awareness:\n"
            "- Key risk factors include hypertension (high blood pressure), elevated LDL cholesterol, diabetes, sedentary lifestyle, and smoking.\n"
            "- Parameters evaluated in our Heart module include Resting BP (trestbps), Serum Cholesterol, Resting ECG, Maximum Heart Rate (thalach), ST depression (oldpeak), and Exercise Angina.\n"
            "- Heart-healthy habits: Follow a diet rich in vegetables, fruits, and omega-3 fatty acids; limit sodium to under 2,000 mg/day; and engage in at least 150 minutes of moderate aerobic exercise weekly."
            + DISCLAIMER_SUFFIX
        )

    # 5. Diabetes & Blood Sugar Information
    if "diabetes" in clean or "glucose" in clean or "sugar" in clean or "insulin" in clean or "hba1c" in clean:
        return (
            "Diabetes & Metabolic Awareness:\n"
            "- Diabetes mellitus is characterized by persistent hyperglycemia due to insulin resistance or insufficient insulin production.\n"
            "- Our Diabetes prediction module evaluates fasting glucose, Body Mass Index (BMI), diastolic blood pressure, triceps skinfold thickness, serum insulin, and diabetes pedigree function.\n"
            "- Preventative tips: Maintain a healthy weight (BMI 18.5–24.9), choose whole grains with a low glycemic index, stay active after meals, and perform periodic HbA1c screenings if you have a family history."
            + DISCLAIMER_SUFFIX
        )

    # 6. Liver Disease Information
    if "liver" in clean or "bilirubin" in clean or "sgpt" in clean or "sgot" in clean or "alt" in clean or "ast" in clean or "alkaline" in clean:
        return (
            "Liver Health & Enzyme Awareness:\n"
            "- The liver filters toxins, metabolizes medications, and synthesizes critical plasma proteins like albumin.\n"
            "- Elevated SGPT (ALT) and SGOT (AST) enzymes, high total bilirubin, or an abnormal albumin-to-globulin (A/G) ratio can indicate hepatic inflammation or fatty liver disease.\n"
            "- Liver wellness tips: Avoid excessive alcohol intake, maintain balanced hydration, avoid unnecessary high doses of paracetamol/acetaminophen, and consume a nutrient-rich, low-sugar diet."
            + DISCLAIMER_SUFFIX
        )

    # 7. Hospitals & Healthcare Directory
    if "hospital" in clean or "doctor" in clean or "clinic" in clean or "nearest" in clean or "emergency" in clean:
        return (
            "Healthcare Directory:\n"
            "MediPredict includes a curated directory of verified multi-specialty hospitals and emergency facilities. "
            "You can search by facility name, city (e.g. New Delhi, Mumbai, Bengaluru, Chennai, Hyderabad), or specialty (Cardiology, Hepatology, Diabetes). "
            "Direct phone lines and GPS Google Maps directions are available on the 'Hospitals' page in the top menu."
            + DISCLAIMER_SUFFIX
        )

    # 8. Feedback & Support
    if "feedback" in clean or "contact" in clean or "report" in clean or "bug" in clean:
        return (
            "We value your input! You can submit feedback, star ratings, or bug reports via the 'Feedback' page "
            "in the top navigation bar. Our administrators review all submissions to continually enhance the application."
            + DISCLAIMER_SUFFIX
        )

    # 9. Generic / Fallback greeting
    if any(k in clean for k in ["hello", "hi", "hey", "good morning", "good evening"]):
        return (
            "Hello! I am your MediPredict Health Awareness Assistant. "
            "I can explain cardiovascular indicators, diabetes risk parameters, liver function tests, "
            "preventative lifestyle practices, and how to use the prediction modules. How can I assist you today?"
            + DISCLAIMER_SUFFIX
        )

    # 10. Fallback for unspecified inquiries
    return (
        "I am designed to provide health-awareness information and guide you through the MediPredict system. "
        "I can answer questions regarding:\n"
        "• Heart disease risk factors and ECG parameters\n"
        "• Diabetes screening, glucose, and BMI\n"
        "• Liver enzyme tests (Bilirubin, SGPT/ALT, SGOT/AST, Albumin)\n"
        "• How to use our machine-learning prediction modules\n"
        "• Finding verified hospitals and healthcare directories\n\n"
        "Please ask about any of these topics, or consult your primary care physician for clinical questions."
        + DISCLAIMER_SUFFIX
    )


def generate_ai_response(user_message):
    """
    Optional external AI integration via GEMINI_API_KEY.
    Gracefully falls back to the local healthcare awareness engine if not configured.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = (
            "You are MediPredict Health Assistant, an educational health-awareness bot for a Django web application. "
            "Answer the user's question clearly and factually. "
            "Guidelines: Focus on preventive health awareness, healthy lifestyle, explaining medical parameters (like BP, glucose, cholesterol, liver enzymes), and explaining how risk assessment works. "
            "CRITICAL: Never claim to diagnose diseases, prescribe medication, or replace a doctor. "
            "If the user mentions emergency warning signs (chest pain, stroke, breathing failure), urge them to contact emergency services immediately. "
            "Keep the reply concise (under 150 words). User message: " + user_message
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        if response and response.text:
            return response.text.strip() + DISCLAIMER_SUFFIX
    except Exception:
        # Fall back gracefully to rule-based engine
        pass
    return None


@login_required
def chatbot_page(request):
    return render(request, "chatbot/chat.html")


@login_required
@require_POST
def chatbot_api(request):
    try:
        data = json.loads(request.body)
        message = str(data.get("message", "")).strip()[:1000]
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"reply": "Please enter a valid message."}, status=400)

    if not message:
        return JsonResponse({"reply": "Please enter a question or topic."}, status=400)

    # Check for AI API first, else use comprehensive rule-based system
    ai_reply = generate_ai_response(message)
    reply_text = ai_reply if ai_reply else get_rule_based_response(message)

    return JsonResponse({"reply": reply_text, "response": reply_text})

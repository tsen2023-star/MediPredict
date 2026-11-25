import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

URGENT = ["severe chest pain", "difficulty breathing", "breathing difficulty", "fainting",
          "face drooping", "slurred speech", "weakness on one side", "stroke"]
def reply(message):
    text = message.lower()
    if any(term in text for term in URGENT):
        return "These may be emergency warning signs. Seek emergency medical help immediately or contact your local emergency number. Do not wait for this chatbot."
    if "heart" in text:
        return "Heart disease risk can be associated with several factors. This site provides only a preliminary model-based risk estimate; consult a qualified healthcare professional."
    if "liver" in text:
        return "Liver conditions require clinical assessment and appropriate tests. This tool is not a diagnosis; please discuss concerns with a healthcare professional."
    if "diabetes" in text or "glucose" in text:
        return "Diabetes assessment requires appropriate laboratory testing and clinical review. This tool provides only a preliminary estimate."
    if "hospital" in text:
        return "Open the Hospitals page and search by city to view hospitals entered by the administrator."
    if "how" in text or "use" in text or "system" in text:
        return "Register or log in, choose a disease prediction page, enter valid health information, and review the preliminary result and disclaimer."
    return "I can answer general questions about heart disease, liver disease, diabetes, hospital listings, and how to use this website. I cannot diagnose or recommend treatment."
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
        return JsonResponse({"reply": "Please type a question."}, status=400)
    return JsonResponse({"reply": reply(message)})

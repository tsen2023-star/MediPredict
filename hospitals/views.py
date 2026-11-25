from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Hospital
@login_required
def hospital_list(request):
    city = request.GET.get("city", "").strip()
    hospitals = Hospital.objects.filter(city__icontains=city) if city else Hospital.objects.all()
    return render(request, "hospitals/list.html", {"hospitals": hospitals, "city": city})

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Hospital


@login_required
def hospital_list(request):
    query = request.GET.get("q", "").strip()
    city_filter = request.GET.get("city", "").strip()

    hospitals = Hospital.objects.all().order_by("city", "name")

    if query:
        hospitals = hospitals.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(specialties__icontains=query) |
            Q(address__icontains=query)
        )

    if city_filter:
        hospitals = hospitals.filter(city__icontains=city_filter)

    # Distinct cities for quick filtering
    available_cities = Hospital.objects.values_list("city", flat=True).distinct().order_by("city")

    paginator = Paginator(hospitals, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "hospitals/list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "city_filter": city_filter,
            "available_cities": available_cities,
            "total_count": paginator.count,
        }
    )


@login_required
def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    return render(
        request,
        "hospitals/detail.html",
        {
            "hospital": hospital,
        }
    )

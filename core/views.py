from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import CalculationForm
from .utils import calculate_relativistic


class HomeView(TemplateView):
    template_name = "core/home.html"


def health_check(request):
    return JsonResponse({"status": "ok"})


# Create your views here.


def relativistic_view(request):
    result = None
    if request.method == "POST":
        form = CalculationForm(request.POST)
        if form.is_valid():
            v = form.cleaned_data["velocity"]
            t0 = form.cleaned_data["proper_time"]
            gamma, dilated = calculate_relativistic(v, t0)
            result = {
                "velocity": v,
                "proper_time": t0,
                "gamma": gamma,
                "dilated_time": dilated,
            }
    else:
        form = CalculationForm()

    return render(request, "core/relativistic.html", {"form": form, "result": result})

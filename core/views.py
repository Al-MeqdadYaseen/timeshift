from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import CalculationForm
from .utils import calculate_relativistic
from django.contrib import messages
from .models import Calculation


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
            request.session["last_result"] = {
                "velocity": v,
                "proper_time": t0,
                "gamma": gamma,
                "dilated_time": dilated,
            }
            request.session["calc_result"] = {
                "velocity": v,
                "proper_time": t0,
                "gamma": gamma,
                "dilated_time": dilated,
            }
            return redirect("core:relativistic")
    else:
        request.session.get("calc_result", None)
        result = request.session.pop("last_result", None)
        if result:
            form = CalculationForm(
                initial={
                    "velocity": result["velocity"],
                    "proper_time": result["proper_time"],
                }
            )
        else:
            form = CalculationForm()

    return render(request, "core/relativistic.html", {"form": form, "result": result})


def save_calculation(request):
    if request.method == "POST":
        result = request.session.get("calc_result")

        if result:
            try:
                Calculation.objects.create(
                    velocity=result["velocity"],
                    proper_time=result["proper_time"],
                    gamma=result["gamma"],
                    dilated_time=result["dilated_time"],
                )
                messages.success(request, "Calculation saved successfully!")
            except (ValueError, TypeError, KeyError):
                messages.error(request, "Failed to save calculation.")
        else:
            messages.error(request, "Calculate first to save!")

    return redirect("core:relativistic")

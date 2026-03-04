from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import CalculationForm
from .utils import calculate_relativistic, calculate_gravitational
from django.contrib import messages
from .models import Calculation
from .objects import GRAVITATIONAL_OBJECTS


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["calculations"] = Calculation.objects.all().order_by("-created_at")[
            :10
        ]  # The latest 10
        return context


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


def gravitational_view(request):
    result = None
    error = None

    if request.method == "POST":
        try:
            t0 = float(request.POST.get("proper_time", ""))
            object_key = request.POST.get("object_key")

            if not object_key:
                error = "Please select an object"
            elif t0 < 0:
                error = "Time must be positive"
            elif object_key not in GRAVITATIONAL_OBJECTS:
                error = "Invalid object selection"
            else:
                obj = GRAVITATIONAL_OBJECTS[object_key]
                factor = obj["multiplier"]
                dilated = calculate_gravitational(t0, factor)

                request.session["grav_result"] = {
                    "calculation_type": "gravitational",
                    "proper_time": t0,
                    "dilated_time": dilated,
                    "gravitational_factor": factor,
                    "object_key": object_key,
                    "object_name": obj["name"],
                }
                result = request.session["grav_result"]

        except ValueError:
            error = "Please enter a valid number for time"
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render(
        request,
        "core/gravitational.html",
        {"objects": GRAVITATIONAL_OBJECTS, "result": result, "error": error},
    )

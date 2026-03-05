from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import CalculationForm
from .utils import calculate_relativistic, calculate_gravitational
from django.contrib import messages
from .models import Calculation
from .objects import GRAVITATIONAL_OBJECTS
from .helper import (
    store_calculation_result,
    get_stored_result,
    save_calculation_to_db,
    clear_stored_result,
)


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
    error = None
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
            store_calculation_result(request, "relativistic", result)
            return redirect("core:relativistic")
    else:
        form = CalculationForm()
        result = get_stored_result(request, "relativistic")
        if result:
            clear_stored_result(
                request, "relativistic"
            )  # Clear after displaying to prevent persistence on refresh

    return render(
        request,
        "core/relativistic.html",
        {"form": form, "result": result, "error": error},
    )


def gravitational_view(request):
    result = None
    error = None

    if request.method == "POST":
        try:
            # Get values with safe defaults
            t0_str = request.POST.get("proper_time", "").strip()
            object_key = request.POST.get("object_key", "").strip()

            # Validate presence
            if not t0_str:
                error = "Proper time is required"
            elif not object_key:
                error = "Please select an object"
            else:
                try:
                    t0 = float(t0_str)
                except ValueError:
                    error = "Proper time must be a valid number"
                else:
                    # Time validation
                    if t0 < 0:
                        error = "Proper time cannot be negative"
                    elif t0 > 1e9:  # 1 billion years cap
                        error = "Time value is too large (max 1e9 years)"

                    # Object validation (don't trust dropdown)
                    elif object_key not in GRAVITATIONAL_OBJECTS:
                        error = "Invalid object selection"

                    # All validations passed
                    else:
                        obj = GRAVITATIONAL_OBJECTS[object_key]
                        factor = obj["multiplier"]
                        dilated = calculate_gravitational(t0, factor)

                        # Store in session
                        result = {
                            "calculation_type": "gravitational",
                            "proper_time": t0,
                            "dilated_time": dilated,
                            "gravitational_factor": factor,
                            "object_key": object_key,
                            "object_name": obj["name"],
                        }
                        store_calculation_result(request, "gravitational", result)
                        return redirect("core:gravitational")

        except Exception as e:
            error = f"Unexpected error: {str(e)}"
        # Get result from session for GET requests
    else:
        result = get_stored_result(request, "gravitational")
        if result:
            clear_stored_result(
                request, "gravitational"
            )  # Clear after displaying to prevent persistence on refresh

    return render(
        request,
        "core/gravitational.html",
        {
            "objects": GRAVITATIONAL_OBJECTS,
            "result": result,
            "error": error,
            "last_input": request.POST.get("proper_time", ""),  # Preserve form input
        },
    )


# Unified Save View
def save_calculation(request, calc_type):
    """Generic save endpoint for both calculation types."""
    if request.method == "POST":
        success = save_calculation_to_db(request, calc_type, messages)

        if not success and calc_type == "relativistic":
            return redirect("core:relativistic")
        elif not success and calc_type == "gravitational":
            return redirect("core:gravitational")

    return redirect(f"core:{calc_type}")


# Legacy save views (kept for backward compatibility)
def save_calculation_relativistic(request):
    return save_calculation(request, "relativistic")


def save_calculation_gravitational(request):
    return save_calculation(request, "gravitational")

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
                    calculation_type="relativistic",
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
                        request.session["grav_result"] = {
                            "calculation_type": "gravitational",
                            "proper_time": t0,
                            "dilated_time": dilated,
                            "gravitational_factor": factor,
                            "object_key": object_key,
                            "object_name": obj["name"],
                        }
                        result = request.session["grav_result"]

        except Exception as e:
            error = f"Unexpected error: {str(e)}"

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


def save_gravitational(request):
    if request.method == "POST":
        result = request.session.get("grav_result")

        if result:
            Calculation.objects.create(
                calculation_type="gravitational",
                proper_time=result["proper_time"],
                dilated_time=result["dilated_time"],
                gravitational_factor=result["gravitational_factor"],
                object_key=result["object_key"],
                object_name=result["object_name"],
            )
            messages.success(request, "Gravitational calculation saved!")
            request.session.pop("grav_result", None)
        else:
            messages.error(request, "No calculation to save.")

    return redirect("core:gravitational")

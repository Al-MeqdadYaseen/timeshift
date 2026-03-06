from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import RelativisticForm, GravitationalForm
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
        form = RelativisticForm(request.POST)
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
            request.session["relativistic_form"] = request.POST
            request.session["relativistic_displayed"] = False
            return redirect("core:relativistic")
        else:
            # Form validation failed
            error = "Please correct the errors below."
    else:
        form_data = request.session.get("relativistic_form")
        if form_data:
            form = RelativisticForm(form_data)
        else:
            form = RelativisticForm()
        result = get_stored_result(request, "relativistic")
        if result:
            displayed = request.session.get("relativistic_displayed", False)
            if displayed:
                clear_stored_result(request, "relativistic")
                request.session["relativistic_displayed"] = False
                request.session.pop("relativistic_form", None)
                result = None
                form = RelativisticForm()
            else:
                request.session["relativistic_displayed"] = True

    return render(
        request,
        "core/relativistic.html",
        {"form": form, "result": result, "error": error},
    )


def gravitational_view(request):
    result = None
    if request.method == "POST":
        form = GravitationalForm(request.POST)
        if form.is_valid():
            t0 = form.cleaned_data["proper_time"]
            object_key = form.cleaned_data["object_key"]
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
            request.session["gravitational_form"] = request.POST
            request.session["gravitational_displayed"] = False
            return redirect("core:gravitational")
    else:
        form_data = request.session.get("gravitational_form")
        if form_data:
            form = GravitationalForm(form_data)
        else:
            form = GravitationalForm()
        result = get_stored_result(request, "gravitational")
        if result:
            displayed = request.session.get("gravitational_displayed", False)
            if displayed:
                clear_stored_result(request, "gravitational")
                request.session["gravitational_displayed"] = False
                request.session.pop("gravitational_form", None)
                result = None
                form = GravitationalForm()
            else:
                request.session["gravitational_displayed"] = True

    return render(
        request,
        "core/gravitational.html",
        {
            "form": form,
            "result": result,
        },
    )


# Unified Save View
def save_calculation(request, calc_type):
    """Generic save endpoint for both calculation types."""
    if request.method == "POST":

        # reset display flag so the next GET will show the result again
        request.session[f"{calc_type}_displayed"] = False
        # Check if result exists in session
        result = request.session.get(f"{calc_type}_result")
        if not result:
            messages.error(request, "No calculation to save. Please calculate first.")
            return redirect(f"core:{calc_type}")
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


# AI helped me with form validation in the views function, setting up the PRG (POST, Redirect, GET) sturcture for the views, and make the inputs and results persist after calculation and saving but get cleared when the page is refreshed.

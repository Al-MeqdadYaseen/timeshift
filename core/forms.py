from django import forms
from .objects import GRAVITATIONAL_OBJECTS


class CalculationForm(forms.Form):
    velocity = forms.FloatField(
        label="Velocity (fraction of c)",
        min_value=0.0,
        max_value=0.999999,  # UI cap to avoid extreme gamma values
        required=True,
        error_messages={
            "required": "Velocity is required",
            "min_value": "Velocity must a positive number",
            "max_value": "Velocity must be less than the speed of light",
        },
    )
    proper_time = forms.FloatField(
        label="Proper time (seconds)",
        min_value=0.0,
        required=True,
        error_messages={
            "required": "Proper time is required",
            "min_value": "Proper time must a positive number",
        },
    )

    def clean_proper_time(self):
        data = self.cleaned_data["proper_time"]
        if data <= 0:  # Reject zero and negative
            raise forms.ValidationError("Proper time must be greater than zero")
        return data


class GravitationalForm(forms.Form):
    proper_time = forms.FloatField(
        label="Proper time (seconds)",
        min_value=0.0,
        required=True,
        error_messages={
            "required": "Proper time is required",
            "min_value": "Proper time must be positive",
        },
    )
    object_key = forms.ChoiceField(
        label="Celestial Object",
        choices=[(k, v["name"]) for k, v in GRAVITATIONAL_OBJECTS.items()],
        required=True,
        error_messages={
            "required": "Please select an object",
        },
    )

    def clean_proper_time(self):
        data = self.cleaned_data["proper_time"]
        if data <= 0:  # Reject zero and negative
            raise forms.ValidationError("Proper time must be greater than zero")
        elif data > 1e9:
            raise forms.ValidationError("Time value is too large (max 1e9 seconds)")
        return data

    def clean_object_key(self):
        data = self.cleaned_data["object_key"]
        if data not in GRAVITATIONAL_OBJECTS:
            raise forms.ValidationError("Invalid object selection")
        return data

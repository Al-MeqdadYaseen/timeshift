from django import forms


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

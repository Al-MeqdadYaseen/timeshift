from django import forms


class CalculationForm(forms.Form):
    velocity = forms.FloatField(
        label="Velocity (fraction of c)",
        min_value=0.0,
        max_value=0.999999,  # UI cap to avoid extreme gamma values
    )
    proper_time = forms.FloatField(label="Proper time (seconds)", min_value=0.0)

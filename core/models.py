from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class Calculation(models.Model):
    velocity = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(0.9999999999)]
    )  # Fraction of c (0.0 to 1.0)
    proper_time = models.FloatField(validators=[MinValueValidator(0.0)])  # Seconds
    gamma = models.FloatField(null=False, blank=False)
    dilated_time = models.FloatField(null=False, blank=False)  # Seconds
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.velocity >= 1.0:
            raise ValidationError({"velocity": "Must be < 1 (speed of light)."})

    def __str__(self):
        return f"Calc t= {self.proper_time} seconds, v = {self.velocity}c"

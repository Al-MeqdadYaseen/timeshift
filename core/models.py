from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class Calculation(models.Model):
    CALCULATION_TYPE = [
        ("relativistic", "Special Relativity"),
        ("gravitational", "Gravitational time dilation"),
    ]

    calculation_type = models.CharField(
        max_length=20, choices=CALCULATION_TYPE, default="relativistic"
    )

    def validate_v(value):
        if not 0 < value < 1:
            raise ValidationError("Velocity must be between 0 and 1 (fraction of c)")

    velocity = models.FloatField(validators=[validate_v])  # Fraction of c (0.0 to 1.0)
    proper_time = models.FloatField(validators=[MinValueValidator(0.0)])  # Seconds
    gamma = models.FloatField(null=True, blank=True)
    dilated_time = models.FloatField(null=False, blank=False)  # Seconds
    gravitational_factor = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True,
        blank=True,  # Only if gravitational
    )
    object_key = models.CharField(
        max_length=50, null=True, blank=True
    )  # Which preset used
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calc t={self.proper_time}seconds, v ={self.velocity:.3f}c"

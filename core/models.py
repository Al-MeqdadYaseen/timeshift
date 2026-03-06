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
        ("relativistic", "Relativistic time dilation"),
        ("gravitational", "Gravitational time dilation"),
    ]

    calculation_type = models.CharField(
        max_length=20, choices=CALCULATION_TYPE, db_index=True
    )

    # Common Fields
    proper_time = models.FloatField(validators=[MinValueValidator(0.0)])  # Seconds
    dilated_time = models.FloatField()  # Seconds
    created_at = models.DateTimeField(auto_now_add=True)

    # Special relativity fields
    def validate_v(value):
        if not 0 < value < 1:
            raise ValidationError("Velocity must be between 0 and 1 (fraction of c)")

    velocity = models.FloatField(
        validators=[validate_v], null=True, blank=True
    )  # Fraction of c (0.0 to 1.0)
    gamma = models.FloatField(null=True, blank=True)

    # Gravitational fields
    gravitational_factor = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True,
        blank=True,  # Only if gravitational
    )
    object_key = models.CharField(
        max_length=50, null=True, blank=True
    )  # Which preset used
    object_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.calculation_type == "relativistic":
            return f"Relativistic: v={self.velocity:.3f}c, t={self.proper_time}"
        else:
            return f"Gravitational: {self.object_name}, t={self.proper_time}"


# AI helped me here with some validation and design the model to save both relativistic and gravitational calculations

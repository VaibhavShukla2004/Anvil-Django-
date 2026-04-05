from django.db import models
import uuid
from django.contrib.auth.models import User

class Workout(models.Model):

    TYPE_CHOICES = [
        ("hypertrophy", "Hypertrophy"),
        ("strength", "Strength"),
        ("endurance", "Endurance"),
        ("balanced", "Balanced"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)

    is_premade = models.BooleanField(default=False)

    # store exercise IDs (simple, fast, no join needed)
    exercise_ids = models.JSONField()

    muscle_groups = models.JSONField()

    equipment = models.JSONField()

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    total_fatigue = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
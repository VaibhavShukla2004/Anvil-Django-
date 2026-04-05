from django.db import models


class Exercise(models.Model):

    TYPE_CHOICES = [
        ("compound", "Compound"),
        ("isolation", "Isolation"),
    ]

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    name = models.CharField(max_length=255)

    # muscle → weight mapping
    muscle_weights = models.JSONField()

    # quick lookup
    primary_muscles = models.JSONField()

    # ["dumbbell", "barbell"]
    equipment = models.JSONField()

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # push / pull / hinge / squat / isolation
    pattern = models.CharField(max_length=50)

    # 0 → 1 scale
    fatigue = models.FloatField()

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)

    image_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
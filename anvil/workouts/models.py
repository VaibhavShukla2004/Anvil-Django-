from django.db import models
from exercises.models import Exercise


class Workout(models.Model):
    name = models.CharField(max_length=255)

    exercises = models.ManyToManyField(Exercise, related_name='workouts')

    equipment = models.JSONField(default=list)       # derived
    muscle_groups = models.JSONField(default=list)   # derived

    no_of_exercises = models.IntegerField(default=0) # derived
    is_premade = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def update_derived_fields(self):
        exercises = self.exercises.all()
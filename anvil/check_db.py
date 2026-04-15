import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anvil.settings')
django.setup()

from workout.models import Workout
from exercise.models import Exercise

workouts = Workout.objects.all()
for w in workouts:
    print(w.name, w.exercise_ids)

print("Mapping:")
for e in Exercise.objects.all():
    print(e.id, e.name)


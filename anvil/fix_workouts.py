import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anvil.settings')
django.setup()

from workout.models import Workout
from exercise.models import Exercise

workouts = Workout.objects.all()

for w in workouts:
    new_ids = []
    for old_id in w.exercise_ids:
        if old_id < 50:
            new_ids.append(old_id + 52)
        else:
            new_ids.append(old_id)
    w.exercise_ids = new_ids
    w.save()
    
print('Workout exercise IDs updated successfully.')

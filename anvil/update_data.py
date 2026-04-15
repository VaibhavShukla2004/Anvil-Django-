import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anvil.settings')
django.setup()

from exercise.models import Exercise

with open('../data/exercises.json', 'r') as f:
    exercises = json.load(f)

Exercise.objects.all().delete()

for ex in exercises:
    Exercise.objects.create(
        name=ex['name'],
        primary_muscles=ex.get('primary_muscles', []),
        muscle_weights=ex.get('muscle_weights', {}),
        equipment=ex.get('equipment', []),
        type=ex.get('type', ''),
        pattern=ex.get('pattern', ''),
        fatigue=ex.get('fatigue', 0.0),
        difficulty=ex.get('difficulty', ''),
        image_url=ex.get('image_url', '')
    )
print('Exercises re-loaded successfully (table cleared and seeded).')

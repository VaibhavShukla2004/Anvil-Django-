import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anvil.settings')
django.setup()

from workout.models import Workout

# Clear all premade workouts that have stale exercise IDs
deleted, _ = Workout.objects.filter(is_premade=True).delete()
print(f'Deleted {deleted} premade workout(s) with stale exercise IDs.')

remaining = Workout.objects.all().count()
print(f'Remaining workouts in DB: {remaining}')

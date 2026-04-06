from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from exercise.models import Exercise
from workout.models import Workout


class Command(BaseCommand):
    help = "Seed initial data"

    def handle(self, *args, **kwargs):

        # ---------------- ADMIN ----------------
        if not User.objects.filter(username="admin").exists():
            user = User.objects.create_user(
                username="admin",
                email="admin@test.com",
                password="1234"
            )
            user.userprofile.role = "ADMIN"
            user.userprofile.save()
            self.stdout.write("Admin created")
        else:
            self.stdout.write("Admin already exists")


        # ---------------- EXERCISES ----------------
        if Exercise.objects.count() == 0:
            Exercise.objects.create(
                name="Pull Up",
                muscle_weights={"back": 1.0},
                primary_muscles=["back"],
                equipment=["bar"],
                type="compound",
                pattern="pull",
                fatigue=0.7,
                difficulty="intermediate",
                image_url=""
            )
            self.stdout.write("Exercises seeded")
        else:
            self.stdout.write("Exercises already exist")


        # ---------------- PREMADE WORKOUT ----------------
        if Workout.objects.filter(is_premade=True).count() == 0:
            Workout.objects.create(
                user=None,
                name="Back Starter",
                is_premade=True,
                exercise_ids=[1],
                muscle_groups=["back"],
                equipment=[],
                type="balanced",
                total_fatigue=1.0
            )
            self.stdout.write("Premade workouts seeded")
        else:
            self.stdout.write("Premade workouts already exist")
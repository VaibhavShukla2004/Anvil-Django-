from rest_framework.decorators import api_view
from rest_framework.response import Response

from exercise.models import Exercise

from exercise.models import Exercise
from .models import Workout
from .serializers import WorkoutSerializer


# GET all
@api_view(['GET'])
def get_all_workouts(request):
    qs = Workout.objects.all()
    return Response(WorkoutSerializer(qs, many=True).data)


# GET by id
@api_view(['GET'])
def get_workout_by_id(request, id):
    try:
        w = Workout.objects.get(id=id)
        return Response(WorkoutSerializer(w).data)
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# GET by name
@api_view(['GET'])
def get_workout_by_name(request):
    name = request.GET.get('name')
    qs = Workout.objects.filter(name__icontains=name)
    return Response(WorkoutSerializer(qs, many=True).data)


# GET premade
@api_view(['GET'])
def get_premade_workouts(request):
    qs = Workout.objects.filter(is_premade=True)
    return Response(WorkoutSerializer(qs, many=True).data)


# GET user-made
@api_view(['GET'])
def get_user_workouts(request):
    qs = Workout.objects.filter(is_premade=False)
    return Response(WorkoutSerializer(qs, many=True).data)


# POST single
@api_view(['POST'])
def add_workout(request):
    serializer = WorkoutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# POST bulk
@api_view(['POST'])
def add_workout_bulk(request):
    serializer = WorkoutSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

#GENERATE workout
@api_view(['POST'])
def generate_workout(request):

    # INPUT
    muscle_groups = request.data.get("muscle_groups", [])
    equipment = request.data.get("equipment", [])
    N = request.data.get("num_exercises", 5)

    # STEP 1 — FILTER
    exercises = Exercise.objects.all()

    if muscle_groups:
        exercises = [
            e for e in exercises
            if any(m in e.primary_muscles for m in muscle_groups)
        ]

    if equipment:
        exercises = [
            e for e in exercises
            if all(eq in e.equipment or not e.equipment for eq in equipment)
        ]

    # STEP 2 — INIT
    M = muscle_groups
    T = N / len(M) if M else 1

    S = {m: 0 for m in M}
    pattern_count = {}
    selected = []

    FATIGUE_MAX = 5
    total_fatigue = 0

    # STEP 3 — GREEDY LOOP
    while len(selected) < N and exercises:

        best = None
        best_score = float('-inf')

        for e in exercises:

            if e in selected:
                continue

            # primary constraint
            if not any(e.muscle_weights.get(m, 0) >= 0.5 for m in M):
                continue

            score = 0

            for m in M:
                score += e.muscle_weights.get(m, 0) * (T - S[m])

            # pattern penalty
            if pattern_count.get(e.pattern, 0) >= 2:
                score -= 1

            # fatigue penalty
            score -= e.fatigue * 0.5

            if score > best_score:
                best_score = score
                best = e

        if not best:
            break

        # fatigue check
        if total_fatigue + best.fatigue > FATIGUE_MAX:
            break

        # ADD
        selected.append(best)
        total_fatigue += best.fatigue

        for m in M:
            S[m] += best.muscle_weights.get(m, 0)

        pattern_count[best.pattern] = pattern_count.get(best.pattern, 0) + 1

    # STEP 4 — BUILD RESPONSE
    exercise_ids = [e.id for e in selected]

    workout = Workout.objects.create(
        name="Generated Workout",
        is_premade=False,
        exercise_ids=exercise_ids,
        muscle_groups=muscle_groups,
        equipment=equipment,
        type="balanced",
        total_fatigue=total_fatigue
    )

    return Response(WorkoutSerializer(workout).data)

# PUT update
@api_view(['PUT'])
def update_workout(request, id):
    try:
        w = Workout.objects.get(id=id)
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    serializer = WorkoutSerializer(w, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# DELETE single
@api_view(['DELETE'])
def delete_workout(request, id):
    try:
        w = Workout.objects.get(id=id)
        w.delete()
        return Response({"message": "deleted"})
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# DELETE bulk
@api_view(['DELETE'])
def delete_workout_bulk(request):
    ids = request.data.get("ids", [])

    count, _ = Workout.objects.filter(id__in=ids).delete()
    return Response({"deleted": count})
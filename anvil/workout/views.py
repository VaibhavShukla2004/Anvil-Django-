from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q

from exercise.models import Exercise
from .models import Workout
from .serializers import WorkoutSerializer


# 🔹 Helper
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "ADMIN"


# ------------------- GET -------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_workouts(request):
    if request.user.is_authenticated:
        qs = Workout.objects.filter(Q(user=request.user) | Q(is_premade=True))
    else:
        qs = Workout.objects.filter(is_premade=True)

    return Response(WorkoutSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_workout_by_id(request, id):
    try:
        w = Workout.objects.get(id=id)
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if w.is_premade:
        return Response(WorkoutSerializer(w).data)

    if not request.user.is_authenticated:
        return Response({"error": "Unauthorized"}, status=401)

    if w.user != request.user:
        return Response({"error": "Forbidden"}, status=403)

    return Response(WorkoutSerializer(w).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_workout_by_name(request):
    name = request.GET.get('name', '')
    qs = Workout.objects.filter(name__icontains=name)

    if request.user.is_authenticated:
        qs = qs.filter(Q(user=request.user) | Q(is_premade=True))
    else:
        qs = qs.filter(is_premade=True)

    return Response(WorkoutSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_premade_workouts(request):
    qs = Workout.objects.filter(is_premade=True)
    return Response(WorkoutSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_workouts(request):
    qs = Workout.objects.filter(user=request.user, is_premade=False)
    return Response(WorkoutSerializer(qs, many=True).data)


# ------------------- GENERATE -------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_workout(request):

    muscle_groups = request.data.get("muscle_groups", [])
    equipment = request.data.get("equipment", [])
    N = request.data.get("num_exercises", 5)

    exercises = Exercise.objects.all()

    if muscle_groups:
        exercises = [e for e in exercises if any(m in e.primary_muscles for m in muscle_groups)]

    if equipment:
        exercises = [e for e in exercises if all(eq in e.equipment or not e.equipment for eq in equipment)]

    M = muscle_groups
    T = N / len(M) if M else 1

    S = {m: 0 for m in M}
    pattern_count = {}
    selected = []

    FATIGUE_MAX = 5
    total_fatigue = 0

    while len(selected) < N and exercises:

        best = None
        best_score = float('-inf')

        for e in exercises:

            if e in selected:
                continue

            if not any(e.muscle_weights.get(m, 0) >= 0.5 for m in M):
                continue

            score = 0

            for m in M:
                score += e.muscle_weights.get(m, 0) * (T - S[m])

            if pattern_count.get(e.pattern, 0) >= 2:
                score -= 1

            score -= e.fatigue * 0.5

            if score > best_score:
                best_score = score
                best = e

        if not best:
            break

        if total_fatigue + best.fatigue > FATIGUE_MAX:
            break

        selected.append(best)
        total_fatigue += best.fatigue

        for m in M:
            S[m] += best.muscle_weights.get(m, 0)

        pattern_count[best.pattern] = pattern_count.get(best.pattern, 0) + 1

    exercise_ids = [e.id for e in selected]

    # 🔥 KEY LOGIC
    if request.user.is_authenticated:

        if Workout.objects.filter(user=request.user).count() >= 10:
            return Response({"error": "Workout limit reached"}, status=400)

        workout = Workout.objects.create(
            user=request.user,
            name="Generated Workout",
            is_premade=False,
            exercise_ids=exercise_ids,
            muscle_groups=muscle_groups,
            equipment=equipment,
            type="balanced",
            total_fatigue=total_fatigue
        )

        return Response(WorkoutSerializer(workout).data)

    # guest
    return Response({
        "name": "Generated Workout",
        "exercise_ids": exercise_ids,
        "muscle_groups": muscle_groups,
        "equipment": equipment,
        "type": "balanced",
        "total_fatigue": total_fatigue
    })


# ------------------- UPDATE -------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_workout(request, id):

    try:
        w = Workout.objects.get(id=id)
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    # ❌ block premade edits
    if w.is_premade:
        return Response({"error": "Cannot update premade workout"}, status=403)

    if w.user != request.user:
        return Response({"error": "Forbidden"}, status=403)

    serializer = WorkoutSerializer(w, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# ------------------- DELETE -------------------

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_workout(request, id):

    try:
        w = Workout.objects.get(id=id)
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if w.is_premade:
        return Response({"error": "Cannot delete premade workout"}, status=403)

    if w.user != request.user:
        return Response({"error": "Forbidden"}, status=403)

    w.delete()
    return Response({"message": "deleted"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_workout_bulk(request):

    ids = request.data.get("ids", [])

    qs = Workout.objects.filter(
        id__in=ids,
        user=request.user,
        is_premade=False
    )

    count = qs.count()
    qs.delete()

    return Response({"deleted": count})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_premade_workout(request):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    data = request.data.copy()
    data["is_premade"] = True
    data["user"] = None  # premade has no owner

    serializer = WorkoutSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_premade_workout_bulk(request):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    data = request.data

    for item in data:
        item["is_premade"] = True
        item["user"] = None

    serializer = WorkoutSerializer(data=data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_premade_workouts(request):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    ids = request.data.get("ids", [])

    qs = Workout.objects.filter(id__in=ids, is_premade=True)

    count = qs.count()
    qs.delete()

    return Response({"deleted": count})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_premade_workout(request, id):

    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    try:
        w = Workout.objects.get(id=id, is_premade=True)
    except Workout.DoesNotExist:
        return Response({"error": "Premade workout not found"}, status=404)

    serializer = WorkoutSerializer(w, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

from django.shortcuts import render
def workouts_page(request):
    """Renders the HTML template for the workouts list"""
    return render(request, "workouts_page.html")

def generated_page(request):
    """Renders the HTML template for the generated workout output"""
    return render(request, "generated_workout.html")

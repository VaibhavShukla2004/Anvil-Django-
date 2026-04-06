from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Exercise
from .serializers import ExerciseSerializer


# 🔹 Helper (ADMIN check)
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "ADMIN"


# ------------------- GET (PUBLIC) -------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_exercises(request):
    qs = Exercise.objects.all()
    return Response(ExerciseSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exercise_by_id(request, id):
    try:
        ex = Exercise.objects.get(id=id)
        return Response(ExerciseSerializer(ex).data)
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exercise_by_name(request):
    name = request.GET.get('name')
    qs = Exercise.objects.filter(name__icontains=name)
    return Response(ExerciseSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exercise_by_muscle(request):
    muscle = request.GET.get('muscle')
    qs = Exercise.objects.filter(primary_muscles__contains=[muscle])
    return Response(ExerciseSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exercise_by_equipment(request):
    eq = request.GET.get('equipment')
    qs = Exercise.objects.filter(equipment__contains=[eq])
    return Response(ExerciseSerializer(qs, many=True).data)


# ------------------- ADMIN ONLY -------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_exercise(request):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_exercise_bulk(request):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    serializer = ExerciseSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_exercise(request, id):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    try:
        ex = Exercise.objects.get(id=id)
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    serializer = ExerciseSerializer(ex, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_exercise_by_id(request, id):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    try:
        ex = Exercise.objects.get(id=id)
        ex.delete()
        return Response({"message": "deleted"})
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_exercise_by_name(request):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    name = request.GET.get('name')
    count, _ = Exercise.objects.filter(name__icontains=name).delete()
    return Response({"deleted": count})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_exercise_bulk(request):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    ids = request.data.get("ids", [])
    names = request.data.get("names", [])

    deleted = 0

    if ids:
        c, _ = Exercise.objects.filter(id__in=ids).delete()
        deleted += c

    if names:
        c, _ = Exercise.objects.filter(name__in=names).delete()
        deleted += c

    return Response({"deleted": deleted})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_by_muscle(request):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    muscle = request.GET.get('muscle')
    count, _ = Exercise.objects.filter(primary_muscles__contains=[muscle]).delete()
    return Response({"deleted": count})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_by_equipment(request):
    if not is_admin(request.user):
        return Response({"error": "Admin only"}, status=403)

    eq = request.GET.get('equipment')
    count, _ = Exercise.objects.filter(equipment__contains=[eq]).delete()
    return Response({"deleted": count})

from django.shortcuts import render

def exercises_page(request):
    return render(request, "exercises.html")
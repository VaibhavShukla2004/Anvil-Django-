from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Exercise
from .serializers import ExerciseSerializer


# GET /exercises/
@api_view(['GET'])
def get_all_exercises(request):
    exercises = Exercise.objects.all()
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data)


# GET /exercises/{id}/
@api_view(['GET'])
def get_exercise_by_id(request, id):
    try:
        exercise = Exercise.objects.get(id=id)
        serializer = ExerciseSerializer(exercise)
        return Response(serializer.data)
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# GET /exercises/by-name/?name=
@api_view(['GET'])
def get_exercise_by_name(request):
    name = request.GET.get('name')
    exercises = Exercise.objects.filter(name__icontains=name)
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data)


# GET /exercises/by-muscle-group/?muscle_group=
@api_view(['GET'])
def get_by_muscle_group(request):
    mg = request.GET.get('muscle_group')
    exercises = Exercise.objects.filter(muscle_group__iexact=mg)
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data)


# GET /exercises/by-equipment/?equipment=
@api_view(['GET'])
def get_by_equipment(request):
    eq = request.GET.get('equipment')
    exercises = Exercise.objects.filter(equipment__contains=[eq])
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data)


# GET /exercises/count/
@api_view(['GET'])
def count_exercises(request):
    count = Exercise.objects.count()
    return Response({"count": count})


# POST /exercises/
@api_view(['POST'])
def add_exercise(request):
    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# DELETE /exercises/{id}/
@api_view(['DELETE'])
def delete_by_id(request, id):
    try:
        exercise = Exercise.objects.get(id=id)
        exercise.delete()
        return Response({"message": "Deleted"})
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# DELETE /exercises/by-name/?name=
@api_view(['DELETE'])
def delete_by_name(request):
    name = request.GET.get('name')
    count, _ = Exercise.objects.filter(name__icontains=name).delete()
    return Response({"deleted": count})


# DELETE /exercises/by-muscle-group/?muscle_group=
@api_view(['DELETE'])
def delete_by_muscle_group(request):
    mg = request.GET.get('muscle_group')
    count, _ = Exercise.objects.filter(muscle_group__iexact=mg).delete()
    return Response({"deleted": count})


# DELETE /exercises/by-equipment/?equipment=
@api_view(['DELETE'])
def delete_by_equipment(request):
    eq = request.GET.get('equipment')
    count, _ = Exercise.objects.filter(equipment__contains=[eq]).delete()
    return Response({"deleted": count})
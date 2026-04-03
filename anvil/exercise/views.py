from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Exercise
from .serializers import ExerciseSerializer

#get all
@api_view(['GET'])
def get_all_exercises(request):
    qs = Exercise.objects.all()
    return Response(ExerciseSerializer(qs, many=True).data)

# GET by ID
@api_view(['GET'])
def get_exercise_by_id(request, id):
    try:
        ex = Exercise.objects.get(id=id)
        return Response(ExerciseSerializer(ex).data)
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# GET by name
@api_view(['GET'])
def get_exercise_by_name(request):
    name = request.GET.get('name')
    qs = Exercise.objects.filter(name__icontains=name)
    return Response(ExerciseSerializer(qs, many=True).data)


# GET by muscle (checks primary_muscles)
@api_view(['GET'])
def get_exercise_by_muscle(request):
    muscle = request.GET.get('muscle')
    qs = Exercise.objects.filter(primary_muscles__contains=[muscle])
    return Response(ExerciseSerializer(qs, many=True).data)


# GET by equipment
@api_view(['GET'])
def get_exercise_by_equipment(request):
    eq = request.GET.get('equipment')
    qs = Exercise.objects.filter(equipment__contains=[eq])
    return Response(ExerciseSerializer(qs, many=True).data)


# POST add single
@api_view(['POST'])
def add_exercise(request):
    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# POST bulk add
@api_view(['POST'])
def add_exercise_bulk(request):
    serializer = ExerciseSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# PUT update
@api_view(['PUT'])
def update_exercise(request, id):
    try:
        ex = Exercise.objects.get(id=id)
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    serializer = ExerciseSerializer(ex, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# DELETE by id
@api_view(['DELETE'])
def delete_exercise_by_id(request, id):
    try:
        ex = Exercise.objects.get(id=id)
        ex.delete()
        return Response({"message": "deleted"})
    except Exercise.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# DELETE by name
@api_view(['DELETE'])
def delete_exercise_by_name(request):
    name = request.GET.get('name')
    count, _ = Exercise.objects.filter(name__icontains=name).delete()
    return Response({"deleted": count})


# DELETE bulk (ids or names)
@api_view(['DELETE'])
def delete_exercise_bulk(request):
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


# DELETE by muscle
@api_view(['DELETE'])
def delete_by_muscle(request):
    muscle = request.GET.get('muscle')
    count, _ = Exercise.objects.filter(primary_muscles__contains=[muscle]).delete()
    return Response({"deleted": count})


# DELETE by equipment
@api_view(['DELETE'])
def delete_by_equipment(request):
    eq = request.GET.get('equipment')
    count, _ = Exercise.objects.filter(equipment__contains=[eq]).delete()
    return Response({"deleted": count})
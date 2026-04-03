from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Workout
from .serializers import WorkoutSerializer
# Create your views here.
#Workout Methods

@api_view(['GET'])
def get_workouts(request):
    qs = Workout.objects.all()

    name = request.GET.get('name')
    muscle = request.GET.get('muscle_group')
    equipment = request.GET.get('equipment')

    if name:
        qs = qs.filter(name__icontains=name)

    if muscle:
        qs = qs.filter(muscle_groups__contains=[muscle])

    if equipment:
        qs = qs.filter(equipment__contains=[equipment])

    return Response(WorkoutSerializer(qs, many=True).data)

@api_view(['GET'])
def get_workout_by_id(request, id):
    try:
        w = Workout.objects.get(id=id)
        return Response(WorkoutSerializer(w).data)
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    
@api_view(['POST'])
def create_workout(request):
    serializer = WorkoutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def bulk_create_workouts(request):
    serializer = WorkoutSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_workout(request, id):
    try:
        w = Workout.objects.get(id=id)
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    serializer = WorkoutSerializer(w, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_workout_by_id(request, id):
    try:
        w = Workout.objects.get(id=id)
        w.delete()
        return Response({"message": "Deleted"})
    except Workout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    

@api_view(['DELETE'])
def delete_workout_by_name(request):
    name = request.GET.get('name')
    count, _ = Workout.objects.filter(name__icontains=name).delete()
    return Response({"deleted": count})


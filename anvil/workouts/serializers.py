
from rest_framework import serializers
from .models import Workout
from exercises.models import Exercise

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        many=True
    )

    class Meta:
        model = Workout
        fields = '__all__'

    def create(self, validated_data):
        exercises = validated_data.pop('exercises')
        workout = Workout.objects.create(**validated_data)
        workout.exercises.set(exercises)
        workout.update_derived_fields()
        workout.save()
        return workout

    def update(self, instance, validated_data):
        exercises = validated_data.pop('exercises', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if exercises is not None:
            instance.exercises.set(exercises)

        instance.update_derived_fields()
        instance.save()

        return instance

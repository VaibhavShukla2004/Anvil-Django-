from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_workouts),
    path('bulk/', views.bulk_create_workouts),

    path('<int:id>/', views.get_workout_by_id),
    path('create/', views.create_workout),
    path('update/<int:id>/', views.update_workout),

    path('delete/<int:id>/', views.delete_workout_by_id),
    path('delete/', views.delete_workout_by_name),
]
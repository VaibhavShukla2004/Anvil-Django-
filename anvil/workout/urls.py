from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_workouts),

    path('<uuid:id>/', views.get_workout_by_id),

    path('by-name/', views.get_workout_by_name),
    path('premade/', views.get_premade_workouts),
    path('user/', views.get_user_workouts),

    path('add/', views.add_workout),
    path('add-bulk/', views.add_workout_bulk),

    path('update/<uuid:id>/', views.update_workout),

    path('delete/<uuid:id>/', views.delete_workout),
    path('delete/bulk/', views.delete_workout_bulk),
    path('generate/', views.generate_workout),
]
from django.urls import path
from . import views

urlpatterns = [
    # GET
    path('', views.get_all_workouts),
    path('<uuid:id>/', views.get_workout_by_id),
    path('by-name/', views.get_workout_by_name),
    path('premade/', views.get_premade_workouts),
    path('user/', views.get_user_workouts),

    # GENERATE
    path('generate/', views.generate_workout),

    # MUTATION
    path('update/<uuid:id>/', views.update_workout),
    path('delete/<uuid:id>/', views.delete_workout),
    path('delete/bulk/', views.delete_workout_bulk),

    # ADMIN premade
    path('premade/add/', views.create_premade_workout),
    path('premade/add-bulk/', views.create_premade_workout_bulk),
    path('premade/update/<uuid:id>/', views.update_premade_workout),
    path('premade/delete/', views.delete_premade_workouts),
]
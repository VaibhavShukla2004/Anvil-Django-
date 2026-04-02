from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_exercises),
    path('count/', views.count_exercises),
    path('<int:id>/', views.get_exercise_by_id),

    path('by-name/', views.get_exercise_by_name),
    path('by-muscle-group/', views.get_by_muscle_group),
    path('by-equipment/', views.get_by_equipment),

    path('add/', views.add_exercise),

    path('delete/<int:id>/', views.delete_by_id),
    path('delete/by-name/', views.delete_by_name),
    path('delete/by-muscle-group/', views.delete_by_muscle_group),
    path('delete/by-equipment/', views.delete_by_equipment),
]
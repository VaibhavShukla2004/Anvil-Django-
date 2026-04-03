from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_exercises),
    path('<int:id>/', views.get_exercise_by_id),

    path('by-name/', views.get_exercise_by_name),
    path('by-muscle/', views.get_exercise_by_muscle),
    path('by-equipment/', views.get_exercise_by_equipment),

    path('add/', views.add_exercise),
    path('add-bulk/', views.add_exercise_bulk),

    path('update/<int:id>/', views.update_exercise),

    path('delete/<int:id>/', views.delete_exercise_by_id),
    path('delete/by-name/', views.delete_exercise_by_name),
    path('delete/bulk/', views.delete_exercise_bulk),
    path('delete/by-muscle/', views.delete_by_muscle),
    path('delete/by-equipment/', views.delete_by_equipment),
]
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from exercise.views import exercises_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercise/', include('exercise.urls')),
    path('workout/', include('workout.urls')),
    path('auth/', include('users.urls')),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('exercises/', exercises_page),  # For the exercises page
]
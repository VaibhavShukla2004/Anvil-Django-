from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercise/', include('exercise.urls')),
    path('workout/', include('workout.urls')),
]
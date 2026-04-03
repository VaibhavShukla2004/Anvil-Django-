from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercises/', include('exercises.urls')),
    path('workouts/', include('workouts.urls')),
]
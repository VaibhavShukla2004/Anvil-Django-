from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercise/', include('exercise.urls', namespace='exercise')),
    path('', views.home, name='home'),
    path('workout/', include('workout.urls')),
    path('auth/', include('users.urls')),
    path('auth/refresh/', TokenRefreshView.as_view()), # For the exercises page
    path('selection/', views.selection_page, name='selection')
]
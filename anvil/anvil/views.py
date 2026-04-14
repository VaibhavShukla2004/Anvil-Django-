from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import render

def home(request):
    return render(request, "main.html")

def selection_page(request):
    return render(request, "selection.html")
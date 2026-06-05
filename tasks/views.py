from django.shortcuts import render

from django.http import JsonResponse
from rest_framework import viewsets
from .models import Task
from .serializer import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


def health_check(request):
    return JsonResponse({
        "status": "healthy"
    })

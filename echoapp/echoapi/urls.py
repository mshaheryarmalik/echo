# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get_emad/', views.get_emad),
]

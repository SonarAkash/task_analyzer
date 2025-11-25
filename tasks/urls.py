from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('api/tasks/analyze/', views.analyze_tasks, name='analyze_tasks'),
]
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('history/', views.history_view, name='history'),
    path('api/predict/', views.api_predict, name='api_predict'),
]
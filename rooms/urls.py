from rest_framework.routers import  DefaultRouter
from django.urls import path
from rooms import views
from . import viewsets

app_name = "rooms"

urlpatterns = [
    path('', views.RoomsView.as_view()),
    path('<int:pk>/', views.RoomView.as_view()),
]

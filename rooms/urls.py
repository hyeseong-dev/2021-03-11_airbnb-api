from django.urls import path
from rooms import views


app_name = "rooms"

urlpatterns = [
    path('list/', views.ListRoomsView.as_view()),
]

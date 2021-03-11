from django.urls import path
from rooms import views


app_name = "rooms"

urlpatterns = [
    path('list/', views.ListRoomsView.as_view()),
    # path('<int:pkk>/', views.SeeRoomView.as_view()), # views.py 파일에 lookup_url_kwarg 클래스 변수 설정이 필요함
    path('<int:pk>/', views.SeeRoomView.as_view()),
]

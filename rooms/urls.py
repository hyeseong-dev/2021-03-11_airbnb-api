from rest_framework.routers import  DefaultRouter
from django.urls import path
from rooms import views
from . import viewsets

app_name = "rooms"

# router = DefaultRouter()
# router.register(r'', viewsets.RoomViewSet, basename='room')


# urlpatterns = router.urls


# ListAPIView, RetrieveAPIView 사용시 기존 장고에서 사용하던 대로 url을 정의하여 사용함.
urlpatterns = [
    path('list/', views.ListRoomsView.as_view()),
    # path('<int:pkk>/', views.SeeRoomView.as_view()), # views.py 파일에 lookup_url_kwarg 클래스 변수 설정이 필요함
    path('<int:pk>/', views.SeeRoomView.as_view()),
]

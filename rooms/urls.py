# from django.urls import path # router 기능을 이용하면  path()는 필요없음
from rest_framework.routers import DefaultRouter
from rooms import views

app_name = "rooms"

router = DefaultRouter()
router.register('',views.RoomViewSet)


urlpatterns = router.urls

# urlpatterns = [
#     path('', views.RoomsView.as_view()),
#     path('search', views.room_search),
#     path('<int:pk>/', views.RoomView.as_view()),
# ]

from rest_framework import status
from rest_framework.generics import RetrieveAPIView#, ListAPIView,
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


# class ListRoomsView(ListAPIView): FBV구현을 위해 
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user) # 여기서 받은 룸은 create 메소드에서 반환한 인스턴스를 말함
            room_serializer = ReadRoomSerializer(room).data # 알맹이에 해당함. HTTP 메서드에서 바디로 보낸 값들과 기타등등
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer
    # lookup_url_kwarg = 'pkk' 이렇게 하면 url의 인자 이름을 내가 원하는대로 지정할 수 있음.



#     {
#     "name": "Beautiful Room",
#     "address": "Cra 1124",
#     "prices": 10,
#     "beds": 5,
#     "lat": 12,
#     "lng": 12,
#     "bedrooms": 2,
#     "bathrooms": 2,
#     "check_in": "14:00",
#     "check_out": "12:00",
#     "instant_book": false
# }
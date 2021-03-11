from rest_framework.generics import RetrieveAPIView#, ListAPIView,
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


# class ListRoomsView(ListAPIView): FBV구현을 위해 
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

@api_view(http_method_names=['GET','POST'])
def rooms_view(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == 'POST':
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_201_CREATED) 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 



class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer
    # lookup_url_kwarg = 'pkk' 이렇게 하면 url의 인자 이름을 내가 원하는대로 지정할 수 있음.

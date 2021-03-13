from rest_framework.views import APIView
from rest_framework import status
from rooms.serializers import RoomSerializer
from users.serializers import ReadUserSerializer, WriteUserSerializer
from rooms.models import Room
from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated #  인증한 유저만 해당 메소드에 접근 가능하도록함.
from rest_framework.decorators import api_view



class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReadUserSerializer(request.user).data)
    
    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response() # 인자로 아무것을 주지 않으면 기본값은 stats.HTTP_200_OK를 갖고 있는 거임
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQEUST)

@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, request): # user의 favs필드의 상태를 업데이트 하기에 post가 아님
        pk = request.data.get('pk',None)
        user = request.user # request.user 속성에 ORM 객체 인스턴스가 값으로 참조 하고 있다는 사실
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                   user.favs.remove(room) # orm을 통해서 객체간의 연결을 해체
                else:
                    user.favs.add(room)   # 1:N 관계를 orm을 통해서 연결함
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST) 
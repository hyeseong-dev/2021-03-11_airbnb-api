from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


class RoomsView(APIView): # collections로 던져줌
    def get(self, request):
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated: # 분기1: 로그인 여부 확인
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():            # 분기2 : 유효성 검사 body로 받은 값들과 serializer에서 정의된 필드 형식과 변수명이 맞는지 확인
            room = serializer.save(user=request.user) # 여기서 받은 룸은 create 메소드에서 반환한 인스턴스를 말함
            room_serializer = ReadRoomSerializer(room).data # 알맹이에 해당함. HTTP 메서드에서 바디로 보낸 값들과 기타등등
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) # data키워드 인자는 오류도 받아서 던져주기도합니다.


class RoomView(APIView): # single로 처리
    def get(self, request, pk): # pk는 
        try:
            room = Room.objects.get(pk=pk)
            serializer = ReadRoomSerializer(room).data
            return Response(data=serializer)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        pass
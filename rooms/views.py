from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer


class OwnPagination(PageNumberPagination):
    page_size = 20


class RoomsView(APIView): # collections로 던져줌
    def get(self, request):
        paginator = OwnPagination()
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated: # 분기1: 로그인 여부 확인
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():            # 분기2 : 유효성 검사 body로 받은 값들과 serializer에서 정의된 필드 형식과 변수명이 맞는지 확인
            room = serializer.save(user=request.user) # 여기서 받은 룸은 create 메소드에서 반환한 인스턴스를 말함
            room_serializer = RoomSerializer(room).data # 알맹이에 해당함. HTTP 메서드에서 바디로 보낸 값들과 기타등등
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) # data키워드 인자는 오류도 받아서 던져주기도합니다.


class RoomView(APIView): # single로 처리
    def get_room(self, pk): # DB에 존재하면 긁어 오고 없으면 None반환, 일명 helper function
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None    

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:# room 객체가 정상적으로 DB에 있을 경우
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else: # Room 객체가 None에 해당할 경우
            return Response(status=status.HTTP_404_NOT_FOUND)
       
    def put(self, request, pk):
        room = self.get_room(pk) # get_room()메서드 정의시 첫번째 인자로 self로 받아서 인스턴스 속성으로 사용 가능
        if room is not None:
            if room.user != request.user: # url  parameter로 받아와 db에서 긁어온게 좌항  로그인한 유저의 정보가 우항
                return Response(status=status.HTTP_403_FORBIDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True) # partial 사용해서 기본적으로 required fields를 모두 넣지 않아도 오류를 발생 시키지 않게함
            if serializer.is_valid(): # db에 가져온 객체 정보와 클라이언트로부터 가져온 정보를 serializer와 비교했을때 유효한가?
                room = serializer.save()     # update() 메서드를 호출함.  객체 생성후 db에 저장함
                return Response(RoomSerializer(room).data) # statusz 키워드를 적어주지 않아도 기본값은 200이라서 생략 가능
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)
        else: # pk로 뒤져본 room이 디비에 없어요.
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk): # 3번째 인자는 urls.py에서 url 파라미터로 넘겨 받은 변수
        room = self.get_room(pk) # 헬퍼 함수를 통해서 room이 db에 있는지 혹은 None인지 반환
        if room is not None:     # 객체가 존재하고
            if room.user != request.user:  # 로그인한 유저가  객체의 user가 아니면(만든사람)
                return Response(status=status.HTTP_403_FORBIDDEN) # 403 오류를 뱉어내고
            room.delete()   # room.user == request.user 동일하면 delete()메소드를 사용해서 db에서 지워버림
            return Response(status=status.HTTP_200_OK) # 정상 삭제되었다는 200 코드를 반환함
        else:
            return Response(status=status.HTTP_404_NOT_FOUND) # pk를 이용해서 조회했지만 없는 경우 404오류를 Response클래스에 담아서 반환함.


@api_view(['GET'])
def room_search(request):
    max_price = request.GET.get('max_price',None)
    min_price = request.GET.get('min_price',None)
    beds = request.GET.get('beds',None)
    bedsrooms = request.GET.get('bedsrooms',None)
    bathrooms = request.GET.get('bathrooms',None)
    lat = request.GET.get('lat',None) # 위도 
    lng = request.GET.get('lng',None) # 경도
    filter_kwargs = {}

    if max_price is not None:
        filter_kwargs['price__lte'] = max_price
    if min_price is not None:
        filter_kwargs['price__gte'] = min_price
    if beds is not None:
        filter_kwargs['beds__gte'] = beds
    if bedsrooms is not None:
        filter_kwargs['bedsrooms__gte'] = bedsrooms
    if bathrooms is not None:
        filter_kwargs['bathrooms__gte'] = bathrooms
    if lat is not None and lng is not None: 
        filter_kwargs['lat__gte'] = float(lat) - 0.005
        filter_kwargs['lat__lte'] = float(lat) + 0.005
        filter_kwargs['lng__gte'] = float(lng) - 0.005
        filter_kwargs['lng__lte'] = float(lng) + 0.005

    paginator = OwnPagination()
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError: # value값이
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)
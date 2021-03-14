from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsOwner

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny] # 누구나 접근 가능
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated] # 로그인 한 누구나
        else:
            permission_classes = [IsOwner] # 해당 데이터를 생성한 주인만!
        return [permission() for permission in permission_classes]
        # called_perm = []
        # for p in permission_classes:
        #     print(p())
        #     print('='*100)
        #     called_perm.append(p())
        #     print(called_perm)
        # return called_perm

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
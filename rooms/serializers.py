from rest_framework import serializers
from users.serializers import TinyUserSerializer
from rooms.models import Room

class RoomSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = ('id', 'name', 'price', 'instant_book', 'user')


class BigRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__' # comma 붙이면 오류 발생, 아니면 exclude = () 이렇게 둬도 가능
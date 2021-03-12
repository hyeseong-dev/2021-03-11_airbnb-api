from rest_framework import serializers
from users.serializers import UserSerializer
from rooms.models import Room

class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ('modified',)

# class BigRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__' # comma 붙이면 오류 발생, 아니면 exclude = () 이렇게 둬도 가능

class WriteRoomSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=140)
    address =  serializers.CharField(max_length=140)
    price =  serializers.IntegerField()
    beds =  serializers.IntegerField(default=1)
    lat =  serializers.DecimalField(max_digits=10, decimal_places=6)
    lng =  serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms =  serializers.IntegerField(default=1)
    bathrooms =  serializers.IntegerField(default=1)
    check_in =  serializers.TimeField('00:00:00')
    check_out =  serializers.TimeField('00:00:00')
    instant_book =  serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Room.objects.create(**validated_data)
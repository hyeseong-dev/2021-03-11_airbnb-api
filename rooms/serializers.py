from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from rooms.models import Room

class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ('modified',)

# class BigRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__' # comma 붙이면 오류 발생, 아니면 exclude = () 이렇게 둬도 가능

class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model: Room
        exclude = ('user', 'modified', 'created')

    def validate(self, data): 
        if self.instance: # update 하는 경우, db에 pk로 값을 조회 했을때 반환받은 값이 있는 경우 
            check_in = data.get('check_in', self.instance.check_in)
            check_out = data.get('check_out', self.instance.check_out)
        else:             # create 하는 경우
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            if check_in == check_out:
                raise serializers.ValidationError('Not enough time between changes')
        return data
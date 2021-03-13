from rest_framework import serializers
from users.serializers import UserSerializer
from rooms.models import Room

class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ('modified',)
        read_only_fields = ('user','id','created','updated')

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
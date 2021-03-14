from rest_framework import serializers
from users.serializers import UserSerializer
from rooms.models import Room, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = 'room',


class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True) # 이걸 적어줘야 HTML form양식이 browseable API에 나타나지 않음
    is_fav = serializers.SerializerMethodField() # Serializer클래스의 메서드를 마치 필드와 같이 나타냄.
    photos = PhotoSerializer(read_only=True, many=True)

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
    
    def get_is_fav(self, obj): # 여기서 objs는 인스턴스들을 말하고 있음
        request = self.context.get('request')
        if request:
            user = request.user # 디비의 유저 인스턴스가 request에 박혀있음
            if user.is_authenticated: # 해당 유저 객체가 로그인 되었는지 확인함
                return obj in user.favs.all() # True/ False 반환
        return False

    def create(self, validated_data):
        request = self.context.get("request") # 이미 만들어진 get_serializer_context를 통해서 self.request값이 self인자를 통해서 전달되고 있음.
        room = Room.objects.create(**validated_data, user=request.user) 
        return room
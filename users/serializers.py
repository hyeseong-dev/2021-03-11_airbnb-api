from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "password",
        )
        read_only_fields = ("id", "superhost", "avatar")

    def validate_first_name(self, value):
        return value.upper()
    
    def create(self, validated_data):
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password) # hash화된 암호로 비밀번호가 설정됨.
        user.save()
        return user
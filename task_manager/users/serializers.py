from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser 

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        self.user = user
        return data

    def create(self, validated_data):
        refresh = RefreshToken.for_user(self.user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
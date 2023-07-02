from rest_framework import serializers
from django.contrib.auth.models import User

class EmailCheck(serializers.Serializer):
    email = serializers.EmailField(required=True)

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=3,
        write_only=True,
        required=True,
    )
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['email', 'password',]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
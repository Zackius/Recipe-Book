from rest_framework import serializers

from user.models import User


class UserRegistratinSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class FullUserAddSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=30, required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    second_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    username = serializers.CharField(max_length=50, required=True)
    password= serializers.CharField(required=True)

    def create(self, validated_data):
        # Logic for creating the user
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            second_name=validated_data['second_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
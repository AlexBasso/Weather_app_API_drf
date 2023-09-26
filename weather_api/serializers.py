from django.contrib.auth.models import User
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class for handling user login information: username and password.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for user data for user registration, 'username' and 'password' are mandatory and 'email' is not.

        Methods:
            create(self, validated_data): Create a new user instance with the provided data.
     """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class WeatherSerializer(serializers.Serializer):
    """
    Serializer class for weather data: 'parameter' and 'coordinates'.

        Fields:
            parameter (CharField): A field for the weather parameter (e.g., temperature, humidity).
            coordinates (ListField of DictField): A list of dictionaries representing coordinates.
        """
    parameter = serializers.CharField()
    coordinates = serializers.ListField(child=serializers.DictField())


class WeatherInputSerializer(serializers.Serializer):
    """
    Serializer class for weather input data, specifically a 'location'.
     """
    location = serializers.CharField()

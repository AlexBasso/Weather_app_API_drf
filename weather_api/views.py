from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, WeatherSerializer, UserLoginSerializer, WeatherInputSerializer

from .weather_request import weather_request_api, get_user_geolocation, search_weather_logic


class LoginView(APIView):
    """
    This view handles user login requests, authenticates the user, and returns an authentication token upon successful login.

        Attributes:
            permission_classes (list): A list of permissions that allow any user to access this view.
            serializer_class (class): The serializer class used for validating user login data.

        Methods:
            post(self, request, *args, **kwargs): Handles HTTP POST requests for user login.
             It validates the provided user login data, attempts to authenticate the user,
             and returns an authentication token if authentication is successful.
     """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(generics.CreateAPIView):
    """
    This view handles user registration requests, creates a new user account if
    the provided registration data is valid, and returns an authentication token
    upon successful registration.

        Attributes:
            queryset (QuerySet): A queryset containing all existing user objects.
            serializer_class (class): The serializer class used for user registration data.
            permission_classes (list): A list of permissions that allow any user to access this view.

        Methods:
            post(self, request, *args, **kwargs): Handles HTTP POST requests for user registration.
             It validates the provided registration data, creates a new user account,
             and returns an authentication token if registration is successful.
     """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentWeatherView(generics.ListAPIView):
    """
    View for retrieving current weather information, it requires authentication and permission for authenticated users.
    It retrieves the current geolocation of the user, fetches weather data based
    on the user's location, and returns the weather information in a serialized format.

        Attributes:
            authentication_classes (list): A list of authentication classes required for this view.
            permission_classes (list): A list of permissions that restrict access to authenticated users.
            serializer_class (class): The serializer class used for serializing weather data.

        Methods:
            get(self, request, *args, **kwargs): Handles HTTP GET requests to retrieve current weather data.
            It retrieves the user's current geolocation, fetches weather data based on the location,
            and returns the weather information in a serialized format.
     """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WeatherSerializer

    def get(self, request, *args, **kwargs):
        current_location = get_user_geolocation()
        latitude = current_location['latitude']
        longitude = current_location['longitude']
        country = current_location['country']

        weather_data = weather_request_api(latitude, longitude, country)
        if weather_data and 'data' in weather_data:
            data = weather_data['data']
            if data and len(data) > 0:
                weather_data_to_serialize = data[0]

                coordinates_data = weather_data_to_serialize.get('coordinates', [])

                serializer_data = {
                    "parameter": weather_data_to_serialize.get('parameter', ''),
                    "coordinates": coordinates_data,
                }

                serializer = WeatherSerializer(serializer_data)

                return Response(serializer.data, status=200)

        return Response({'error': 'Failed to fetch weather data'}, status=500)


class SearchWeatherView(generics.ListAPIView):
    """
    View for searching and retrieving current weather information based on provided location, requires authentication and
    permission for authenticated users.It allows users to search for weather information by providing a location query
    (city name or zip code) via GET or POST requests. The view fetches weather data based on the provided location
    query and returns the weather information.

        Attributes:
            authentication_classes (list): A list of authentication classes required for this view.
            permission_classes (list): A list of permissions that restrict access to authenticated users.
            serializer_class (class): The serializer class used for handling location queries.

        Methods:
            get(self, request, *args, **kwargs): Handles HTTP GET requests for weather information retrieval.
            Users can provide a location query via the 'location' query parameter to search for weather data.

            post(self, request, *args, **kwargs): Handles HTTP POST requests for weather information retrieval.
            Users can provide a location query via the request data to search for weather data.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WeatherInputSerializer

    def get(self, request, *args, **kwargs):
        location_query = self.request.query_params.get('location')

        if not location_query:
            return Response({'error': 'Please provide a location (city name or zip code)'}, status=400)

        try:
            return search_weather_logic(location_query, True, False)
        except Exception as e:
            print(f"Error: {e}")
            return Response({'error': 'Failed to fetch weather data'}, status=500)

        return Response({'error': 'Failed to fetch weather data'}, status=500)

    def post(self, request, *args, **kwargs):
        location_query = request.data.get('location') or request.POST.get('location') or request.data.get('parameter')

        if location_query:
            try:
                return search_weather_logic(location_query, True, False)
            except Exception as e:
                print(f"Error: {e}")
                return Response({'error': 'Failed to fetch weather data'}, status=500)

        return Response({'error': 'Failed to fetch weather data'}, status=500)


class ForcastWeatherView(generics.ListAPIView):
    """
    View for retrieving weather forecasts for 7 days, it requires authentication and permission for authenticated users.
    It allows users to retrieve weather forecasts based on a location query
    (city name or zip code) via GET or POST requests. The view fetches weather
    forecasts and returns the forecasted weather information.

        Attributes:
            authentication_classes (list): A list of authentication classes required for this view.
            permission_classes (list): A list of permissions that restrict access to authenticated users.
            serializer_class (class): The serializer class used for handling location queries.

        Methods:
            get(self, request, *args, **kwargs): Handles HTTP GET requests for weather forecast retrieval for 7 days.
            Users can provide a location query via the 'location' query parameter to retrieve forecasts.

            post(self, request, *args, **kwargs): Handles HTTP POST requests for weather forecast retrieval for 7 days.
            Users can provide a location query via the request data to retrieve forecasts.
     """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WeatherInputSerializer

    def get(self, request, *args, **kwargs):
        location_query = self.request.query_params.get('location')
        # print('testing loc:', location_query, type(location_query))

        if not location_query:
            try:
                return search_weather_logic(location_query, False, True)
            except Exception as e:
                print(f"Error: {e}")
                return Response({'error': 'Failed to fetch weather data'}, status=500)
        else:
            try:
                return search_weather_logic(location_query, False, False)
            except Exception as e:
                print(f"Error: {e}")
                return Response({'error': 'Failed to fetch weather data'}, status=500)

        return Response({'error': 'Failed to fetch weather data'}, status=500)

    def post(self, request, *args, **kwargs):
        location_query = request.data.get('location') or request.POST.get('parameter') or request.data.get('parameter')
        # print('testing loc:', location_query, type(location_query))

        if location_query:
            try:
                return search_weather_logic(location_query, False, False)
            except Exception as e:
                print(f"Error: {e}")
                return Response({'error': 'Failed to fetch weather data'}, status=500)

        return Response({'error': 'Failed to fetch weather data'}, status=500)

from django.urls import path
from .views import RegistrationView, LoginView, CurrentWeatherView, SearchWeatherView, ForcastWeatherView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('weather/current/', CurrentWeatherView.as_view(), name='current-weather'),
    path('weather/search/', SearchWeatherView.as_view(), name='search-weather'),
    path('weather/forcast/', ForcastWeatherView.as_view(), name='forcast-weather'),
]

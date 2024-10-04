from django.urls import path
from .views import car_search  # Import the car_search view

urlpatterns = [
    path('search/', car_search, name='car-search'),  # Define the search URL
]

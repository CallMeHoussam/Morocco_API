from django.urls import path
from .views import (
    CityListCreateView,
    CategoryListCreateView,
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    UpcomingEventsView,
)

urlpatterns = [
    path("cities/", CityListCreateView.as_view(), name="city-list-create"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),

    path("", EventListCreateView.as_view(), name="event-list-create"),
    path("upcoming/", UpcomingEventsView.as_view(), name="event-upcoming"),
    path("<int:pk>/", EventRetrieveUpdateDestroyView.as_view(), name="event-detail"),
]

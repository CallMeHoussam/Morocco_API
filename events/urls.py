from django.urls import path
from .views import (
    CityListCreateView,
    CityDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    UpcomingEventsView,
    event_stats,
)

urlpatterns = [
    path("cities/", CityListCreateView.as_view(), name="city-list-create"),
    path("cities/<slug:slug>/", CityDetailView.as_view(), name="city-detail"),
    
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),

    path("", EventListCreateView.as_view(), name="event-list-create"),
    path("upcoming/", UpcomingEventsView.as_view(), name="event-upcoming"),
    path("stats/", event_stats, name="event-stats"),
    path("<int:pk>/", EventRetrieveUpdateDestroyView.as_view(), name="event-detail"),
]
from django.urls import path
from .views import (
    CityListCreateView, CityDetailView, CategoryListCreateView, CategoryDetailView,
    EventListCreateView, EventRetrieveUpdateDestroyView, UpcomingEventsView,
    NewEventsView, TodayEventsView, ThisWeekEventsView, ThisMonthEventsView,
    event_stats, external_events, import_external_event, approve_event, pending_events
)

urlpatterns = [
    path("cities/", CityListCreateView.as_view(), name="city-list"),
    path("cities/<slug:slug>/", CityDetailView.as_view(), name="city-detail"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
    path("categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),
    path("", EventListCreateView.as_view(), name="event-list"),
    path("upcoming/", UpcomingEventsView.as_view(), name="event-upcoming"),
    path("new/", NewEventsView.as_view(), name="event-new"),
    path("today/", TodayEventsView.as_view(), name="event-today"),
    path("this-week/", ThisWeekEventsView.as_view(), name="event-this-week"),
    path("this-month/", ThisMonthEventsView.as_view(), name="event-this-month"),
    path("<int:pk>/", EventRetrieveUpdateDestroyView.as_view(), name="event-detail"),
    path("stats/", event_stats, name="event-stats"),
    path("external/", external_events, name="external-events"),
    path("external/import/", import_external_event, name="import-external-event"),
    path("admin/approve/<uuid:event_id>/", approve_event, name="approve-event"),
    path("admin/pending/", pending_events, name="pending-events"),
]
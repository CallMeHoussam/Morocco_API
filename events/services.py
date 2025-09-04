import requests
from django.conf import settings
from datetime import datetime, timedelta

class EventAPIService:
    def __init__(self):
        self.eventbrite_token = getattr(settings, 'EVENTBRITE_TOKEN', '')
        self.ticketmaster_key = getattr(settings, 'TICKETMASTER_KEY', '')

    def search_eventbrite_events(self, query="", location=""):
        return []

    def search_ticketmaster_events(self, keyword="", city="", country_code="MA"):
        return []

event_api_service = EventAPIService()
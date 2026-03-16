from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from core.models import User, FamilyGroup, Event

class EventAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.family1 = FamilyGroup.objects.create(name="Family 1")
        self.family2 = FamilyGroup.objects.create(name="Family 2")
        self.user = User.objects.create_user(username="testuser", password="password")

        # Create events for family1
        # Event 1 is tomorrow
        self.event1 = Event.objects.create(
            family=self.family1,
            creator=self.user,
            title="Event 1",
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )
        # Event 2 is today (earlier than Event 1)
        self.event2 = Event.objects.create(
            family=self.family1,
            creator=self.user,
            title="Event 2",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1)
        )

        # Create event for family2
        self.event3 = Event.objects.create(
            family=self.family2,
            creator=self.user,
            title="Event 3",
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=2, hours=1)
        )

    def test_list_events_success(self):
        """Test retrieving events for a specific family."""
        response = self.client.get(f"/api/families/{self.family1.id}/events/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

    def test_list_events_ordering(self):
        """Test that events are returned in chronological order."""
        response = self.client.get(f"/api/families/{self.family1.id}/events/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Event 2 starts before Event 1
        self.assertEqual(data[0]["title"], "Event 2")
        self.assertEqual(data[1]["title"], "Event 1")

    def test_list_events_filtering(self):
        """Test that only the requested family's events are returned."""
        response = self.client.get(f"/api/families/{self.family2.id}/events/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Event 3")

    def test_list_events_empty(self):
        """Test that an empty list is returned if no events exist for the family."""
        family3 = FamilyGroup.objects.create(name="Family 3")
        response = self.client.get(f"/api/families/{family3.id}/events/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

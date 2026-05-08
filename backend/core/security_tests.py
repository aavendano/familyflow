from django.test import TestCase, Client
from core.models import User, FamilyGroup, GroceryList, GroceryItem

class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.family = FamilyGroup.objects.create(name="Test Family")
        self.grocery_list = GroceryList.objects.create(family=self.family, name="Main List")
        # Ensure user with ID 1 exists
        self.user1, _ = User.objects.get_or_create(id=1, defaults={'username': 'admin'})

    def test_unauthenticated_create_grocery_item(self):
        """
        Test that an unauthenticated request fails with 401.
        """
        payload = {
            "name": "Hack Milk",
            "quantity": "2"
        }
        response = self.client.post(
            f"/api/families/{self.family.id}/groceries/",
            data=payload,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

        # Verify it was NOT created
        self.assertFalse(GroceryItem.objects.filter(name="Hack Milk").exists())

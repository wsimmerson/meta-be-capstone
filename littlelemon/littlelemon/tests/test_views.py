from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from restaurant.models import Menu, Booking
import json

# TestCase class


class MenuItemTests(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        for x in range(5):
            m = Menu.objects.create(title=f'item {x}', price=x, inventory=x)

    def test_get_items_from_api(self):
        self.client.login(username='temporary', password='temporary')
        res = self.client.get('/restaurant/menu/')
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 5)

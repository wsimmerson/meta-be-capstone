from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from restaurant.models import Menu, Booking


class MenuItemViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu = Menu.objects.create(title='item 1', price=12, inventory=10)
        self.data = {'title': 'item 2', 'price': 34, 'inventory': 2}
        self.url = reverse('restaurant:menu-list')
        self.user = User.objects.create(
            username='temp', email='temp@temp.com', password='temporary1')

    def test_list_menu_items(self):
        # Anyone should be able to see the menu items
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_menu_item(self):
        # Authenticated users should be able to create menu items
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)

    def test_create_menu_item_unauthenticated(self):
        # Unauthenticated users should not be able to create menu items
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SingleMenuItemViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu = Menu.objects.create(title='item 1', price=12, inventory=10)
        self.data = {"title": "item 2", 'price': self.menu.price,
                     'inventory': self.menu.inventory}
        self.url = reverse('restaurant:menu-detail',
                           kwargs={'pk': self.menu.pk})
        self.user = User.objects.create(
            username='temp', email='temp@temp.com', password='temporary1')

    def test_retrieve_menu_item(self):
        # Anyone should be able to see a menu item
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'item 1')

    def test_update_menu_item(self):
        # Authenticated users should be able to update menu items
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'item 2')

    def test_update_menu_item_unauthenticated(self):
        # Unauthenticated users should not be able to update menu items
        response = self.client.put(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookingViewSetTest(APITestCase):
    def setUp(self):
        self.client
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.booking = Booking.objects.create(
            name='test booking', booking_date='2022-01-23')
        self.data = {'name': 'test booking updated', 'number_of_guests':
                     self.booking.number_of_guests, 'booking_date': self.booking.booking_date}
        self.url = reverse('booking-list')

    def test_list_bookings(self):
        # Only authenticated users should be able to see bookings
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_bookings_unauthenticated(self):
        # Unauthenticated users should not be able to see bookings
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_booking(self):
        # Only authenticated users should be able to create bookings
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_create_booking_unauthenticated(self):
        # Unauthenticated users should not be able to create bookings
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_booking(self):
        # Only authenticated users should be able to update bookings
        self.client.force_authenticate(user=self.user)
        booking_url = reverse('booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.put(booking_url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test booking updated')

    def test_update_booking_unauthenticated(self):
        # Unauthenticated users should not be able to update bookings
        booking_url = reverse('booking-detail', kwargs={'pk': self.booking.pk})
        response = self.client.put(booking_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

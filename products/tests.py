from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

class ThrottlingTests(APITestCase):
    def test_throttling(self):
        for _ in range(101):
            self.client.get(reverse('product-list'))  # Замените 'some-view' на реальное имя вашей view
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 429)  # Ожидается статус 429 при превышении лимита

# Create your tests here.

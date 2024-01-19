from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token


class ManagementAdvertiserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_show_ad_view(self):
        response = self.client.get(reverse('show_ad'))
        self.assertEqual(response.status_code, 200)

    def test_ad_click_view(self):
        response = self.client.get(reverse('ad_click', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects

    def test_ad_statistics_view(self):
        response = self.client.get(reverse('ad_statistics', kwargs={'unique_id_ad': 1}))
        self.assertEqual(response.status_code, 200)

import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class LogInTest(TestCase):
	url = reverse("api:login")

	def setUp(self):
		self.credentials = {
			'username': 'temporary',
			'password': 'temp1234'
		}
		User.objects.create_user(**self.credentials)
	def test_authentication_without_password(self):
		response = self.client.post(self.url, {"username": "snowman"})
		self.assertEqual(400, response.status_code)
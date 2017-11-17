import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

class LogInTest(TestCase):
	# base_url = reverse('api_accounts')

	def setUp(self):
		self.credentials = {
			'username': 'temporary',
			'first_name': '1',
			'last_name': '2',
			'password': 'temp1234'
		}
		self.user = User.objects.create_user(**self.credentials)

	def test_login_view_update(self):
		# Test Login
		client = APIClient()
		response = client.post('/login/', self.credentials, format='json')
		self.assertEqual(response.status_code, 200, "The token should be successfully returned.")
		response_content = json.loads(response.content.decode('utf-8'))
		token = response_content["token"]
		print(token)

		# Test View Account
		client.credentials(HTTP_AUTHORIZATION='Token ' + token)
		response = client.get('/api/accounts')
		self.assertEqual(response.status_code, 200, "List of users should be working.")

		# Test Update Account
		client.credentials(HTTP_AUTHORIZATION='Token ' + token)
		response = client.patch('/api/accounts/'+ str(self.user.id), {"first_name": "Deny", "last_name": "Herianto"})
		self.assertEqual(response.status_code, 200, "Update should be working")
		response_content = json.loads(response.content.decode('utf-8'))
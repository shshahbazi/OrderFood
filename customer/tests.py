from django.test import TestCase
from rest_framework.test import APIClient
from .models import Profile, Address, Card

class ProfileTest(TestCase):

    def setUp(self) -> None:
        self.user_test = Profile.objects.create_user(full_name='shaqayeq sh', email='shsh@gmail.com',
                                                     phone='09111111111', password='shsh', is_verified=True)

        self.user_admin_test = Profile.objects.create_superuser(full_name='narges jahromi', email='nrgsjhrmi@gmail.com',
                                                                phone='09111111111', password='nrgs', is_verified=True)

        Profile.objects.create_user(full_name='john doe', password='john', email='john@email.com', phone='09111111111')

        self.client_rest_admin = APIClient()
        response = self.client.post('/login/', data={'email': 'nrgsjhrmi@gmail.com', 'password': 'nrgs'})
        self.client_rest_admin.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        self.client_rest_user = APIClient()
        response = self.client.post('/login/', data={'email': 'shsh@gmail.com', 'password': 'shsh'})
        self.client_rest_user.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_login(self):
        # user is verified with correct password
        response = self.client.post('/login/', data={'email': 'shsh@gmail.com', 'password': 'shsh'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], 'shaqayeq sh')

        # user is not verified
        response = self.client.post('/login/', data={'email': 'john@email.com', 'password': 'john'})
        self.assertEqual(response.status_code, 400)

    def test_login_fail(self):
        response = self.client.post('/login/', data={'email': 'shsh@gmail.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 400)

    def test_update_profile(self):
        response = self.client_rest_user.put('/update-profile/',
                                             data={'full_name': 'shaghayegh sh', 'phone': '09123456789'})
        self.user_test.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user_test.full_name, 'shaghayegh sh')

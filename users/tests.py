from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from url.models import Shortener


User = get_user_model()


class AdminViewsTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            role=User.ADMIN
        )
        self.client.login(username='admin', password='adminpassword')

        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword',
            role=User.USER
        )


    def test_admin_user_create_view(self):
        response = self.client.post(reverse('create_user'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())


    def test_admin_template_view(self):
        response = self.client.get(reverse('admin_statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/admin_template.html')


    def test_delete_user_view(self):
        response = self.client.post(reverse('delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


    def test_delete_url_view(self):
        long_url = 'https://www.example.com'
        short_url = 'test1234'
        shortener = Shortener.objects.create(
            long_url=long_url,
            short_url=short_url,
            user=self.user            
        )
        response = self.client.post(reverse('delete_url', args=[shortener.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Shortener.objects.filter(id=shortener.id).exists()) 


    def tearDown(self):
        self.admin_user.delete()
        self.user.delete()

from django.test import TestCase, Client
from django.urls import reverse

from users.models import CustomUser

from .models import Shortener
from .services import shorten_url, _generate_short_url

from unittest.mock import patch


class AddUrlViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.url = 'https://example.com'
        
        self.valid_form_data = {'long_url': self.url}
        
        self.invalid_form_data = {'long_url': 'invalid'}
    

    def test_get_request(self):
        """Проверка, что """
        self.client.force_login(self.user)
        response = self.client.get(reverse('add_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url/add_url.html')


    def test_post_request_with_valid_data(self):
        """Проверка на создание с валидными данными"""

        self.client.force_login(self.user)
        response = self.client.post(reverse('add_url'), data=self.valid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertIn('long_url', response.json())
        self.assertIn('short_url', response.json())
    

    def test_post_request_without_authentication(self):
        """Проверка на создание, если пользователь не authentication"""

        response = self.client.post(reverse('add_url'), data=self.valid_form_data)
        self.assertEqual(response.status_code, 302)
    

    def test_post_request_with_invalid_data(self):
        """Проверка на создание с невалидными данными"""

        self.client.force_login(self.user)
        response = self.client.post(reverse('add_url'), data=self.invalid_form_data)
        self.assertEqual(response.status_code, 400)


class UrlListViewTests(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = CustomUser.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

        self.url1 = Shortener.objects.create(
            long_url='https://www.example.com',
            short_url='abc',
            user=self.user1
        )
        self.url2 = Shortener.objects.create(
            long_url='https://www.google.com',
            short_url='def',
            user=self.user2
        )


    def test_url_list_view_template(self):
        """Проверка, что представление использует правильный шаблон."""

        response = self.client.get(reverse('url_list'))
        self.assertTemplateUsed(response, 'url/url_list.html')


    def test_url_list_view_context(self):
        """Проверка, что представление передает правильные данные в контекст."""

        response = self.client.get(reverse('url_list'))
        self.assertEqual(len(response.context['urls']), 2)
        self.assertEqual(response.context['urls'][0]['user'], self.user1)
        self.assertEqual(response.context['urls'][0]['urls'][0], self.url1)
        self.assertEqual(response.context['urls'][1]['user'], self.user2)
        self.assertEqual(response.context['urls'][1]['urls'][0], self.url2)


class ShortenerServiceTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')


    def test_generate_short_url(self):
        """ Проверка на длину короткого url"""
        short_url = _generate_short_url()
        self.assertEqual(len(short_url), 8)


    @patch('random.sample')
    def test_generate_short_url_with_mock(self, mock_sample):
        """ Проверка на создание короткого url """
        mock_sample.return_value = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        short_url = _generate_short_url()
        self.assertEqual(short_url, 'abcdefgh')


    def test_shorten_url(self):
        """ Проверка создания короткого url пользователем """
        long_url = 'https://www.example.com'
        self.client.force_login(self.user)
        request = self.client.get('/')
        request.user = self.user
        new_url = shorten_url(request, long_url)
        self.assertEqual(new_url.long_url, long_url)
        self.assertEqual(new_url.user, self.user)
        self.assertEqual(Shortener.objects.count(), 1)



class RedirectShortUrlViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='password')

        self.long_url = 'https://www.example.com'
        self.short_url = 'test1234'
        self.shortener = Shortener.objects.create(
            long_url=self.long_url,
            short_url=self.short_url,
            user=self.user            
        )


    def test_redirect_short_url(self):
        """Проверка на переход по короткому url"""
        self.assertEqual(self.shortener.click_count, 0)

        response = self.client.get(reverse('redirect_short_url', args=[self.short_url]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], self.long_url)
        self.shortener.refresh_from_db()
        self.assertEqual(self.shortener.click_count, 1)


    def test_short_url_not_found(self):
        """Проверка на несуществующий короткий url"""
        response = self.client.get(reverse('redirect_short_url', args=['invalid_short_url']))
        self.assertEqual(response.status_code, 404)

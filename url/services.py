import random
import string

from .models import Shortener


def _generate_short_url(url):
    """Функция для генерации короткого url"""

    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, 8))


def shorten_url(request, long_url):
    """Функция для создания в БД новой записи с проверкой на наличие дубликата короткого URL"""

    while True:
        short_url = _generate_short_url(long_url)

        if not Shortener.objects.filter(short_url=short_url).exists():

            new_url = Shortener(
                long_url=long_url,
                short_url=short_url,
                user=request.user
            )
            new_url.save()
            return new_url


def get_list_url(request):
    """Функция для возвращении url, которые принадлежат пользователю"""

    url = Shortener.objects.filter(user=request.user)

    return url
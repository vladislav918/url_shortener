import random
import string

from typing import Optional, List, Dict

from django.http import HttpRequest
from django.db.models import QuerySet

from .models import Shortener

from users.models import CustomUser


def _generate_short_url() -> str:
    """Функция для генерации короткого url"""

    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, 8))


def shorten_url(request: HttpRequest, long_url: str) -> Shortener:
    """Функция для создания в БД новой записи с проверкой на наличие дубликата короткого URL"""

    while True:
        short_url = _generate_short_url()

        if not Shortener.objects.filter(short_url=short_url).exists():

            new_url = Shortener(
                long_url=long_url,
                short_url=short_url,
                user=request.user
            )
            new_url.save()
            return new_url


def get_dict_user_and_urls(roles: Optional[CustomUser] = None) -> List[Dict[CustomUser, QuerySet]]:
    """Функция для получения словаря пользователя и его url"""

    if roles is None:
        roles = [CustomUser.ADMIN, CustomUser.USER]

    users = CustomUser.objects.filter(role__in=roles).prefetch_related('shortener_set').all()
    urls = []
    for user in users:
        user_urls = user.shortener_set.all()
        urls.append({
            'user': user,
            'urls': user_urls
        })
    return urls
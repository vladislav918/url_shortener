from django.db import models
from django.core.validators import URLValidator


class Shortener(models.Model):
    long_url = models.TextField(
        verbose_name='Длинный url',
        validators=[URLValidator()],
    )
    short_url = models.CharField(
        verbose_name='Короткий url',
        max_length=15,
        unique=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )
    click_count = models.PositiveIntegerField(
        verbose_name='Количество кликов',
        default=0
    )
    user = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'shortener_url'
        verbose_name = 'URL'
        verbose_name_plural = 'URLS'

    def __str__(self):
        return f'{self.long_url} to {self.short_url}'
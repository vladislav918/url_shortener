from django.contrib import admin
from .models import Shortener

from django.template.defaultfilters import truncatechars

@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    model = Shortener
    list_display = ['generate_short_url_from_long_url', 'short_url', 'click_count','created_at']


    def generate_short_url_from_long_url(self, obj: Shortener) -> str:
        return truncatechars(obj.long_url, 60)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'role']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser'),
                         'classes': 'collapse'}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

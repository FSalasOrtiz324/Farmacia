from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class PharmacyUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        return False  # desactivar en lugar de borrar

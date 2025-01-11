from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "password"]


admin.site.register(User, CustomUserAdmin)

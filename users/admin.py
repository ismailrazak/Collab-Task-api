from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ['id','password']

admin.site.register(User,CustomUserAdmin)
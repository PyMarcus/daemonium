from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

AdminSite.site_header: str = "💀Ransomware monitor💀"


class CustomUserAdmin(UserAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)

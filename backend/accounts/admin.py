from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Organization, User

admin.site.register(Organization)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Organization", {"fields": ("organization", "role")}),
    )
    list_display = ("username", "organization", "role", "is_staff")
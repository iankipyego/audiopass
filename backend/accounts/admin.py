from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Hospital, User


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "timezone")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "hospital", "is_staff", "is_superuser")
    list_filter = ("role", "hospital", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")

    # Add role and hospital to the edit form (the default UserAdmin would
    # otherwise hide our custom fields).
    fieldsets = UserAdmin.fieldsets + (
        ("Audiopass", {"fields": ("role", "hospital")}),
    )
    # Add role and hospital to the create form too, so they can be set when a
    # user is first created rather than only on a second edit.
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Audiopass", {"fields": ("role", "hospital")}),
    )

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("username", "password", "first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "first_name", "last_name", "email"),
            },
        ),
    )

    list_display = ("email", "username", "date_joined")
    list_filter = ("is_admin", "is_active")
    search_fields = (
        "email",
        "username",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
    )

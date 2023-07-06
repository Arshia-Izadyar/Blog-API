from django.contrib import admin

from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("custom_field",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("custom_field",)}),)
    
    list_display = ('email', 'username', 'date_joined')
    list_filter = ('is_admin','is_active')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login',)
    
    
    
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import CustomUser
from .forms import CustomUserSignUpForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserSignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ( 'email', 'is_staff', 'is_active', )
    list_filter = ( 'email', 'is_staff', 'is_active', )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )

    search_fields = ('email', )
    ordering = ('email', )



admin.site.register(CustomUser, CustomUserAdmin)
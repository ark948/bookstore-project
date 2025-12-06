from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser, UserProfile, Province, City
from accounts.forms import CustomUserSignUpForm, CustomUserChangeForm


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profile"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserSignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ( 'email', 'is_staff', 'is_active', )
    list_filter = ( 'email', 'is_staff', 'is_active', )

    fieldsets = (
        (None, {"fields": ("email", "password", "role", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "role"
            )}
        ),
    )

    search_fields = ('email', )
    ordering = ('email', )
    inlines = [UserProfileInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Province)
admin.site.register(City)
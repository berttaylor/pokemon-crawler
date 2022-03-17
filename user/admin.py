from django.contrib import admin

# Register your models here.
from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "date_joined",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name"
    )

    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    ("first_name", "last_name"),
                    "email",
                    "password",
                    ("date_joined", "last_login"),
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )

    readonly_fields = ("password", "last_login", "date_joined",)
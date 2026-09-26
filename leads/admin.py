from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "name",
        "phone",
        "telegram",
        "form_type",
        "source",
        "status",
    )
    list_filter = ("status", "form_type", "created_at")
    search_fields = ("name", "phone", "telegram", "comment", "source")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at", "page_url", "extra")
    date_hierarchy = "created_at"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
                    "form_type",
                    "name",
                    "phone",
                    "telegram",
                    "source",
                    "comment",
                )
            },
        ),
        ("Служебное", {"fields": ("page_url", "extra", "created_at", "updated_at")}),
    )

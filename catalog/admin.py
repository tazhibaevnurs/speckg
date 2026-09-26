from django.contrib import admin

from .models import Brand, Category, Vehicle, VehicleImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_flagship", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "condition",
        "availability",
        "price_usd",
        "year",
        "is_published",
        "is_featured",
    )
    list_filter = ("brand", "category", "condition", "availability", "is_published")
    search_fields = ("name", "short_specs", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price_usd", "is_published", "is_featured")
    inlines = [VehicleImageInline]
    fieldsets = (
        (
            "Карточка",
            {
                "fields": (
                    "brand",
                    "category",
                    "name",
                    "slug",
                    "condition",
                    "availability",
                    "price_usd",
                    "is_published",
                    "is_featured",
                    "sort_order",
                )
            },
        ),
        (
            "ТТХ",
            {
                "fields": (
                    "year",
                    "mileage_km",
                    "power_hp",
                    "wheel_formula",
                    "payload",
                    "engine",
                    "gearbox",
                    "fuel",
                    "gvw",
                    "short_specs",
                )
            },
        ),
        ("Описание", {"fields": ("description", "extra_features")}),
        ("Фото", {"fields": ("main_image", "use_placeholder")}),
    )

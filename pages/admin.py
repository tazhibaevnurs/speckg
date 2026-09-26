from django.contrib import admin

from .models import Document, FAQ


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "is_placeholder", "file", "sort_order")
    list_editable = ("is_placeholder", "sort_order")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_published", "sort_order")
    list_editable = ("is_published", "sort_order")
    search_fields = ("question", "answer")

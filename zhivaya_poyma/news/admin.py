from django.contrib import admin
from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "created_at")
    list_filter = ("is_published", "published_at", "created_at")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Основное", {
            "fields": ("title", "slug", "excerpt")
        }),
        ("Контент", {
            "fields": ("cover_image", "body")
        }),
        ("Публикация", {
            "fields": ("is_published", "published_at", "created_at")
        }),
    )
    
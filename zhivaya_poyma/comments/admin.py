from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",
        "page",
        "is_approved",
        "created_at",
    )
    list_filter = ("is_approved", "created_at")
    search_fields = (
        "author_name",
        "author_email",
        "text",
        "page__title",
    )
    readonly_fields = (
        "page",
        "author_name",
        "author_email",
        "text",
        "created_at",
        "ip_address",
        "user_agent",
    )
    actions = ("approve_comments", "unapprove_comments")

    @admin.action(description="Одобрить выбранные комментарии")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Снять публикацию выбранных комментариев")
    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
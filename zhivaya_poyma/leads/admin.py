from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "interest_type", "email", "telegram", "created_at")
    list_filter = ("interest_type", "created_at")
    search_fields = ("name", "email", "telegram", "message")
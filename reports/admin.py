"""
Admin configuration for the reports app.
"""

from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter", "reason", "status", "listing", "reported_user", "created_at")
    list_filter = ("reason", "status")
    search_fields = ("reporter__email", "reported_user__email")
    list_editable = ("status",)

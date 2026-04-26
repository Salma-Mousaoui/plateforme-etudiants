"""
Admin configuration for the housing app.
"""

from django.contrib import admin

from .models import HousingListing


@admin.register(HousingListing)
class HousingListingAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "type", "price", "owner", "is_approved", "is_active", "created_at")
    list_filter = ("type", "is_approved", "is_active", "city")
    search_fields = ("title", "city", "owner__email")
    list_editable = ("is_approved", "is_active")

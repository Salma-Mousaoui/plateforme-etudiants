"""
Models for the dashboard app — audit log for all admin actions.
"""

from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    TARGET_TYPES = [
        ("user", "User"),
        ("listing", "Listing"),
        ("report", "Report"),
        ("group", "Group"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
    )
    action = models.CharField(max_length=200)
    target_type = models.CharField(
        max_length=20, choices=TARGET_TYPES, blank=True, null=True
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Activity Log"

    def __str__(self):
        actor = self.user.get_full_name() if self.user else "System"
        return f"{actor} — {self.action}"

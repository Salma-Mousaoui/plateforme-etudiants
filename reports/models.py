"""
Models for the reports app.

Role: Reports and content moderation.
"""

from django.db import models
from django.conf import settings


class Report(models.Model):
    REASONS = [
        ("scam", "Scam"),
        ("inappropriate_behavior", "Inappropriate behavior"),
        ("fake_profile", "Fake profile"),
        ("other", "Other"),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_sent",
    )
    listing = models.ForeignKey(
        "housing.HousingListing",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_received",
    )
    reason = models.CharField(max_length=50, choices=REASONS)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[("pending", "Pending"), ("resolved", "Resolved")],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ["-created_at"]

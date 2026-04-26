"""
Models for the reports app.

Role: Reports and content moderation.
"""

from django.db import models
from django.conf import settings


class Report(models.Model):
    """Report filed against a listing or a user."""

    REASON_CHOICES = [
        ('arnaque', 'Scam'),
        ('comportement_inapproprie', 'Inappropriate Behaviour'),
        ('faux_profil', 'Fake Profile'),
        ('autre', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made',
    )
    listing = models.ForeignKey(
        'housing.HousingListing',
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True,
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_received',
        null=True,
        blank=True,
    )
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.reported_user or self.listing
        return f"Report by {self.reporter.username} -> {target} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']

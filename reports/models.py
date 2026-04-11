"""
Models for the reports app.

Role : Signalements et modération de contenu.
"""

from django.db import models
from django.conf import settings


class Report(models.Model):
    """Signalement d'une annonce ou d'un utilisateur."""

    REASON_CHOICES = [
        ('arnaque', 'Arnaque'),
        ('comportement_inapproprie', 'Comportement inapproprié'),
        ('faux_profil', 'Faux profil'),
        ('autre', 'Autre'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('resolved', 'Résolu'),
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
        return f"Signalement de {self.reporter.username} -> {target} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-created_at']

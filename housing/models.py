"""
Models for the housing app.

Role : Gestion des annonces de logements.
"""

from django.db import models
from django.conf import settings


class HousingListing(models.Model):
    TYPES = [
        ("chambre", "Room"),
        ("appartement", "Apartment"),
        ("colocation", "Shared housing"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    city = models.CharField(max_length=100)
    photo = models.ImageField(
        upload_to="listings/",
        blank=True,
        null=True,
        verbose_name="Photo",
    )
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.city} ({self.price}€/month)"

    class Meta:
        verbose_name = "Annonce de logement"
        verbose_name_plural = "Annonces de logement"
        ordering = ["-created_at"]

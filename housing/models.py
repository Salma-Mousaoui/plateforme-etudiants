"""
Models for the housing app.

Role : Gestion des annonces de logements.
"""

from django.db import models
from django.conf import settings


class HousingListing(models.Model):
    """Annonce de logement publiée par un utilisateur."""

    TYPE_CHOICES = [
        ('chambre', 'Chambre'),
        ('appartement', 'Appartement'),
        ('colocation', 'Colocation'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='housing_listings',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.city} ({self.price} EUR)"

    class Meta:
        verbose_name = 'Annonce de logement'
        verbose_name_plural = 'Annonces de logement'
        ordering = ['-created_at']

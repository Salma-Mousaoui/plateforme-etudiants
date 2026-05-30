"""
Models for the housing app.

Role : Housing listing management.
"""

from django.db import models
from django.conf import settings


def get_listings_storage():
    """Return ListingsStorage in production, None (default) in local dev."""
    if settings.USE_SUPABASE_STORAGE:
        from core.storage_backends import ListingsStorage
        return ListingsStorage()
    return None


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
        storage=get_listings_storage,
        blank=True,
        null=True,
        verbose_name="Photo",
    )
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.city} ({self.price}€/month)"

    def get_photo_url(self):
        if self.photo:
            try:
                return self.photo.url
            except Exception:
                return None
        return None

    class Meta:
        verbose_name = "Housing Listing"
        verbose_name_plural = "Housing Listings"
        ordering = ["-created_at"]


class ListingPhoto(models.Model):
    listing = models.ForeignKey(
        HousingListing, on_delete=models.CASCADE, related_name='photos'
    )
    image = models.ImageField(upload_to='listings/gallery/', storage=get_listings_storage)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"Photo #{self.ordre} - {self.listing.title}"

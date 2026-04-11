"""
Models for the core app.

Role : Modèle User personnalisé et profils professionnels.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Utilisateur personnalisé de la plateforme."""

    ROLE_CHOICES = [
        ('student', 'Étudiant'),
        ('lawyer', 'Avocat'),
        ('orientation', 'Conseiller d\'orientation'),
        ('housing', 'Agent immobilier'),
        ('admin', 'Administrateur'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class ProfessionalProfile(models.Model):
    """Profil étendu pour les utilisateurs professionnels."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile')
    bio = models.TextField(blank=True)
    speciality = models.CharField(max_length=200, blank=True)
    languages = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Profil pro de {self.user.username}"

    class Meta:
        verbose_name = 'Profil professionnel'
        verbose_name_plural = 'Profils professionnels'

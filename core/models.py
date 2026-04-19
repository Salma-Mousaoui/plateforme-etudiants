from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """
    Custom user model.
    Inherits from AbstractUser to keep all Django features
    (login, password, admin) and adds custom fields.
    Email is used as the login identifier.
    """
    ROLES = [
        ("student",     "Student"),
        ("lawyer",      "Lawyer"),
        ("orientation", "Academic Advisor"),
        ("housing",     "Landlord / Agency"),
        ("admin",       "Administrator"),
    ]

    role         = models.CharField(max_length=20, choices=ROLES, default="student")
    city         = models.CharField(max_length=100, blank=True, verbose_name="City")
    phone        = models.CharField(max_length=30, blank=True, verbose_name="Phone")
    photo        = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_validated = models.BooleanField(
        default=False,
        help_text="True only after admin validation for professional accounts"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def is_pro(self):
        """Returns True if the user is a professional."""
        return self.role in ["lawyer", "orientation", "housing"]


class ProfessionalProfile(models.Model):
    """
    Extended profile for professional users only.
    Created automatically via signal when a pro user registers.
    """
    user       = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_profile"
    )
    bio        = models.TextField(blank=True, default="")
    speciality = models.CharField(max_length=200, blank=True, default="")
    languages  = models.CharField(max_length=200, blank=True, default="")
    website    = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Professional Profile"
        verbose_name_plural = "Professional Profiles"

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_professional_profile(sender, instance, created, **kwargs):
    """Auto-create a ProfessionalProfile when a pro user is created."""
    if created and instance.is_pro():
        ProfessionalProfile.objects.get_or_create(user=instance)

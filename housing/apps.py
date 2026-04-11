"""
App configuration for housing.
"""

from django.apps import AppConfig


class HousingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'housing'
    verbose_name = 'Logements'

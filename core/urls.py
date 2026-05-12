"""URL patterns for the core app."""

from django.urls import path

from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    path("",          views.LandingView.as_view(), name="landing"),
    path("register/", RegisterView.as_view(),       name="register"),
    path("login/",    CustomLoginView.as_view(),    name="login"),
    path("logout/",   CustomLogoutView.as_view(),   name="logout"),
    path("profile/",  views.profil_view,            name="profil"),

    # Role-specific dashboards
    path("dashboard/etudiant/",      views.StudentDashboardView.as_view(), name="student_dashboard"),
    path("dashboard/professionnel/", views.ProDashboardView.as_view(),     name="pro_dashboard"),
    path("dashboard/logement/",      views.HousingDashboardView.as_view(), name="housing_dashboard"),

    # Legacy professional space (kept for backward compatibility)
    path("mon-espace/",                  views.EspaceProView,         name="espace-pro"),
    path("mon-espace/modifier-profil/",  views.UpdateProfileProView,  name="update-profile-pro"),
]

"""URL patterns for the core app."""

from django.urls import path

from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    path("",           views.LandingView.as_view(),  name="landing"),
    path("register/",  RegisterView.as_view(),        name="register"),
    path("login/",     CustomLoginView.as_view(),     name="login"),
    path("logout/",    CustomLogoutView.as_view(),    name="logout"),
    path("profile/",   views.profil_view,             name="profil"),
    path("espace-pro/", views.espace_pro_view,        name="espace-pro"),
]

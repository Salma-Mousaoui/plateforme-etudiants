"""
Views for the core app.

LandingView        — public homepage
RegisterView       — user sign-up (student + professional)
CustomLoginView    — email-based login
CustomLogoutView   — GET/POST logout
profil_view        — authenticated profile page
"""

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from chat.models import Message
from .forms import LoginForm, ProfessionalProfileForm, RegisterForm
from .models import ProfessionalProfile

User = get_user_model()


# ==============================================================================
# LandingView — public homepage
# ==============================================================================

def _role_dashboard_url(role):
    """Return the redirect URL name for a given user role."""
    if role == "admin":
        return "dashboard"
    if role in ("lawyer", "orientation", "housing"):
        return "espace-pro"
    return "housing"  # student


class LandingView(TemplateView):
    template_name = "core/landing.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(_role_dashboard_url(request.user.role))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Elan - Moroccan Students in Spain"
        context["services"] = [
            {
                "icon":        "building",
                "title":       "Housing",
                "anchor":      "housing",
                "description": "Find verified rooms and apartments in Spain",
                "url":         "/housing/",
            },
            {
                "icon":        "journal-text",
                "title":       "Counselors",
                "anchor":      "counselors",
                "description": "University and academic degree advice",
                "url":         "/orienteurs/",
            },
            {
                "icon":        "briefcase",
                "title":       "Lawyers",
                "anchor":      "lawyers",
                "description": "Immigration lawyers, certified and verified",
                "url":         "/avocats/",
            },
            {
                "icon":        "chat-dots",
                "title":       "Community",
                "anchor":      "community",
                "description": "Chat with Moroccan students across Spain",
                "url":         "/chat/",
            },
        ]
        return context


# ==============================================================================
# RegisterView
# ==============================================================================

class RegisterView(View):
    """Handle student and professional sign-up."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("landing")
        form = RegisterForm()
        return render(request, "core/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user.is_pro():
                # Professional accounts are inactive until admin validates them
                messages.info(
                    request,
                    "Your account has been created and is pending admin validation. "
                    "You will be notified once approved.",
                )
                return redirect("landing")

            # Students are active immediately — log them in
            authenticated_user = authenticate(
                request,
                username=user.email,
                password=form.cleaned_data["password1"],
            )
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(
                    request,
                    f"Welcome, {user.get_full_name()}! Your account has been created.",
                )
            return redirect(_role_dashboard_url(user.role))

        return render(request, "core/register.html", {"form": form})


# ==============================================================================
# CustomLoginView
# ==============================================================================

class CustomLoginView(DjangoLoginView):
    """Email-based login using Django's built-in LoginView."""

    form_class    = LoginForm
    template_name = "core/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("landing")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        from django.urls import reverse
        return reverse(_role_dashboard_url(self.request.user.role))

    def form_invalid(self, form):
        messages.error(self.request, "Incorrect email or password.")
        return super().form_invalid(form)


# ==============================================================================
# CustomLogoutView
# ==============================================================================

class CustomLogoutView(View):
    """Logout via POST (CSRF-safe) or GET (fallback for simple links)."""

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect("landing")

    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect("landing")


# ==============================================================================
# profil_view
# ==============================================================================

@login_required
def profil_view(request):
    """Display and update the authenticated user's profile."""
    user        = request.user
    pro_profile = None

    if user.is_pro():
        pro_profile, _ = ProfessionalProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Update base user fields
        user.city  = request.POST.get("city",  user.city).strip()
        user.phone = request.POST.get("phone", user.phone).strip()

        if "photo" in request.FILES:
            user.photo = request.FILES["photo"]

        user.save()

        # Update professional profile if applicable
        if user.is_pro() and pro_profile:
            pro_form = ProfessionalProfileForm(request.POST, instance=pro_profile)
            if pro_form.is_valid():
                pro_form.save()

        messages.success(request, "Your profile has been updated.")
        return redirect("profil")

    pro_form = ProfessionalProfileForm(instance=pro_profile) if pro_profile else None

    return render(request, "core/profil.html", {
        "pro_profile": pro_profile,
        "pro_form":    pro_form,
    })


# ==============================================================================
# EspaceProView
# ==============================================================================

@login_required
def EspaceProView(request):
    """Professional dashboard — only accessible to validated non-student users."""
    user = request.user

    if user.role == "student" or not user.is_validated:
        messages.warning(request, "Your account is pending admin validation")
        return redirect("/")

    context = {}

    if user.role == "housing":
        listings = user.listings.all()
        context["listings"]           = listings
        context["listings_published"] = listings.filter(is_approved=True).count()
        context["listings_pending"]   = listings.filter(is_approved=False).count()
    elif user.role in ("lawyer", "orientation"):
        pro_profile, _ = ProfessionalProfile.objects.get_or_create(user=user)
        context["professional_profile"] = pro_profile
        context["form"] = ProfessionalProfileForm(instance=pro_profile)

    context["recent_messages"] = (
        Message.objects
        .filter(receiver=user)
        .select_related("sender")
        .order_by("-sent_at")[:5]
    )

    return render(request, "core/espace_pro.html", context)


# ==============================================================================
# UpdateProfileProView
# ==============================================================================

@login_required
def UpdateProfileProView(request):
    """Allow a validated professional to update their professional profile."""
    user        = request.user
    pro_profile = user.professional_profile

    if request.method == "POST":
        form = ProfessionalProfileForm(request.POST, request.FILES, instance=pro_profile)
        if form.is_valid():
            form.save()
            if form.cleaned_data.get("photo"):
                user.photo = form.cleaned_data["photo"]
                user.save()
            messages.success(request, "Profile updated successfully")
            return redirect("espace-pro")
    else:
        form = ProfessionalProfileForm(instance=pro_profile)

    return render(request, "core/update_profile_pro.html", {"form": form})

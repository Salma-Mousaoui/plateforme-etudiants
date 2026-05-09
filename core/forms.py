"""
Forms for the core app.

RegisterForm     — student / professional sign-up
LoginForm        — email-based authentication
ProfessionalProfileForm — pro profile edit
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import ProfessionalProfile

User = get_user_model()

# Roles exposed to public registration — admin is excluded
ROLES_WITHOUT_ADMIN = [
    ("student",     "Student"),
    ("lawyer",      "Lawyer"),
    ("orientation", "Academic Advisor"),
    ("housing",     "Landlord / Agency"),
]


# ==============================================================================
# RegisterForm
# ==============================================================================

class RegisterForm(UserCreationForm):
    """Sign-up form.  username is set to email automatically in save()."""

    first_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class":        "form-control",
            "placeholder":  "First name",
            "autocomplete": "given-name",
        }),
    )

    last_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class":        "form-control",
            "placeholder":  "Last name",
            "autocomplete": "family-name",
        }),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class":        "form-control",
            "placeholder":  "your@email.com",
            "autocomplete": "email",
        }),
    )

    # Hidden select — synced via JS with the visual role cards
    role = forms.ChoiceField(
        choices=ROLES_WITHOUT_ADMIN,
        initial="student",
        widget=forms.Select(attrs={
            "class": "form-select d-none",
            "id":    "id_role",
        }),
    )

    city = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class":        "form-control",
            "placeholder":  "City in Spain (optional)",
            "autocomplete": "address-level2",
        }),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class":        "form-control",
            "placeholder":  "Create a password",
            "autocomplete": "new-password",
        }),
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            "class":        "form-control",
            "placeholder":  "Repeat your password",
            "autocomplete": "new-password",
        }),
    )

    class Meta:
        model  = User
        fields = ["first_name", "last_name", "email", "role", "city",
                  "password1", "password2"]

    # ── Validation ────────────────────────────────────────────────────────────

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )
        return email

    def clean_role(self):
        role = self.cleaned_data.get("role")
        valid_roles = [r[0] for r in ROLES_WITHOUT_ADMIN]
        if role not in valid_roles:
            raise forms.ValidationError("Invalid role selected.")
        return role

    # ── Save ──────────────────────────────────────────────────────────────────

    def save(self, commit=True):
        user = super().save(commit=False)

        email = self.cleaned_data["email"].strip().lower()
        user.email      = email
        user.username   = email   # AbstractUser requires username — use email
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name  = self.cleaned_data["last_name"].strip()
        user.role       = self.cleaned_data["role"]
        user.city       = self.cleaned_data.get("city", "").strip()

        if user.is_pro():
            # Pro accounts must be reviewed before login is allowed
            user.is_active    = False
            user.is_validated = False
        else:
            # Students can log in immediately
            user.is_active    = True
            user.is_validated = False

        if commit:
            user.save()
        return user


# ==============================================================================
# LoginForm
# ==============================================================================

class LoginForm(AuthenticationForm):
    """Email-based login form."""

    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={
            "class":        "form-control",
            "placeholder":  "your@email.com",
            "autocomplete": "email",
            "autofocus":    True,
        }),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class":        "form-control",
            "placeholder":  "Your password",
            "autocomplete": "current-password",
        }),
    )

    error_messages = {
        "invalid_login": "Incorrect email or password. Please try again.",
        "inactive":      "This account is inactive. Please wait for admin validation.",
    }


# ==============================================================================
# ProfessionalProfileForm
# ==============================================================================

class ProfessionalProfileForm(forms.ModelForm):
    """Edit form for the professional profile section."""

    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model  = ProfessionalProfile
        fields = ["bio", "speciality", "languages", "website"]
        widgets = {
            "bio": forms.Textarea(attrs={
                "class":       "form-control",
                "rows":        4,
                "placeholder": "Describe your services...",
            }),
            "speciality": forms.TextInput(attrs={
                "class":       "form-control",
                "placeholder": "e.g. Immigration Law",
            }),
            "languages": forms.TextInput(attrs={
                "class":       "form-control",
                "placeholder": "e.g. Arabic, French, Spanish",
            }),
            "website": forms.URLInput(attrs={
                "class":       "form-control",
                "placeholder": "https://your-website.com",
            }),
        }

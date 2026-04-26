"""
Admin dashboard views — all protected by admin_required.
Follows POST-Redirect-GET; every mutating action writes to ActivityLog.
"""

import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from chat.models import ChatGroup
from housing.models import HousingListing
from reports.models import Report

from .decorators import admin_required
from .models import ActivityLog

User = get_user_model()


# ── Helpers ────────────────────────────────────────────────────────────────────

def log_action(request, action, target_type=None, target_id=None):
    ActivityLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        target_type=target_type,
        target_id=target_id,
        ip_address=request.META.get("REMOTE_ADDR"),
    )


def _sidebar_counts():
    pros = (
        User.objects.filter(is_validated=False)
        .exclude(role__in=["student", "admin"])
        .count()
    )
    return {
        "pros_count": pros,
        "pending_pros_count": pros,
        "pending_listings_count": HousingListing.objects.filter(
            is_approved=False, is_active=True
        ).count(),
        "pending_reports_count": Report.objects.filter(status="pending").count(),
    }


# ── Dashboard Home ─────────────────────────────────────────────────────────────

@method_decorator(admin_required, name="dispatch")
class DashboardHomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(_sidebar_counts())
        today = datetime.date.today()
        ctx["total_users"] = User.objects.count()
        ctx["new_this_month"] = User.objects.filter(
            date_joined__month=today.month,
            date_joined__year=today.year,
        ).count()
        ctx["open_reports"] = Report.objects.filter(status="pending").count()
        ctx["active_listings"] = HousingListing.objects.filter(
            is_approved=True, is_active=True
        ).count()
        ctx["pending_listings"] = HousingListing.objects.filter(
            is_approved=False, is_active=True
        ).count()
        ctx["pros_en_attente"] = (
            User.objects.filter(is_validated=False)
            .exclude(role__in=["student", "admin"])
            .order_by("date_joined")[:5]
        )
        ctx["annonces_en_attente"] = (
            HousingListing.objects.filter(is_approved=False, is_active=True)
            .select_related("owner")[:5]
        )
        ctx["signalements_pending"] = (
            Report.objects.filter(status="pending")
            .select_related("reporter", "listing", "reported_user")[:5]
        )
        return ctx


# ── Users ──────────────────────────────────────────────────────────────────────

@method_decorator(admin_required, name="dispatch")
class UserListView(View):
    template_name = "dashboard/users/liste.html"

    def get(self, request):
        qs = User.objects.all().order_by("-date_joined")
        role = request.GET.get("role", "")
        statut = request.GET.get("statut", "")
        search = request.GET.get("search", "")
        if role:
            qs = qs.filter(role=role)
        if statut == "actif":
            qs = qs.filter(is_active=True)
        elif statut == "inactif":
            qs = qs.filter(is_active=False)
        elif statut == "attente":
            qs = qs.filter(is_validated=False).exclude(role="student")
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
            )
        paginator = Paginator(qs, 20)
        page = paginator.get_page(request.GET.get("page"))
        ctx = _sidebar_counts()
        ctx.update({
            "users": page,
            "role": role,
            "statut": statut,
            "search": search,
            "page_title": "All Users",
        })
        return render(request, self.template_name, ctx)


@method_decorator(admin_required, name="dispatch")
class PendingProsView(View):
    def get(self, request):
        qs = (
            User.objects.filter(is_validated=False)
            .exclude(role__in=["student", "admin"])
            .order_by("date_joined")
        )
        paginator = Paginator(qs, 20)
        page = paginator.get_page(request.GET.get("page"))
        ctx = _sidebar_counts()
        ctx.update({"users": page, "page_title": "Pending Professional Accounts"})
        return render(request, "dashboard/users/liste.html", ctx)


@method_decorator(admin_required, name="dispatch")
class StudentListView(View):
    def get(self, request):
        qs = User.objects.filter(role="student").order_by("-date_joined")
        paginator = Paginator(qs, 20)
        page = paginator.get_page(request.GET.get("page"))
        ctx = _sidebar_counts()
        ctx.update({"users": page, "page_title": "Students"})
        return render(request, "dashboard/users/liste.html", ctx)


@method_decorator(admin_required, name="dispatch")
class InactiveUserListView(View):
    def get(self, request):
        qs = User.objects.filter(is_active=False).order_by("-date_joined")
        paginator = Paginator(qs, 20)
        page = paginator.get_page(request.GET.get("page"))
        ctx = _sidebar_counts()
        ctx.update({"users": page, "page_title": "Disabled Accounts"})
        return render(request, "dashboard/users/liste.html", ctx)


@method_decorator(admin_required, name="dispatch")
class UserDetailView(View):
    def get(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        pro_profile = getattr(target, "professional_profile", None)
        listings = HousingListing.objects.filter(owner=target).order_by("-created_at")
        reports_received = Report.objects.filter(
            reported_user=target
        ).select_related("reporter").order_by("-created_at")
        ctx = _sidebar_counts()
        ctx.update({
            "target_user": target,
            "pro_profile": pro_profile,
            "listings": listings,
            "reports_received": reports_received,
            "page_title": f"User — {target.get_full_name() or target.email}",
        })
        return render(request, "dashboard/users/detail.html", ctx)


@method_decorator(admin_required, name="dispatch")
class ActivateUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = True
        user.save()
        log_action(request, f"Activated account: {user.email}", "user", user.id)
        messages.success(request, f"Account of {user.get_full_name() or user.email} activated.")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard")


@method_decorator(admin_required, name="dispatch")
class DeactivateUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        if user.role == "admin":
            messages.error(request, "Cannot deactivate an administrator account.")
            return redirect("dashboard")
        if user == request.user:
            messages.error(request, "You cannot deactivate your own account.")
            return redirect("dashboard")
        user.is_active = False
        user.save()
        log_action(request, f"Deactivated account: {user.email}", "user", user.id)
        messages.warning(request, f"Account of {user.get_full_name() or user.email} deactivated.")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard")


@method_decorator(admin_required, name="dispatch")
class ValidateUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_validated = True
        user.is_active = True
        user.save()
        log_action(request, f"Validated account: {user.email}", "user", user.id)
        messages.success(request, f"{user.get_full_name() or user.email} validated successfully.")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard")


@method_decorator(admin_required, name="dispatch")
class DeleteUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        if user.role == "admin":
            messages.error(request, "Cannot delete an administrator account.")
            return redirect("dashboard")
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
            return redirect("dashboard")
        name = user.get_full_name() or user.email
        log_action(request, f"Deleted account: {user.email}", "user")
        user.delete()
        messages.success(request, f"Account of {name} deleted.")
        return redirect("dashboard-users")


# ── Listings ───────────────────────────────────────────────────────────────────

@method_decorator(admin_required, name="dispatch")
class AdminListingListView(View):
    def get(self, request):
        qs = HousingListing.objects.select_related("owner").order_by("-created_at")
        statut = request.GET.get("statut", "")
        city = request.GET.get("city", "")
        listing_type = request.GET.get("type", "")
        if statut == "pending":
            qs = qs.filter(is_approved=False, is_active=True)
        elif statut == "approved":
            qs = qs.filter(is_approved=True, is_active=True)
        elif statut == "rejected":
            qs = qs.filter(is_active=False)
        if city:
            qs = qs.filter(city__icontains=city)
        if listing_type:
            qs = qs.filter(type=listing_type)
        cities = HousingListing.objects.values_list("city", flat=True).distinct().order_by("city")
        paginator = Paginator(qs, 20)
        page = paginator.get_page(request.GET.get("page"))
        ctx = _sidebar_counts()
        ctx.update({
            "listings": page,
            "statut": statut,
            "city": city,
            "listing_type": listing_type,
            "cities": cities,
            "page_title": "Housing Listings",
        })
        return render(request, "dashboard/annonces/liste.html", ctx)


@method_decorator(admin_required, name="dispatch")
class AdminListingDetailView(View):
    def get(self, request, pk):
        listing = get_object_or_404(
            HousingListing.objects.select_related("owner"), pk=pk
        )
        reports = Report.objects.filter(listing=listing).select_related("reporter")
        ctx = _sidebar_counts()
        ctx.update({
            "listing": listing,
            "reports": reports,
            "page_title": listing.title,
        })
        return render(request, "dashboard/annonces/detail.html", ctx)


@method_decorator(admin_required, name="dispatch")
class AdminValidateListingView(View):
    def post(self, request, pk):
        listing = get_object_or_404(HousingListing, pk=pk)
        listing.is_approved = True
        listing.is_active = True
        listing.save()
        log_action(request, f"Approved listing: {listing.title}", "listing", listing.id)
        messages.success(request, f"Listing '{listing.title}' approved.")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard-listings")


@method_decorator(admin_required, name="dispatch")
class AdminRejectListingView(View):
    def post(self, request, pk):
        listing = get_object_or_404(HousingListing, pk=pk)
        listing.is_active = False
        listing.save()
        log_action(request, f"Rejected listing: {listing.title}", "listing", listing.id)
        messages.warning(request, f"Listing '{listing.title}' rejected.")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard-listings")


@method_decorator(admin_required, name="dispatch")
class AdminDeleteListingView(View):
    def post(self, request, pk):
        listing = get_object_or_404(HousingListing, pk=pk)
        title = listing.title
        log_action(request, f"Deleted listing: {title}", "listing")
        listing.delete()
        messages.success(request, f"Listing '{title}' deleted.")
        return redirect("dashboard-listings")


# ── Reports ────────────────────────────────────────────────────────────────────

@method_decorator(admin_required, name="dispatch")
class ReportListView(View):
    def get(self, request):
        qs = (
            Report.objects.select_related("reporter", "listing", "reported_user")
            .order_by("-created_at")
        )
        statut = request.GET.get("statut", "")
        if statut:
            qs = qs.filter(status=statut)
        paginator = Paginator(qs, 20)
        page = paginator.get_page(request.GET.get("page"))
        ctx = _sidebar_counts()
        ctx.update({"reports": page, "statut": statut, "page_title": "Reports"})
        return render(request, "dashboard/signalements/liste.html", ctx)


@method_decorator(admin_required, name="dispatch")
class ReportDetailView(View):
    def get(self, request, pk):
        report = get_object_or_404(
            Report.objects.select_related("reporter", "listing", "reported_user"), pk=pk
        )
        ctx = _sidebar_counts()
        ctx.update({"report": report, "page_title": f"Report #{report.id}"})
        return render(request, "dashboard/signalements/detail.html", ctx)


@method_decorator(admin_required, name="dispatch")
class ResolveReportView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.status = "resolved"
        report.save()
        log_action(request, f"Resolved report #{report.id}", "report", report.id)
        messages.success(request, "Report marked as resolved.")
        return redirect(request.META.get("HTTP_REFERER") or "dashboard-reports")


@method_decorator(admin_required, name="dispatch")
class RemoveReportedContentView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        if report.listing:
            report.listing.is_active = False
            report.listing.save()
            log_action(
                request,
                f"Removed reported listing #{report.listing.id}",
                "listing",
                report.listing.id,
            )
            messages.warning(request, "Reported listing deactivated.")
        elif report.reported_user:
            if report.reported_user.role == "admin":
                messages.error(request, "Cannot deactivate an administrator.")
                return redirect("dashboard-reports")
            report.reported_user.is_active = False
            report.reported_user.save()
            log_action(
                request,
                f"Deactivated reported user: {report.reported_user.email}",
                "user",
                report.reported_user.id,
            )
            messages.warning(request, "Reported user deactivated.")
        report.status = "resolved"
        report.save()
        return redirect("dashboard-reports")


# ── Chat Groups ────────────────────────────────────────────────────────────────

class _ChatGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["name", "city"]


@method_decorator(admin_required, name="dispatch")
class ChatGroupListView(View):
    def get(self, request):
        groups = ChatGroup.objects.prefetch_related("members").order_by("name")
        ctx = _sidebar_counts()
        ctx.update({
            "groups": groups,
            "form": _ChatGroupForm(),
            "page_title": "Chat Groups",
        })
        return render(request, "dashboard/groupes_chat/liste.html", ctx)


@method_decorator(admin_required, name="dispatch")
class CreateChatGroupView(View):
    def post(self, request):
        form = _ChatGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            log_action(request, f"Created chat group: {group.name}", "group", group.id)
            messages.success(request, f"Group '{group.name}' created.")
        else:
            messages.error(request, "Invalid form data. Please check the fields.")
        return redirect("dashboard-groups")


@method_decorator(admin_required, name="dispatch")
class UpdateChatGroupView(View):
    def post(self, request, pk):
        group = get_object_or_404(ChatGroup, pk=pk)
        form = _ChatGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            log_action(request, f"Updated chat group: {group.name}", "group", group.id)
            messages.success(request, f"Group '{group.name}' updated.")
        else:
            messages.error(request, "Invalid form data.")
        return redirect("dashboard-groups")


@method_decorator(admin_required, name="dispatch")
class DeleteChatGroupView(View):
    def post(self, request, pk):
        group = get_object_or_404(ChatGroup, pk=pk)
        name = group.name
        log_action(request, f"Deleted chat group: {name}", "group")
        group.delete()
        messages.success(request, f"Group '{name}' deleted.")
        return redirect("dashboard-groups")


# ── Activity Logs ──────────────────────────────────────────────────────────────

@method_decorator(admin_required, name="dispatch")
class ActivityLogView(View):
    def get(self, request):
        qs = ActivityLog.objects.select_related("user").order_by("-created_at")
        search = request.GET.get("search", "")
        if search:
            qs = qs.filter(
                Q(action__icontains=search) | Q(user__email__icontains=search)
            )
        paginator = Paginator(qs, 50)
        page = paginator.get_page(request.GET.get("page"))
        ctx = _sidebar_counts()
        ctx.update({"logs": page, "search": search, "page_title": "Activity Logs"})
        return render(request, "dashboard/logs.html", ctx)

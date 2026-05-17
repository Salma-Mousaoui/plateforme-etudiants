from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View

from reports.models import Report

User = get_user_model()


def _pro_dashboard_url(role):
    if role in ("lawyer", "orientation"):
        return "pro_dashboard"
    if role == "housing":
        return "housing_dashboard"
    return "landing"


class LawyerListView(ListView):
    template_name = "professionals/lawyer_list.html"
    context_object_name = "professionals"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ("lawyer", "orientation", "housing"):
            return redirect(_pro_dashboard_url(request.user.role))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(role="lawyer", is_validated=True, is_active=True)


class AdvisorListView(ListView):
    template_name = "professionals/advisor_list.html"
    context_object_name = "professionals"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ("lawyer", "orientation", "housing"):
            return redirect(_pro_dashboard_url(request.user.role))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(role="orientation", is_validated=True, is_active=True)


def ProfessionalDetailView(request, pk):
    pro = get_object_or_404(User, pk=pk, is_validated=True)
    profile = getattr(pro, "professional_profile", None)
    return render(request, "professionals/professional_detail.html", {
        "pro": pro,
        "profile": profile,
    })


@method_decorator(login_required, name="dispatch")
class ReportProView(View):
    def post(self, request, pk):
        reported_user = get_object_or_404(User, pk=pk, is_validated=True)
        reason = request.POST.get("reason", "other")
        description = request.POST.get("description", "")
        Report.objects.create(
            reporter=request.user,
            reported_user=reported_user,
            reason=reason,
            description=description,
        )
        messages.success(request, "Report submitted. Thank you for helping keep the platform safe.")
        return redirect("pro-detail", pk=pk)

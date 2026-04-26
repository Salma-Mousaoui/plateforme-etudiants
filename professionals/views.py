from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View

from reports.models import Report

User = get_user_model()


class LawyerListView(ListView):
    template_name = "professionals/lawyer_list.html"
    context_object_name = "professionals"

    def get_queryset(self):
        return User.objects.filter(role="lawyer", is_validated=True, is_active=True)


class AdvisorListView(ListView):
    template_name = "professionals/advisor_list.html"
    context_object_name = "professionals"

    def get_queryset(self):
        return User.objects.filter(role="orientation", is_validated=True, is_active=True)


class ProfessionalDetailView(DetailView):
    template_name = "professionals/professional_detail.html"
    context_object_name = "pro"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs["pk"], is_validated=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["profile"] = self.object.professional_profile
        except User.professional_profile.RelatedObjectDoesNotExist:
            context["profile"] = None
        return context


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

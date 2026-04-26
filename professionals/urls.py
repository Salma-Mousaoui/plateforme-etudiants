from django.urls import path
from django.views.generic import RedirectView

from .views import AdvisorListView, LawyerListView, ProfessionalDetailView, ReportProView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="lawyers", permanent=False), name="professionals"),
    path("lawyers/", LawyerListView.as_view(), name="lawyers"),
    path("advisors/", AdvisorListView.as_view(), name="advisors"),
    path("professional/<int:pk>/", ProfessionalDetailView.as_view(), name="pro-detail"),
    path("professional/<int:pk>/report/", ReportProView.as_view(), name="report-pro"),
]

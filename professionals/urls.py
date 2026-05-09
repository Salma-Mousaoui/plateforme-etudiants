from django.urls import path

from .views import AdvisorListView, LawyerListView, ProfessionalDetailView, ReportProView

urlpatterns = [
    path("avocats/", LawyerListView.as_view(), name="lawyers"),
    path("orienteurs/", AdvisorListView.as_view(), name="advisors"),
    path("professionnel/<int:pk>/", ProfessionalDetailView, name="pro-detail"),
    path("professionnel/<int:pk>/signaler/", ReportProView.as_view(), name="report-pro"),
]

"""URL patterns for the Elan admin dashboard."""

from django.urls import path

from . import views

urlpatterns = [
    # Home
    path("", views.DashboardHomeView.as_view(), name="dashboard"),

    # Users
    path("utilisateurs/", views.UserListView.as_view(), name="dashboard-users"),
    path("utilisateurs/pros-en-attente/", views.PendingProsView.as_view(), name="dashboard-pending-pros"),
    path("utilisateurs/etudiants/", views.StudentListView.as_view(), name="dashboard-students"),
    path("utilisateurs/inactifs/", views.InactiveUserListView.as_view(), name="dashboard-inactive"),
    path("utilisateurs/<int:user_id>/", views.UserDetailView.as_view(), name="dashboard-user-detail"),
    path("utilisateurs/<int:user_id>/activer/", views.ActivateUserView.as_view(), name="activate-user"),
    path("utilisateurs/<int:user_id>/desactiver/", views.DeactivateUserView.as_view(), name="deactivate-user"),
    path("utilisateurs/<int:user_id>/valider/", views.ValidateUserView.as_view(), name="validate-user"),
    path("utilisateurs/<int:user_id>/supprimer/", views.DeleteUserView.as_view(), name="delete-user"),

    # Listings
    path("annonces/", views.AdminListingListView.as_view(), name="dashboard-listings"),
    path("annonces/<int:pk>/", views.AdminListingDetailView.as_view(), name="dashboard-listing-detail"),
    path("annonces/<int:pk>/valider/", views.AdminValidateListingView.as_view(), name="validate-listing"),
    path("annonces/<int:pk>/rejeter/", views.AdminRejectListingView.as_view(), name="reject-listing"),
    path("annonces/<int:pk>/supprimer/", views.AdminDeleteListingView.as_view(), name="delete-listing"),

    # Reports
    path("signalements/", views.ReportListView.as_view(), name="dashboard-reports"),
    path("signalements/<int:pk>/", views.ReportDetailView.as_view(), name="dashboard-report-detail"),
    path("signalements/<int:pk>/traiter/", views.ResolveReportView.as_view(), name="resolve-report"),
    path("signalements/<int:pk>/supprimer-contenu/", views.RemoveReportedContentView.as_view(), name="remove-reported-content"),

    # Chat Groups
    path("groupes-chat/", views.ChatGroupListView.as_view(), name="dashboard-groups"),
    path("groupes-chat/creer/", views.CreateChatGroupView.as_view(), name="create-group"),
    path("groupes-chat/<int:pk>/modifier/", views.UpdateChatGroupView.as_view(), name="update-group"),
    path("groupes-chat/<int:pk>/supprimer/", views.DeleteChatGroupView.as_view(), name="delete-group"),

    # Logs
    path("logs/", views.ActivityLogView.as_view(), name="dashboard-logs"),
]

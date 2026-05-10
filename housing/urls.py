from django.urls import path

from . import views

urlpatterns = [
    path("logements/",                      views.ListingListView.as_view(),   name="listings"),
    path("logements/creer/",                views.CreateListingView.as_view(), name="create-listing"),
    path("logements/mes-annonces/",         views.MyListingsView.as_view(),    name="my-listings"),
    path("logements/<int:pk>/",             views.ListingDetailView.as_view(), name="listing-detail"),
    path("logements/<int:pk>/modifier/",    views.EditListingView,             name="edit-listing"),
    path("logements/<int:pk>/supprimer/",   views.DeleteListingView,           name="delete-listing"),
    path("logements/<int:pk>/signaler/",    views.ReportListingView.as_view(), name="report-listing"),
]

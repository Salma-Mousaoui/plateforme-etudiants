from django.urls import path
from django.views.generic import RedirectView

from .views import (
    CreateListingView,
    ListingDetailView,
    ListingListView,
    MyListingsView,
    ReportListingView,
)

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="listings", permanent=False), name="housing"),
    path("listings/", ListingListView.as_view(), name="listings"),
    path("listings/create/", CreateListingView.as_view(), name="create-listing"),
    path("listings/my-listings/", MyListingsView.as_view(), name="my-listings"),
    path("listings/<int:pk>/", ListingDetailView.as_view(), name="listing-detail"),
    path("listings/<int:pk>/report/", ReportListingView.as_view(), name="report-listing"),
]

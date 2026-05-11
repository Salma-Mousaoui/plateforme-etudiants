from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View

from reports.models import Report
from .forms import HousingListingForm
from .models import HousingListing


@method_decorator(login_required, name="dispatch")
class UpdateListingView(View):
    template_name = "housing/edit_listing.html"

    def _get_listing(self, request, pk):
        return get_object_or_404(HousingListing, pk=pk, owner=request.user)

    def get(self, request, pk):
        listing = self._get_listing(request, pk)
        return render(request, self.template_name, {"form": HousingListingForm(instance=listing), "listing": listing})

    def post(self, request, pk):
        listing = self._get_listing(request, pk)
        form = HousingListingForm(request.POST, instance=listing)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.is_approved = False
            updated.save()
            messages.success(request, "Listing updated and resubmitted for approval.")
            return redirect("espace-pro")
        return render(request, self.template_name, {"form": form, "listing": listing})


@method_decorator(login_required, name="dispatch")
class DeleteListingView(View):
    def post(self, request, pk):
        listing = get_object_or_404(HousingListing, pk=pk, owner=request.user)
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect("espace-pro")


class ListingListView(ListView):
    template_name = "housing/listing_list.html"
    context_object_name = "listings"

    def get_queryset(self):
        qs = HousingListing.objects.filter(is_approved=True, is_active=True)
        cities = self.request.GET.getlist("city")
        listing_type = self.request.GET.get("type")
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")
        if cities:
            qs = qs.filter(city__in=cities)
        if listing_type:
            qs = qs.filter(type=listing_type)
        if price_min:
            try:
                qs = qs.filter(price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                qs = qs.filter(price__lte=float(price_max))
            except ValueError:
                pass
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        approved_active = HousingListing.objects.filter(is_approved=True, is_active=True)
        context["city_counts"] = (
            approved_active
            .values("city")
            .annotate(count=Count("id"))
            .order_by("city")
        )
        context["selected_cities"] = self.request.GET.getlist("city")
        context["selected_type"] = self.request.GET.get("type", "")
        context["types"] = HousingListing.TYPES
        return context


class ListingDetailView(DetailView):
    model = HousingListing
    template_name = "housing/listing_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_approved:
            raise Http404
        return obj


@method_decorator(login_required, name="dispatch")
class CreateListingView(View):
    template_name = "housing/create_listing.html"

    def _check_permission(self, request):
        if request.user.role != "housing" or not request.user.is_validated:
            messages.error(request, "Only validated landlords/agencies can post listings.")
            return False
        return True

    def get(self, request):
        if not self._check_permission(request):
            return redirect("listings")
        return render(request, self.template_name, {"form": HousingListingForm()})

    def post(self, request):
        if not self._check_permission(request):
            return redirect("listings")
        form = HousingListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.is_approved = False
            listing.save()
            messages.success(request, "Listing submitted — awaiting admin validation.")
            return redirect("my-listings")
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class MyListingsView(ListView):
    template_name = "housing/my_listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        return HousingListing.objects.filter(owner=self.request.user).order_by("-created_at")


@method_decorator(login_required, name="dispatch")
class ReportListingView(View):
    def post(self, request, pk):
        listing = get_object_or_404(HousingListing, pk=pk)
        reason = request.POST.get("reason", "other")
        description = request.POST.get("description", "")
        Report.objects.create(
            reporter=request.user,
            listing=listing,
            reason=reason,
            description=description,
        )
        messages.success(request, "Report submitted. Thank you for helping keep the platform safe.")
        return redirect("listing-detail", pk=pk)

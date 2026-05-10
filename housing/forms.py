from django import forms

from .models import HousingListing


class HousingListingForm(forms.ModelForm):
    class Meta:
        model = HousingListing
        fields = ["title", "description", "type", "price", "city", "photo"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Listing title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": "0.01", "step": "0.01"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "photo": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

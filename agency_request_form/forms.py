from django import forms
from .models import AgencyRequest
from django.core.exceptions import ValidationError
import re
class AgencyRequestForm(forms.ModelForm):

    class Meta:
        model = AgencyRequest
        fields = "__all__"

        widgets = {
            "agency_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter agency name",
                    "maxlength": "255",
                }
            ),

            "ecgains": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter ECGAINS",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter state code (DB value)",
                    "maxlength": "100",
                }
            ),

            "contact_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter contact email",
                    "maxlength": "254",
                }
            ),

            "developer": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "module_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter module name",
                    "maxlength": "255",
                }
            ),

            "bid_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "main_bid_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/bid",
                    "maxlength": "1000",
                    
                    
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                    
                }
            ),

            "has_bids": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "procurement_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "comments": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter comments",
                    "rows": 4,
                    "cols" : 40
                }
            ),
        }

    def clean_ecgains(self):
        ecgains = self.cleaned_data["ecgains"]

        ecgains = ecgains.strip()

        if not re.fullmatch(
            r"^\d{2}-\d{2}-\d{3}-\d{4}-\d{6}$",
            ecgains
        ):
            raise ValidationError(
                "ECGAINS must follow the format XX-XX-XXX-XXXX-XXXXX."
            )

        return ecgains


    def clean_main_bid_link(self):
        main_bid_link = self.cleaned_data["main_bid_link"]

        if not main_bid_link.startswith(("http://", "https://")):
            raise ValidationError(
                "Please enter a valid HTTP or HTTPS URL."
            )

        return main_bid_link
from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "telegram", "interest_type", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
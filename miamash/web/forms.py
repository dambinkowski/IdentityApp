from django import forms
from core.models import ProfileIdentityVariant, Request, RequestIdentityVariant 

# Profile Identity Variant forms 
class ProfileIdentityVariantForm(forms.ModelForm):
    class Meta:
        model = ProfileIdentityVariant
        fields = ['label', 'context', 'variant']


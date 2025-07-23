from django import forms
from core.models import ProfileIdentityVariant, Request, RequestIdentityVariant, User

# Profile Identity Variant forms 
class ProfileIdentityVariantForm(forms.ModelForm):
    class Meta:
        model = ProfileIdentityVariant
        fields = ['label', 'context', 'variant']


# Request send forms
class RequestSendForm(forms.ModelForm):
    receiver = forms.CharField(label='Receiver Username', help_text="Enter username, who you want to ask the information from")
    request_reasoning = forms.CharField(label='Request Reasoning', widget=forms.Textarea, help_text="Enter the reason for the request")

    class Meta:
        model = Request
        fields = ['receiver', 'request_reasoning']

    def clean_receiver(self):
        receiver = self.cleaned_data.get('receiver')
        # check if such a user exists in users
        if not User.objects.filter(username=receiver).exists():
            raise forms.ValidationError("User with this username does not exist.")
        return User.objects.get(username=receiver)
    
class RequestSendUpdateForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_reasoning']
    
class RequestSendRequestIdentityVariantForm(forms.ModelForm):
    class Meta:
        model = RequestIdentityVariant
        fields = ['label', 'context']


# request receive forms
class RequestReceiveRequestIdentityVariantForm(forms.ModelForm):
    class Meta:
        model = RequestIdentityVariant
        fields = ['profile_link']

    def __init__(self, *args, **kwargs):
        self.request_object = kwargs.pop('request_object', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.request_object and not cleaned_data.get('profile_link'):
            raise forms.ValidationError("Profile link is required for the request identity variant.")
        return cleaned_data


    
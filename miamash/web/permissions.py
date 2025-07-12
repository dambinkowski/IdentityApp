from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from core.models import *

# only profile owner mixin 
class ProfileIdentityVariantOwnerMixin(LoginRequiredMixin, View):
    """
    Mixin to ensure that user is logged in. 
    And server uses those login credential to restrict access to ProfileIdentityVariant objects.
    That it only allows CRUD operation to be performed by the owner.
    """
    model = ProfileIdentityVariant
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import View
from core.models import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

# only profile owner mixin 
class ProfileIdentityVariantOwnerPermissionMixin(LoginRequiredMixin, View):
    """
    Security mixin insures that user is logged in, then references those server side credentials
    to only allow CRUD operations on ProfileIdentityVariants that they own.
    """
    model = ProfileIdentityVariant
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user) 
    
# only request sender mixin
class RequestSenderPermissionMixin(LoginRequiredMixin, View):
    """
    Security mixin insures that user is logged in, then references those server side credentials
    to only allow CRUD operations on Requests that user is a sender. 
    """
    model = Request
    
    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)

class RequestSenderRequestIdentityVariantPermissionMixin(LoginRequiredMixin, View):
    """
    Security mixin insures that user is logged in, then references those server side credentials
    to only allow CRUD operations on Requests that user is a sender. 
    """
    model = RequestIdentityVariant
    pk_url_kwarg = 'request_identity_variant_pk'  
    
    def get_queryset(self):
        # get the request object from the URL, make sure that user is allowed to CRUD that instance 
        return self.model.objects.filter(request__sender=self.request.user) # type: ignore
    
    # since RequestIdentityVariant object is a chil of Request object, for creation safety 
    # overiding dispatch method is also nessesery 
    def dispatch(self, request, *args, **kwargs):
        # handle not authenticated user where there is no request.sender 
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # if user authenticated, check if has parent permission, or 404 they don't have such a resaurce access 
        self.request_send = get_object_or_404(Request, pk=kwargs['pk'], sender=request.user)  # only expose when there is match of PK from URL and the sender is request.user 
        return super().dispatch(request, *args, **kwargs)
    
# only request receiver mixin
class RequestReceiverPermissionMixin(LoginRequiredMixin, View):
    """
    Security mixin insures that user is logged in, then references those server side credentials
    to only allow CRUD operations on Requests that user is a receiver.
    """
    model = Request
    
    def get_queryset(self):
        return self.model.objects.filter(receiver=self.request.user) # type: ignore

    # helper method to get the request object from the URL using pk, only from the set of requests that user is allowed to access
    def get_secured_request(self):
        pk = self.kwargs.get('pk') # request pk from the URL
        try:
            return self.get_queryset().get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404("There is no such request.")


class RequestReceiverRequestIdentityVariantPermissionMixin(LoginRequiredMixin, View):
    """
    Security mixin insures that user is logged in, then references those server side credentials
    to only allow CRUD operations on RequestIdentityVariants that user is a receiver.
    """
    model = RequestIdentityVariant
    pk_url_kwarg = 'request_identity_variant_pk'  
    
    def get_queryset(self):
        # get the request object from the URL, make sure that user is allowed to CRUD that instance 
        return self.model.objects.filter(request__receiver=self.request.user) # type: ignore
    
    # since RequestIdentityVariant object is a chil of Request object, for creation safety 
    # overiding dispatch method is also nessesery 
    def dispatch(self, request, *args, **kwargs):
        # handle not authenticated user where there is no request.sender 
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # if user authenticated, check if has parent permission, or 404 they don't have such a resaurce access 
        self.request_receive = get_object_or_404(Request, pk=kwargs['pk'], receiver=request.user)  # only expose when there is match of PK from URL and the receiver is request.user 
        if self.request_receive.status != Request.Status.ACCEPTED:
            raise PermissionDenied("Request must be accepted to view variants.")
        return super().dispatch(request, *args, **kwargs)
    
class IsRequestAcceptedPermissionMixin(View):
    """
    Permission checks if the request status is accepted.
    """
    # to make it roboust check if object is Request or RequestIdentityVariant
    def get_object(self, queryset=None):
        obj = super().get_object(queryset) # type: ignore 
        if isinstance(obj, Request):
            if obj.status != 'accepted':
                raise PermissionDenied("Request is not accepted.")
        elif isinstance(obj, RequestIdentityVariant):
            if obj.request.status != 'accepted':
                raise PermissionDenied("Request is not accepted.")
        else:
            raise PermissionDenied("Only Request or RequestIdentityVariant objects are allowed.")
        return obj
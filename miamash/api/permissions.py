from rest_framework.permissions import BasePermission
from core.models import Request, RequestIdentityVariant

class IsProfileOwner(BasePermission):
    """
    Checks if user is logged in and is owner ProfileIdentityVariant
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # in this case, obj is a ProfileIdentityVariant instance
        return obj.user == request.user

class IsRequestSender(BasePermission):
    """
    Checks if user is logged in and is the sender of the Request
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # in this case, obj is a Request instance or a RequestIdentityVariant instance
        # variable request is the DRF request object that has request.user - as logged in user who is making the request to access the view
        if isinstance(obj, Request):
            # if obj is a Request instance, return true if Request.sender matches the logged in user
            return obj.sender == request.user
        
        if isinstance(obj, RequestIdentityVariant):
            # if obj is a RequestIdentityVariant instance, get parent Request to check who is sender and compare it with logged in user
            return obj.request.sender == request.user

        # there sohuld be no other cases, but if there are, return False untill added 
        return False
    
    
    
class IsRequestReceiver(BasePermission):
    """
    Checks if user is logged in and is the receiver of the Request
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # in this case, obj is a Request instance or a RequestIdentityVariant instance
        # variable request is the DRF request object that has request.user - as logged in user who is making the request to access the view
        if isinstance(obj, Request):
            # if obj is a Request instance, return true if Request.sender matches the logged in user
            return obj.receiver == request.user
        
        if isinstance(obj, RequestIdentityVariant):
            # if obj is a RequestIdentityVariant instance, get parent Request to check who is sender and compare it with logged in user
            return obj.request.receiver == request.user

        # there sohuld be no other cases, but if there are, return False untill added 
        return False
    
class IsRequestAccepted(BasePermission):
    """
    Check if request status is ACCEPTED
    """
    
    def has_object_permission(self, request, view, obj):
        # if its Request instance 
        if isinstance(obj, Request):
            # if obj is a Request instance, return true if Request.sender matches the logged in user
            return obj.receiver == Request.Status.ACCEPTED
        # if its RequestIdentityVariant instance
        if isinstance(obj, RequestIdentityVariant):
            # if obj is a RequestIdentityVariant instance, get parent Request to check who is sender and compare it with logged in user
            return obj.request.status == Request.Status.ACCEPTED

        return False

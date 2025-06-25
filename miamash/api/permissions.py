from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsProfileOwner(BasePermission):
    """
    Custom permission to only allow profile owners to view or edit their profiles.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsRequestSender(BasePermission):
    """
    Custom permission to only allow the sender of a request to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
    
class IsRequestReceiver(BasePermission):
    """
    Custom permission to only allow the receiver to see requested views, accept or deny requests. And link with their personal profile. 
    """
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user
from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsProfileOwner(BasePermission):
    """
    Custom permission to only allow profile owners to view or edit their profiles.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

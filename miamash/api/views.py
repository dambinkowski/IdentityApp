from rest_framework import viewsets, permissions
from core.models import * 
from .serializers import *
from .permissions import *

class ProfileIdentityVariantViewSet(viewsets.ModelViewSet):
    """
    User can see, create, edit and delete only their own profile identity variants.
    """
    queryset = ProfileIdentityVariant.objects.all()
    serializer_class = ProfileIdentityVariantSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]

    def get_queryset(self):
        user = self.request.user
        return ProfileIdentityVariant.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

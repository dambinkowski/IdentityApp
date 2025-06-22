from rest_framework import viewsets, permissions
from core.models import * 
from .serializers import *
from .permissions import *

class ProfileIdentityVariantViewSet(viewsets.ModelViewSet):
    """
    User can see, create, edit and delete their profile identity variants.
    """
    queryset = ProfileIdentityVariant.objects.all()
    serializer_class = ProfileIdentityVariantSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]

    def get_queryset(self):
        user = self.request.user
        return ProfileIdentityVariant.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SenderRequestViewSet(viewsets.ModelViewSet):
    """
    User can send requests to other users, see them, edit and delete. 
    """
    queryset = Request.objects.all()
    serializer_class = SenderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    # only show request where user is the sender 
    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(sender=user)
    

    
class ReceiverRequestViewSet(viewsets.ModelViewSet):
    """
    User can see, create, edit and delete only their own requests as receiver.
    """
    queryset = Request.objects.all()
    serializer_class = ReceiverRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    # only show request where user is the receiver
    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(receiver=user)
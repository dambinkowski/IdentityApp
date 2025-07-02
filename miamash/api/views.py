from rest_framework import generics, permissions
from core.models import * 
from .serializers import *
from .permissions import *


# Profile Identity Variant views 
class ProfileIdentityVariantListCreateAPIView(generics.ListCreateAPIView):
    """
    User can see their profile identity variants and create new ones.
    """
    serializer_class = ProfileIdentityVariantSerializer
    permission_classes = [IsProfileOwner]

    # for list query where logged in user is the owner only 
    def get_queryset(self):
        return ProfileIdentityVariant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileIdentityVariantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    User can see, edit and delete their profile identity variants.
    """
    serializer_class = ProfileIdentityVariantSerializer
    permission_classes = [IsProfileOwner]

    # for detail query where logged in user is the owner only 
    def get_queryset(self):
        return ProfileIdentityVariant.objects.filter(user=self.request.user)


# Request Send views 

class RequestSendListCreateAPIView(generics.ListCreateAPIView):
    """
    User can see sent-requests and create new ones.
    """
    serializer_class = RequestSendListCreateSerializer
    permission_classes = [IsRequestSender]

    # for list query where logged in user is the sender only 
    def get_queryset(self):
        return Request.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class RequestSendDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    User can see, edit and delete their sent-requests.
    """
    serializer_class = RequestSendDetailSerializer
    permission_classes = [IsRequestSender]

    # for detail query where logged in user is the sender only 
    def get_queryset(self):
        return Request.objects.filter(sender=self.request.user)

class RequestSendRequestIdentityVariantListCreateAPIView(generics.ListCreateAPIView):
    """
    User can see and create request identity variants for their sent-requests.
    """
    serializer_class = RequestSendRequestIdentityVariantSerializer
    permission_classes = [IsRequestSender]

    def get_queryset(self):
        request_id = self.kwargs['pk']
        return RequestIdentityVariant.objects.filter(request__id=request_id, request__sender=self.request.user)

    def perform_create(self, serializer):
        request_id = self.kwargs['pk']
        request_instance = generics.get_object_or_404(Request, id=request_id, sender=self.request.user)
        serializer.save(request=request_instance)

class RequestSendRequestIdentityVariantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    User can see, edit and delete request identity variants for their sent-requests.
    """
    serializer_class = RequestSendRequestIdentityVariantSerializer
    permission_classes = [IsRequestSender]

    def get_queryset(self):
        request_id = self.kwargs['pk']
        return RequestIdentityVariant.objects.filter(request__id=request_id, request__sender=self.request.user)



# Request Receive views

class RequestReceiveListAPIView(generics.ListAPIView):
    """
    User can see received requests.
    """
    serializer_class = RequestReceiveListSerializer
    permission_classes = [IsRequestReceiver]

    # for list query where logged in user is the receiver only 
    def get_queryset(self):
        return Request.objects.filter(receiver=self.request.user)
    
class RequestReceiveDetailAPIView(generics.RetrieveAPIView):
    """
    User can see details of a received request.
    """
    serializer_class = RequestReceiveDetailSerializer
    permission_classes = [IsRequestReceiver]

    # for detail query where logged in user is the receiver only 
    def get_queryset(self):
        return Request.objects.filter(receiver=self.request.user)

class RequestReceiveRequestIdentityVariantListAPIView(generics.ListAPIView):
    """
    User can see request identity variants for their received requests.
    """
    serializer_class = RequestReceiveRequestIdentityVariantSerializer
    permission_classes = [IsRequestReceiver]

    def get_queryset(self):
        request_id = self.kwargs['pk']
        return RequestIdentityVariant.objects.filter(request__id=request_id, request__receiver=self.request.user)
    
class RequestReceiveRequestIdentityVariantDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    User can see and edit request identity variants for their received requests.
    """
    serializer_class = RequestReceiveRequestIdentityVariantDetailSerializer
    permission_classes = [IsRequestReceiver]
    lookup_url_kwarg = 'request_identity_variant_pk'

    def get_queryset(self):
        request_id = self.kwargs['pk']
        return RequestIdentityVariant.objects.filter(request__id=request_id, request__receiver=self.request.user)

class RequestReceiveAcceptAPIView(generics.UpdateAPIView):
    """
    User can accept their received request.
    """
    serializer_class = RequestReceiveStatusSerializer
    permission_classes = [IsRequestReceiver]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return Request.objects.filter(receiver=self.request.user)

    def perform_update(self, serializer):
        request_instance = self.get_object()
        serializer.save(request=request_instance, status=Request.Status.ACCEPTED)

class RequestReceiveDenyAPIView(generics.UpdateAPIView):
    """
    User can deny their received request.
    """
    serializer_class = RequestReceiveStatusSerializer
    permission_classes = [IsRequestReceiver]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return Request.objects.filter(receiver=self.request.user)

    def perform_update(self, serializer):
        request_instance = self.get_object()
        serializer.save(request=request_instance, status=Request.Status.DENIED)

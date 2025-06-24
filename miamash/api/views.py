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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    # for detail query where logged in user is the owner only 
    def get_queryset(self):
        return ProfileIdentityVariant.objects.filter(user=self.request.user)


# Request Send views 

class RequestSendListCreateAPIView(generics.ListCreateAPIView):
    """
    User can see sent-requests and create new ones.
    """
    serializer_class = RequestSendListCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    # for detail query where logged in user is the sender only 
    def get_queryset(self):
        return Request.objects.filter(sender=self.request.user)

class RequestSendRequestIdentityVariantListCreateAPIView(generics.ListCreateAPIView):
    """
    User can see and create request identity variants for their sent-requests.
    """
    serializer_class = RequestSendRequestIdentityVariantSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request_id = self.kwargs['pk']
        return RequestIdentityVariant.objects.filter(request__id=request_id, request__sender=self.request.user)

class RequestReceiveListAPIView(generics.ListAPIView):
    """
    User can see received requests.
    """
    serializer_class = RequestReceiveListSerializer
    permission_classes = [permissions.IsAuthenticated]

    # for list query where logged in user is the receiver only 
    def get_queryset(self):
        return Request.objects.filter(receiver=self.request.user)
    
class RequestReceiveDetailAPIView(generics.RetrieveAPIView):
    """
    User can see details of a received request.
    """
    serializer_class = RequestReceiveDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    # for detail query where logged in user is the receiver only 
    def get_queryset(self):
        return Request.objects.filter(receiver=self.request.user)

class RequestReceiveRequestIdentityVariantListAPIView(generics.ListAPIView):
    """
    User can see request identity variants for their received requests.
    """
    serializer_class = RequestReceiveRequestIdentityVariantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request_id = self.kwargs['pk']
        return RequestIdentityVariant.objects.filter(request__id=request_id, request__receiver=self.request.user)
    
class RequestReceiveRequestIdentityVariantDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    User can see and edit request identity variants for their received requests.
    """
    serializer_class = RequestReceiveRequestIdentityVariantDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'request_identity_variant_pk'

    def get_queryset(self):
        request_id = self.kwargs['pk']
        return RequestIdentityVariant.objects.filter(request__id=request_id, request__receiver=self.request.user)

class RequestReceiveAcceptAPIView(generics.UpdateAPIView):
    """
    User can accept their received request.
    """
    serializer_class = RequestReceiveStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return Request.objects.filter(receiver=self.request.user)

    def perform_update(self, serializer):
        request_instance = self.get_object()
        serializer.save(request=request_instance, status=Request.Status.DENIED)

# class SenderRequestViewSet(viewsets.ModelViewSet):
#     """
#     User can send requests to other users, see them, edit and delete. 
#     """
#     queryset = Request.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

#     # set dynamic serializer choice, so creation allows new username but not in update 
#     def get_serializer_class(self):
#         if self.action in ['update', 'partial_update']:
#             return SenderRequestUpdateSerializer
#         return SenderRequestSerializer

#     # only show request where user is the sender 
#     def get_queryset(self):
#         user = self.request.user
#         return Request.objects.filter(sender=user)
    
    

    
# class ReceiverRequestViewSet(viewsets.ModelViewSet):
#     """
#     User can see, create, edit and delete only their own requests as receiver.
#     """
#     queryset = Request.objects.all()
#     serializer_class = ReceiverRequestSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # only show request where user is the receiver
#     def get_queryset(self):
#         user = self.request.user
#         return Request.objects.filter(receiver=user)
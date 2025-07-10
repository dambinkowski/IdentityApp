from django.shortcuts import render, get_object_or_404
from core.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from api.views import *
from rest_framework import renderers
from rest_framework.response import Response


# Home view 
class HomeView(TemplateView):
    """
    Render welcome page for unauthenticated users
    """
    template_name = 'web/public/index.html'

    # over ride get that if user is authenticated, they should be redirect to dashboard
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

# Dashboard view
class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard page for authenticated users
    """
    template_name = 'web/private/dashboard.html'



# def prototype_request(request):
#     singleRequest = get_object_or_404(Request, pk=3)
#     return render(request,'web/prototype_request.html', {'SingleRequest':singleRequest})

# Profile Views
class ProfileIdentityVariantListCreateView(ProfileIdentityVariantListCreateAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variants
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/identity_variant.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        # get the queryset from the parent view
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'identity_variants': serializer.data})
    
class ProfileIdentityVariantDetailView(ProfileIdentityVariantDetailAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variants
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/identity_variant_detail.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'identity_variant': serializer.data})

    
# Send requests views   
class RequestSendListCreateView(RequestSendListCreateAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variants
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_send.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'send_requests': serializer.data})

class RequestSendDetailView(RequestSendDetailAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variants
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_send_detail.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'send_request': serializer.data})
    
class RequestSendRequestIdentityVariantListCreateView(RequestSendRequestIdentityVariantListCreateAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variants
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_send_request_identity_variant.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'request_identity_variants': serializer.data}) 
    
class RequestSendRequestIdentityVariantDetailView(RequestSendRequestIdentityVariantDetailAPIView):   
    """
    Uses api endpoint to render html template page with Profile Identity Variants
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_send_request_identity_variant_detail.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'request_identity_variant': serializer.data})
    

# Receive requests views
class RequestReceiveListView(RequestReceiveListAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variants
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_receive.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'receive_requests': serializer.data})

class RequestReceiveDetailView(RequestReceiveDetailAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variant details
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_receive_detail.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'receive_request': serializer.data})
    
class RequestReceiveRequestIdentityVariantListView(RequestReceiveRequestIdentityVariantListAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variant details
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_receive_request_identity_variant.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'request_identity_variants': serializer.data})
    
class RequestReceiveRequestIdentityVariantDetailView(RequestReceiveRequestIdentityVariantDetailAPIView):
    """
    Uses api endpoint to render html template page with Profile Identity Variant details
    """
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'web/private/request_receive_request_identity_variant_detail.html'

    # ovver ride get method to return dict 
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'request_identity_variant': serializer.data})
    
class RequestReceiveAcceptView(RequestReceiveAcceptAPIView):
    #  I don't think i will have html template for this view
    # but we will see i propable need functionaliy that once posted redirect or someting 

    pass

class RequestReceiveDenyView(RequestReceiveDenyAPIView):
    # same here 
    pass
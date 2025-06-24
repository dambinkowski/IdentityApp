from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

# create router instance 
router = DefaultRouter()
# Register the ProfileIdentityVariantViewSet with the router
router.register(r'profile-identity-variant', ProfileIdentityVariantViewSet, basename='profile-identity-variant')
# router.register(r'request-send', SenderRequestViewSet, basename='sender-request')
# router.register(r'request-recieve', ReceiverRequestViewSet, basename='receiver-request')




urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    # profile identity variant management 
    path('', include(router.urls)),

    # send requests management
    path('request/send/', RequestSendListCreateAPIView.as_view(), name='request-send-list-create'),
    path('request/send/<int:pk>/', RequestSendDetailAPIView.as_view(), name='request-send-detail'),
    path('request/send/<int:pk>/request-identity-variant/', RequestSendRequestIdentityVariantListCreateAPIView.as_view(), name='request-send-request-identity-variant-list-create'),
    path('request/send/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/', RequestSendRequestIdentityVariantDetailAPIView.as_view(), name='request-send-request-identity-variant-detail'),
    # received requests management 
    path('request/receive/', RequestReceiveListAPIView.as_view(), name='request-receive-list'),
    path('request/receive/<int:pk>/', RequestReceiveDetailAPIView.as_view(), name='request-receive-detail'),
    path('request/receive/<int:pk>/request-identity-variant/', RequestReceiveRequestIdentityVariantListAPIView.as_view(), name='request-receive-request-identity-variant-list'),
    path('request/receive/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/', RequestReceiveRequestIdentityVariantDetailAPIView.as_view(), name='request-receive-request-identity-variant-detail'),
]


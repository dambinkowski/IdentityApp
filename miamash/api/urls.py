from .views import *
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    # registration and authentication
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),

    # profile identity variant management 
    path('profile/identity-variant/', ProfileIdentityVariantListCreateAPIView.as_view(), name='profile-identity-variant-list-create'),
    path('profile/identity-variant/<int:pk>/', ProfileIdentityVariantDetailAPIView.as_view(), name='profile-identity-variant-detail'),

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
    path('request/receive/<int:pk>/accept/', RequestReceiveAcceptAPIView.as_view(), name='request-receive-accept'),
    path('request/receive/<int:pk>/deny/', RequestReceiveDenyAPIView.as_view(), name='request-receive-deny'),

    # API documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


from django.urls import path, include
from .views import *


urlpatterns = [
    # public views 
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),

    # authenticated user views
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # profile identity variant management 
    # list of variants 
    path('profile/identity-variant/', ProfileIdentityVariantListView.as_view(), name='profile-identity-variant-list'),
    # add new variant
    path('profile/identity-variant/add/', ProfileIdentityVariantCreateView.as_view(), name='profile-identity-variant-create'),
    # # detail view of a variant
    path('profile/identity-variant/<int:pk>/', ProfileIdentityVariantDetailView.as_view(), name='profile-identity-variant-detail'),
    # # edit profile identity variant     
    path('profile/identity-variant/<int:pk>/edit/', ProfileIdentityVariantUpdateView.as_view(), name='profile-identity-variant-update'),
    # # delete profile identity variant
    path('profile/identity-variant/<int:pk>/delete/', ProfileIdentityVariantDeleteView.as_view(), name='profile-identity-variant-delete'),

    # # send requests management
    # list of send requests 
    path('request/send/', RequestSendListView.as_view(), name='request-send-list'),
    # create new request 
    path('request/send/create/', RequestSendCreateView.as_view(), name='request-send-create'),
    # request detail
    path('request/send/<int:pk>/', RequestSendDetailView.as_view(), name='request-send-detail'),
    # request update
    path('request/send/<int:pk>/edit/', RequestSendUpdateView.as_view(), name='request-send-update'),
    # request delete
    path('request/send/<int:pk>/delete/', RequestSendDeleteView.as_view(), name='request-send-delete'),
    # create new request identity variant for the request
    path('request/send/<int:pk>/request-identity-variant/create/', RequestSendRequestIdentityVariantCreateView.as_view(), name='request-send-request-identity-variant-create'),
    # request identity variant detail 
    path('request/send/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/', RequestSendRequestIdentityVariantDetailView.as_view(), name='request-send-request-identity-variant-detail'),
    # request identity variant update
    path('request/send/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/edit/', RequestSendRequestIdentityVariantUpdateView.as_view(), name='request-send-request-identity-variant-update'),
    # request identity variant delete
    path('request/send/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/delete/', RequestSendRequestIdentityVariantDeleteView.as_view(), name='request-send-request-identity-variant-delete'),

    # # # received requests management
    # list of received requests
    path('request/receive/', RequestReceiveListView.as_view(), name='request-receive-list'),
    # request detials 
    path('request/receive/<int:pk>/', RequestReceiveDetailView.as_view(), name='request-receive-detail'),
    # request identity variant detail
    path('request/receive/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/', RequestReceiveRequestIdentityVariantDetailView.as_view(), name='request-receive-request-identity-variant-detail'),
    # request identity variant update / link to the existing identity profile variant 
    path('request/receive/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/edit/', RequestReceiveRequestIdentityVariantUpdateView.as_view(), name='request-receive-request-identity-variant-update'),
    # accept request  
    path('request/receive/<int:pk>/accept/', RequestReceiveAcceptView.as_view(), name='request-receive-accept'),
    # deny request 
    path('request/receive/<int:pk>/deny/', RequestReceiveDenyView.as_view(), name='request-receive-deny'), 

]
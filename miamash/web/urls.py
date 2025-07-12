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
    # path('request/send/', RequestSendListCreateView.as_view(), name='request-send-list-create'),
    # path('request/send/<int:pk>/', RequestSendDetailView.as_view(), name='request-send-detail'),
    # path('request/send/<int:pk>/request-identity-variant/', RequestSendRequestIdentityVariantListCreateView.as_view(), name='request-send-request-identity-variant-list-create'),
    # path('request/send/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/', RequestSendRequestIdentityVariantDetailView.as_view(), name='request-send-request-identity-variant-detail'),

    # # # received requests management 
    # path('request/receive/', RequestReceiveListView.as_view(), name='request-receive-list'),
    # path('request/receive/<int:pk>/', RequestReceiveDetailView.as_view(), name='request-receive-detail'),
    # path('request/receive/<int:pk>/request-identity-variant/', RequestReceiveRequestIdentityVariantListView.as_view(), name='request-receive-request-identity-variant-list'),
    # path('request/receive/<int:pk>/request-identity-variant/<int:request_identity_variant_pk>/', RequestReceiveRequestIdentityVariantDetailView.as_view(), name='request-receive-request-identity-variant-detail'),
    # path('request/receive/<int:pk>/accept/', RequestReceiveAcceptView.as_view(), name='request-receive-accept'),
    # path('request/receive/<int:pk>/deny/', RequestReceiveDenyView.as_view(), name='request-receive-deny'), 

]
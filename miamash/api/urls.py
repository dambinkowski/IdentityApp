from rest_framework.routers import DefaultRouter
from .views import ProfileIdentityVariantViewSet
from django.urls import path, include

# create router instance 
router = DefaultRouter()
# Register the ProfileIdentityVariantViewSet with the router
router.register(r'profile-identity-variant', ProfileIdentityVariantViewSet, basename='profile-identity-variant')





urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('', include(router.urls))
]


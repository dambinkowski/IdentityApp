from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('prototype/request', views.prototype_request, name='prototype_request')
]
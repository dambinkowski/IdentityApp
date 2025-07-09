from django.urls import path, include
from . import views 


urlpatterns = [
    # public views 
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),

    # authenticated user views
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

]
from django.urls import path
from . import views 

urlpatterns = [
    path('test/<int:pk>/', views.TestView.as_view(), name='test')
]
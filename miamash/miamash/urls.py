from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin page 
    path('admin/', admin.site.urls),
    # api app
    path('api/', include('api.urls')),
    # web app 
    path('', include('web.urls')),
    
]

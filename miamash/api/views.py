from rest_framework.generics import RetrieveAPIView
from .serializer import *
from core.models import *
from django.shortcuts import get_object_or_404

class TestView(RetrieveAPIView):
    serializer_class = RequestPrototypeSerializer
    queryset = Request.objects.select_related('sender', 'receiver')
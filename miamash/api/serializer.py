from rest_framework import serializers
from core.models import Request

class RequestPrototypeSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    receiver = serializers.CharField(source='receiver.username')
    class Meta:
        model = Request
        fields=['sender', 'receiver', 'status', 'request_reasoning']
from rest_framework import serializers
from core.models import ProfileIdentityVariant, Request, RequestIdentityVariant

class ProfileIdentityVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIdentityVariant
        fields = ['id', 'label', 'context', 'variant']
        read_only_fields = ['id']
        


class RequestSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username', read_only=True)
    
    class Meta:
        model = Request
        fields = '__all__'
        read_only_fields = ['id', 'sender', 'created_at', 'created_at', 'status']
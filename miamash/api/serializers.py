from rest_framework import serializers
from core.models import ProfileIdentityVariant, Request, RequestIdentityVariant

class ProfileIdentityVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIdentityVariant
        fields = ['id', 'label', 'context', 'variant']
        read_only_fields = ['id']


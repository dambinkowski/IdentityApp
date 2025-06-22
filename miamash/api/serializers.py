from rest_framework import serializers
from core.models import ProfileIdentityVariant, Request, RequestIdentityVariant
from django.contrib.auth import get_user_model

# get current active model 
User = get_user_model()

class ProfileIdentityVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIdentityVariant
        fields = ['id', 'label', 'context', 'variant']
        read_only_fields = ['id']
        


class SenderRequestSerializer(serializers.ModelSerializer):
    receiver_username = serializers.CharField(source='receiver.username') # allow to use username instead of id
    
    class Meta:
        model = Request
        fields = ['id', 'receiver_username', 'request_reasoning', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'status']
    
    # creating new Request
    def create(self, validated_data):
        #  get receiver username from validated data  
        receiver_username = validated_data['receiver']['username']
        # get user object if exists, else raise error
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"Username: '{receiver_username}' does not exist")
        # to get sender use .user attribute, from DRF Request object
        # using server data for who sender is (not client data) for security  
        sender = self.context['request'].user
        # create new Request instance
        request_instance = Request.objects.create(
            sender=sender,
            receiver=receiver,
            request_reasoning=validated_data.get('request_reasoning', '')
        )
        # return created instance 
        return request_instance

class ReceiverRequestSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Request
        fields = '__all__'
        read_only_fields = ['id', 'sender', 'created_at', 'status']
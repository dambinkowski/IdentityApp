from rest_framework import serializers
from core.models import ProfileIdentityVariant, Request, RequestIdentityVariant
from django.contrib.auth.models import User

# Profil Identity Variant Serializers
class ProfileIdentityVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileIdentityVariant
        fields = ['id', 'label', 'context', 'variant']
        read_only_fields = ['id']
        


# Request Send Serializers

class RequestSendListCreateSerializer(serializers.ModelSerializer):
    # list usernames instead of users ids  
    receiver_username = serializers.CharField(source='receiver.username') 
    
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
    
class RequestSendRequestIdentityVariantSerializer(serializers.ModelSerializer):
    user_provided_variant = serializers.CharField(source='profile_link.variant', read_only=True)
    class Meta:
        model = RequestIdentityVariant
        fields = ['id', 'label', 'context', 'user_provided_variant']
        read_only_fuields = ['id', 'user_variant']
    
    def create(self, validated_data):
        # ensure request belongs to the sender (current user)
        request_instance = validated_data['request']
        if request_instance.sender != self.context['request'].user:
            raise serializers.ValidationError("You can only add identity variants to your own requests.")
        return super().create(validated_data)
    

class RequestSendDetailSerializer(serializers.ModelSerializer):
    # make receiver username read-only not allowing to change in update
    receiver_username = serializers.CharField(source='receiver.username', read_only=True) 
    # include nested request-identity-variants related to this request
    request_identity_variants = RequestSendRequestIdentityVariantSerializer(many=True, read_only=True)
    class Meta:
        model = Request
        fields = ['id', 'receiver_username', 'request_reasoning', 'status', 'created_at', 'request_identity_variants']
        read_only_fields = ['id', 'receiver_username', 'created_at', 'status', 'request_identity_variants']
    
    def update(self, instance, validated_data):
        # only allow updating request_reasoning 
        instance.request_reasoning = validated_data.get('request_reasoning', instance.request_reasoning)
        instance.save()
        return instance



# Request Receive Serializers
class RequestReceiveListSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True) 
    
    class Meta:
        model = Request
        fields = ['id', 'sender_username', 'request_reasoning', 'status', 'created_at']
        read_only_fields = ['id', 'sender_username', 'request_reasoning','status','created_at']
    
class RequestReceiveRequestIdentityVariantSerializer(serializers.ModelSerializer):
    user_provided_variant = serializers.CharField(source='profile_link.variant', read_only=True)
    class Meta:
        model = RequestIdentityVariant
        fields = ['id', 'label', 'context', 'user_provided_variant']
        read_only_fuields = ['id', 'label', 'context']

class RequestReceiveDetailSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True) 
    # include nested request-identity-variants related to this request
    request_identity_variants = RequestReceiveRequestIdentityVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Request
        fields = ['id', 'sender_username', 'request_reasoning', 'status', 'created_at', 'request_identity_variants']
        read_only_fields = ['id', 'sender_username', 'created_at', 'status', 'request_identity_variants']

class RequestReceiveRequestIdentityVariantDetailSerializer(serializers.ModelSerializer):
    user_provided_variant = serializers.CharField(source='profile_link.variant', read_only=True)
    
    class Meta:
        model = RequestIdentityVariant
        fields = ['id', 'label', 'context', 'profile_link', 'user_provided_variant']
        read_only_fields = ['id', 'label', 'context', 'user_provided_variant']
    
class RequestReceiveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['status']
        read_only_fields = ['status']
    



# class SenderRequestSerializer(serializers.ModelSerializer):
#     receiver_username = serializers.CharField(source='receiver.username') # allow to use username instead of id
    
#     class Meta:
#         model = Request
#         fields = ['id', 'receiver_username', 'request_reasoning', 'status', 'created_at']
#         read_only_fields = ['id', 'created_at', 'status']
    

#     # creating new Request
#     def create(self, validated_data):
#         #  get receiver username from validated data  
#         receiver_username = validated_data['receiver']['username']
#         # get user object if exists, else raise error
#         try:
#             receiver = User.objects.get(username=receiver_username)
#         except User.DoesNotExist:
#             raise serializers.ValidationError(f"Username: '{receiver_username}' does not exist")
#         # to get sender use .user attribute, from DRF Request object
#         # using server data for who sender is (not client data) for security  
#         sender = self.context['request'].user
#         # create new Request instance
#         request_instance = Request.objects.create(
#             sender=sender,
#             receiver=receiver,
#             request_reasoning=validated_data.get('request_reasoning', '')
#         )
#         # return created instance 
#         return request_instance
    
# class SenderRequestUpdateSerializer(serializers.ModelSerializer):
#     receiver_username = serializers.CharField(source='receiver.username', read_only=True) # read-only for update
    
#     class Meta:
#         model = Request
#         fields = ['id', 'receiver_username', 'request_reasoning', 'status', 'created_at']
#         read_only_fields = ['id', 'receiver_username', 'created_at', 'status']
    
#     def update(self, instance, validated_data):
#         # only allow updating request_reasoning 
#         instance.request_reasoning = validated_data.get('request_reasoning', instance.request_reasoning)
#         instance.save()
#         return instance

# class ReceiverRequestSerializer(serializers.ModelSerializer):
#     sender = serializers.CharField(source='sender.username', read_only=True)
    
#     class Meta:
#         model = Request
#         fields = '__all__'
#         read_only_fields = ['id', 'sender', 'created_at', 'status']
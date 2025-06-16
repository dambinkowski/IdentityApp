from django.db import models
from django.contrib.auth.models import User 

class ProfileIdentityVariant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='identity_variants')
    label = models.CharField(max_length=50)
    context = models.TextField(blank=True)
    variant = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} / {self.label} / {self.variant}"

class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_recieved')
    request_reasoning = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    def __str__(self):
        return f"FROM:{self.sender.username} / TO:{self.receiver.username} / {self.request_reasoning}"

class RequestIdentityVariant(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='identity_variants')
    label = models.CharField(max_length=50)
    context = models.TextField(blank=True)
    profile_link = models.ForeignKey(ProfileIdentityVariant,null=True, blank=True, on_delete=models.SET_NULL) 
    def __str__(self):
        return f"{self.label} / {self.context} / {self.profile_link}"
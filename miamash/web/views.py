from django.shortcuts import render, get_object_or_404
from core.models import *
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request, 'web/home.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/sign_up.html'
    success_url = '/dashboard/'

def dashboard(request):
    return render(request, 'web/dashboard.html')


def prototype_request(request):
    singleRequest = get_object_or_404(Request, pk=3)
    return render(request,'web/prototype_request.html', {'SingleRequest':singleRequest})
from django.shortcuts import render, get_object_or_404
from core.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect


# Home view 
class HomeView(TemplateView):
    """
    Render the welcome page with the links to sign up and log in.
    Any user can access this page.

    """
    template_name = 'web/public/index.html'

    # over ride get that if user is authenticated, they should be redirect to dashboard
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

# Dashboard view
class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Render the dashboard page for authenticated users.
    """
    template_name = 'web/private/dashboard.html'



def prototype_request(request):
    singleRequest = get_object_or_404(Request, pk=3)
    return render(request,'web/prototype_request.html', {'SingleRequest':singleRequest})

from core.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect
from .forms import ProfileIdentityVariantForm
from django.urls import reverse_lazy
from .permissions import ProfileIdentityVariantOwnerMixin


# Home view 
class HomeView(TemplateView):
    """
    View renders HTML home page for unauthenticated users, authenticated users will be redirected to dashboard view 
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
    View renders HTML page for authenticated users, entry point for pathway of actions. 
    Provides links to manage profile identity variants, send requests, and receive requests.
    """
    template_name = 'web/private/dashboard.html'

# Profile Identity variants views, list, create, detail, update, delete
class ProfileIdentityVariantListView(ProfileIdentityVariantOwnerMixin, ListView):
    """
    View gets all ProfileIdentityVariant objects for the authenticated user from the database
    then Renders HTML page with the list of those fetched objects.
    """
    template_name = 'web/private/profile_identity_variant_list.html'
    context_object_name = 'profile_identity_variants'


class ProfileIdentityVariantCreateView(ProfileIdentityVariantOwnerMixin, CreateView):
    """ 
    View renders HTML page with the form to create a new ProfileIdentityVariant object.
    When form is submitted, view proccesse, hard codes the user to cerdentials of the logged-in user,
    and saves the new ProfileIdentityVariant object to the database and redirects to the list view.
    """
    form_class = ProfileIdentityVariantForm
    template_name = 'web/private/profile_identity_variant_create.html'
    success_url = reverse_lazy('profile-identity-variant-list')

    def form_valid(self, form):
        # process user owner server side, by hardcoding the user to the logged-in user
        # this is to ensure that the user cannot create a variant for another user
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileIdentityVariantDetailView(ProfileIdentityVariantOwnerMixin, DetailView):
    """
    View gets ProfileIdentityVariant pk from the URL, then queries the database filtering by 
    user credentials that come from server side using login credentials, then in those avaible resources
    looks for match from the URL pk. Once found it will render HTML page with details otheriwe it will return 404. 
    """
    template_name = 'web/private/profile_identity_variant_detail.html'
    context_object_name = 'profile_identity_variant'


class ProfileIdentityVariantUpdateView(ProfileIdentityVariantOwnerMixin, UpdateView):
    """
    View gets ProfileIdentityVariant pk from the URL, then queries the database filtering by 
    user credentials that come from server side using login credentials, then in those available resources
    looks for match from the URL pk. Once found it will render HTML page with the form with data from database loaded in there
    now user can update the form and submit it, wich will then validate the data, create object and save it to the database. 
    After succesful update user will be redirected to list view of all ProfileIdentityVariant.
    """
    form_class = ProfileIdentityVariantForm
    template_name = 'web/private/profile_identity_variant_update.html'
    success_url = reverse_lazy('profile-identity-variant-list')


class ProfileIdentityVariantDeleteView(ProfileIdentityVariantOwnerMixin, DeleteView):
    """
    View reuses detail tempalet, uses the same safety logic to maintain server side security of using user credentials to filter
    query set, then it allows post form method for aleready used template in detail view, this way detail page can be used for both
    detail view and delete view. User can delete ProfileIdentityVariant object by clicking on the delete button in the detail view template
    So this extentds detail view get functionality and allows post to delete the object.
    """
    context_object_name = 'profile_identity_variant'
    template_name = 'web/private/profile_identity_variant_detail.html'
    success_url = reverse_lazy('profile-identity-variant-list')


# request send 


# request receive
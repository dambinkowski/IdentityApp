from django.http import HttpRequest
from django.http.response import HttpResponse
from core.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect
from .forms import *
from django.urls import reverse_lazy
from .permissions import * 


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
class ProfileIdentityVariantListView(ProfileIdentityVariantOwnerPermissionMixin, ListView):
    """
    View gets all ProfileIdentityVariant objects for the authenticated user from the database
    then Renders HTML page with the list of those fetched objects.
    """
    template_name = 'web/private/profile_identity_variant_list.html'
    context_object_name = 'profile_identity_variants'


class ProfileIdentityVariantCreateView(ProfileIdentityVariantOwnerPermissionMixin, CreateView):
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


class ProfileIdentityVariantDetailView(ProfileIdentityVariantOwnerPermissionMixin, DetailView):
    """
    View gets ProfileIdentityVariant pk from the URL, then queries the database filtering by 
    user credentials that come from server side using login credentials, then in those avaible resources
    looks for match from the URL pk. Once found it will render HTML page with details otheriwe it will return 404. 
    """
    template_name = 'web/private/profile_identity_variant_detail.html'
    context_object_name = 'profile_identity_variant'


class ProfileIdentityVariantUpdateView(ProfileIdentityVariantOwnerPermissionMixin, UpdateView):
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


class ProfileIdentityVariantDeleteView(ProfileIdentityVariantOwnerPermissionMixin, DeleteView):
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
class RequestSendListView(RequestSenderPermissionMixin, ListView):
    """
    View fetches Request objects from database where sever side user logged in credential
    match the sender field of the Request object. Then renders HTML page with that list. 
    """
    template_name = 'web/private/request_send_list.html'
    context_object_name = 'send_requests'

class RequestSendCreateView(RequestSenderPermissionMixin, CreateView):
    """
    View renders HTML page with form for user to fill out information to create a new request, 
    with exception of setting the sender, that part backend handles by hacroded credentials used
    from logged in session. 
    """
    form_class = RequestSendForm
    template_name = 'web/private/request_send_create.html'
    success_url = reverse_lazy('request-send-list')

    def form_valid(self, form):
        # process user owner server side, by hardcoding the sender to the logged-in user
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
    # i will want it to redirect to create request variant after 

class RequestSendDetailView(RequestSenderPermissionMixin, DetailView):
    """
    View gets Request id - pk from the URL, then querie the database filtering by that pk 
    and logged in user credentails, then if finds a match it renders HTML page with details.
    It also shows RequestIdentityVariant lits for that request, and allows user to create new RequestIdentityVariant
    for that request.
    """
    template_name = 'web/private/request_send_detail.html'
    context_object_name = 'send_request'

    def get_context_data(self, **kwargs):
        """
        Override get_context_data to add RequestIdentityVariant objects
        """
        context = super().get_context_data(**kwargs) 
        requestObject = self.get_object() # Request as model, not django request object 
        # add to context, pylance does not know that passed object is Request, that has request_identity_variants, so type: ignore
        context['request_identity_variants'] = requestObject.request_identity_variants.all() # type: ignore
        return context

class RequestSendUpdateView(RequestSenderPermissionMixin, UpdateView):
    """
    View gets Request id - pk from URL, then checks if logged in user has permission for CRUD, then it 
    renders HTML pafe with prepoulated fields from data, allowing user to update, not exposing sender field that has already been set 
    in creation server side 
    """
    form_class = RequestSendUpdateForm
    template_name = 'web/private/request_send_update.html'

    def get_success_url(self):
        return reverse_lazy('request-send-detail', kwargs={'pk': self.get_object().pk})


class RequestSendDeleteView(RequestSenderPermissionMixin, DeleteView):
    """
    Vieg gets request pk from URL, then checks if logged in user has permission via mixin, then delets the Request instance from the database.
    It uses detail view template
    """
    context_object_name = 'send_request'
    template_name = 'web/private/request_send_detail.html'
    success_url = reverse_lazy('request-send-list')

class RequestSendRequestIdentityVariantCreateView(RequestSenderRequestIdentityVariantPermissionMixin, CreateView):
    """
    View gets post request and creates RequestIdentityVariant for the Request. 
    """
    template_name = 'web/private/request_send_request_identity_variant_create.html'
    form_class = RequestSendRequestIdentityVariantForm

    def get_success_url(self):
        # request_object is set in mixin permission, during dispatch
        return reverse_lazy('request-send-detail', kwargs={'pk': self.request_send.pk})

    def form_valid(self, form):
        # write parent id (Request) server side, to insure user only creates RequestIdentityVariant for the Request they are senders 
        # insuring that user is sender of this Request is checked in the mixin, but now hardcode saving it to the form instance
        form.instance.request = self.request_send
        return super().form_valid(form)

class RequestSendRequestIdentityVariantDetailView(RequestSenderRequestIdentityVariantPermissionMixin, DetailView):
    """
    View gets RequestIdentityVariant id - pk from the URL, checks if user is a sender of parent object Request, 
    then queries db for that instance, Renders HTML with info or shows 404 if not found.
    """
    template_name = 'web/private/request_send_request_identity_variant_detail.html'
    context_object_name = 'request_identity_variant'

class RequestSendRequestIdentityVariantUpdateView(RequestSenderRequestIdentityVariantPermissionMixin, UpdateView):
    """
    View gets id - pk from URL, then checks if there is Request with that id availbale for that user based on login credentiatls using mixin, 
    then it gets RequestIdentityVariant object from the database, and renders HTML page with form prepopulated with data from that object. 
    User can update the informations and submit the form then view will validate and save to the database, and redirect Request detail view. 
    """
    form_class = RequestSendRequestIdentityVariantForm
    template_name = 'web/private/request_send_request_identity_variant_update.html'

    def get_success_url(self):
        return reverse_lazy('request-send-detail', kwargs={'pk': self.request_send.pk})

class RequestSendRequestIdentityVariantDeleteView(RequestSenderRequestIdentityVariantPermissionMixin, DeleteView):
    """
    View uses the same HTML template as RequestSendRequestIdentityVariantDetailView, and takes care of POST request 
    to dele the RequstIdentityVariant object from the database, first insures that user is a sender of the parent Request object,
    upon success it redirects to the RequestSendDetailView.
    """
    context_object_name = 'request_identity_variant'
    template_name = 'web/private/request_send_request_identity_variant_detail.html'

    def get_success_url(self):
        return reverse_lazy('request-send-detail', kwargs={'pk': self.request_send.pk})

# request receive

class RequestReceiveListView(RequestReceiverPermissionMixin, ListView):
    """
    View fetches Request objects from database where server side user logged in credential
    match the receiver field of the Request object. Then renders HTML page with that list. 
    """
    template_name = 'web/private/request_receive_list.html'
    context_object_name = 'received_requests'

class RequestReceiveDetailView(RequestReceiverPermissionMixin, DetailView):
    """
    View gets Request id - pk from the URL, then queries the database filtering by that pk 
    and logged in user credentails, then if finds a match it renders HTML page with details.
    It also shows RequestIdentityVariant lists for that request, and allows user to update RequestIdentityVariant
    for that request.
    """
    template_name = 'web/private/request_receive_detail.html'
    context_object_name = 'receive_request'

    def get_context_data(self, **kwargs):
        """
        Override get_context_data to add RequestIdentityVariant objects
        """
        context = super().get_context_data(**kwargs) 
        requestObject = self.get_object() # Request as model, not django request object 
        # add to context, pylance does not know that passed object is Request, that has request_identity_variants, so type: ignore
        context['request_identity_variants'] = requestObject.request_identity_variants.all() # type: ignore
        return context

class RequestReceiveRequestIdentityVariantDetailView(RequestReceiverRequestIdentityVariantPermissionMixin, DetailView):
    """
    View gets RequestIdentityVariant id - pk from the URL, checks if user is a receiver of parent object Request, 
    then queries db for that instance, Renders HTML with info or shows 404 if not found.
    """
    template_name = 'web/private/request_receive_request_identity_variant_detail.html'
    context_object_name = 'request_identity_variant'

class RequestReceiveRequestIdentityVariantUpdateView(RequestReceiverRequestIdentityVariantPermissionMixin, UpdateView):
    """
    View gets id - pk from URL, then checks if there is Request with that id available for that user based on login credentials using mixin, 
    then it gets RequestIdentityVariant object from the database, and renders HTML page with form prepopulated with data from that object. 
    User can update the information and submit the form then view will validate and save to the database, and redirect Request detail view. 
    """
    form_class = RequestReceiveRequestIdentityVariantForm
    template_name = 'web/private/request_receive_request_identity_variant_update.html'

    def get_success_url(self):
        return reverse_lazy('request-receive-detail', kwargs={'pk': self.request_receive.pk})
    
class RequestReceiveAcceptView(RequestReceiverPermissionMixin, View):
    """
    View gets Request id - pk from the URL, checks if user is a receiver of that Request, then it updates the status of that Request to 'accepted'.
    After that it redirects to the RequestReceiveDetailView.
    """
    def post(self, request, *args, **kwargs):
        self.request_receive.status = 'accepted'  # type: ignore
        self.request_receive.save()  # type: ignore
        return redirect('request-receive-detail', pk=self.request_receive.pk)  # type: ignore


class RequestReceiveDenyView(RequestReceiverPermissionMixin, View):
    """
    View gets Request id - pk from the URL, checks if user is a receiver of that Request, then it updates the status of that Request to 'denied'.
    After that it redirects to the RequestReceiveDetailView.
    """
    def post(self, request, *args, **kwargs):
        self.request_receive.status = 'denied'  # type: ignore
        self.request_receive.save()  # type: ignore
        return redirect('request-receive-detail', pk=self.request_receive.pk)  # type: ignore
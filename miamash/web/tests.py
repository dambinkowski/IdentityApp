from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import ProfileIdentityVariant, Request, ProfileIdentityVariant, RequestIdentityVariant

User = get_user_model() # set User model

## REGISTRATION AND LOGIN ## 
class AuthenticationTests(TestCase):
    def setUp(self):
            # Create valid user credentials
            self.valid_username = 'Johny'
            self.valid_password = 'test123123'
            self.valid_email = 'johny@example.com'
            # Create a user with valid credentials
            self.user = User.objects.create_user(
                username=self.valid_username,
                email=self.valid_email,
                password=self.valid_password,
            )  

            self.valid_user_login_data = {
                'login': 'Johny',
                'password': 'test123123',
            }
            
            self.wrong_user_login_password_data = {
                'username': 'Johny',
                'password': 'wrongpassword',
            }   

            self.wrong_user_login_username_data = {
                'username': 'WrongUser',
                'password': 'test123123',
            }

            # Create valid user registration data
            self.valid_user_registration_data = {
                'username': 'Michael',
                'email': 'michael@example.com',
                'password1': 'test123123',
                'password2': 'test123123',
            }
            # Create invalid user registration data
            self.invalid_user_registration_data = {
                'username': '',
                'email': '',
                'password1': '',
                'password2': '',
            }

            # Define URLs for registration, login, and logout
            self.register_url = reverse('account_signup')
            self.login_url = reverse('account_login')
            self.logout_url = reverse('account_logout')
            self.dashboard_url = reverse('dashboard')

    # user can log in  with good credentials
    def test_user_can_login_with_good_credentials(self):
        # post login 
        response = self.client.post(self.login_url, self.valid_user_login_data)
        # response should be 302 redirect to dashboard 
        self.assertEqual(response.status_code, 302)
        # check if redirects to dashboard 
        self.assertRedirects(response, self.dashboard_url)
        # check if dashboard has username in welcome message 

    # dashboard loads correctly for logged in user 
    def test_user_dashboard_after_login(self):
        # post login 
        response = self.client.post(self.login_url, self.valid_user_login_data)
        # follow redirect 
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        # make sure dashboard shows for correct user by checking username  
        self.assertContains(response, f"Hello {self.valid_username}") 
    
    #  user cannot log in with bad credentials
    def test_user_cannot_login_with_bad_credentials(self):
        # post login wrong password
        response = self.client.post(self.login_url, self.wrong_user_login_password_data)
        # repsonse should be 200 reload the form page with error, not 302 redirect  
        self.assertEqual(response.status_code, 200)

        # post login wrong username
        response = self.client.post(self.login_url, self.wrong_user_login_username_data)
        # response should be 200 reaload the form page with error, not 302 redirect 
        self.assertEqual(response.status_code, 200)


    # user can log out 
    def test_user_can_logout(self):
        # post login
        self.client.post(self.login_url, self.valid_user_login_data)
        # logout 
        self.client.post(self.logout_url)
        # now checked if truly logged out, should redirect to login page when trying to access dashboard 
        response = self.client.get(self.dashboard_url)
        # should redirect login page 
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url) # type: ignore 

    # user can register with good credentials
    def test_user_can_register_with_good_credentials(self):
        # post register with valid data, redirect302 should happen to dashboard 
        response = self.client.post(self.register_url, self.valid_user_registration_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)
        # then dashboard should load, with correct hello msg 
        response = self.client.get(response.url) # type: ignore
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Hello {self.valid_user_registration_data['username']}") 

    # test if user is unique
    def test_user_cannot_register_with_existing_username(self):
    # Try to register with an existing username
        response = self.client.post(self.register_url, {
            'username': self.valid_username,  # Already exists in setUp
            'email': 'john1@example.com',     # lets not repeat email 
            'password1': self.valid_password,
            'password2': self.valid_password,
        })
        # The response should be 200 (form re-rendered with error, not 400)
        self.assertEqual(response.status_code, 200)
        # just to make sure url should still be signup
        self.assertIn('/accounts/signup/', self.register_url)

    # user cannot register with bad credentials
    def test_user_cannot_register_with_bad_credentials(self):
        # post register with invalid data
        response = self.client.post(self.register_url, self.invalid_user_registration_data)
        # response should be 200 reload the page 
        self.assertEqual(response.status_code, 200)
        # page should still be signup 
        self.assertIn('/accounts/signup/', self.register_url)
        

## PROFILE IDENTITY VARIANTS ## 
class ProfileIdentityVariantsTests(TestCase):
    def setUp(self):
        # Create valid user credentials
        self.valid_username = 'Johny'
        self.valid_password = 'test123123'
        self.valid_email = 'johny@example.com'
        # Create a user with valid credentials
        self.user = User.objects.create_user(
            username=self.valid_username,
            email=self.valid_email,
            password=self.valid_password,
        )  

        self.valid_user_login_data = {
            'username': 'Johny',
            'password': 'test123123',
        }

        self.valid_identity_variant_data = {
            'label': 'First Name',
            'context': 'Firstname also known as given name.',
            'variant': 'John',
        }

        self.valid_updated_identity_variant_data = {
            'label': 'Polish firstname',
            'context': 'This has to be Polish letters first name.',
            'variant': 'Janusz',
        }

        # Define URLs for profile identity variants
        self.profile_identity_variant_list_url = reverse('profile-identity-variant-list')
        self.profile_identity_variant_create_url = reverse('profile-identity-variant-create')
        self.profile_identity_variant_detail_url = lambda pk: reverse('profile-identity-variant-detail', args=[pk])
        self.profile_identity_variant_update_url = lambda pk: reverse('profile-identity-variant-update', args=[pk])
        self.profile_identity_variant_delete_url = lambda pk: reverse('profile-identity-variant-delete', args=[pk])

    # user can create their profile identity variants
    def test_user_can_create_their_identity_variants(self):
        # log in the user
        self.client.login(username=self.valid_username, password=self.valid_password)
        # post create profile identity variant
        create_response = self.client.post(self.profile_identity_variant_create_url, self.valid_identity_variant_data)
        # respond should be 302 redirect to list view
        self.assertEqual(create_response.status_code, 302)
        self.assertRedirects(create_response, self.profile_identity_variant_list_url)
        # lets check if it exist in db now, latest added variant should be same as just created valius
        variant = ProfileIdentityVariant.objects.filter(user__username=self.valid_username).latest('id')
        self.assertEqual(variant.label, self.valid_identity_variant_data['label'])
        self.assertEqual(variant.context, self.valid_identity_variant_data['context'])
        self.assertEqual(variant.variant, self.valid_identity_variant_data['variant'])

    # stranger cannot create users profile identity variants
    def test_stranger_cannot_create_users_identity_variants(self):
        # post create profile identity variant without logging in
        response = self.client.post(self.profile_identity_variant_create_url, self.valid_identity_variant_data)
        # response should be 302 redirect to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/profile/identity-variant/add/')

#     # user can see their identity varians 
    def test_user_can_see_their_identity_variants(self):
        # post login
        self.client.login(username=self.valid_username, password=self.valid_password)
        # create variant, and get list 
        self.client.post(self.profile_identity_variant_create_url, self.valid_identity_variant_data)
        response = self.client.get(self.profile_identity_variant_list_url)
        # response should be 200 OK
        self.assertEqual(response.status_code, 200)
        # response data should contain new variant 
        self.assertContains(response, self.valid_identity_variant_data['label'])
        self.assertContains(response, self.valid_identity_variant_data['context'])
        self.assertContains(response, self.valid_identity_variant_data['variant'])


#     # stranger cannot see users profile identity variants 
    def test_stranger_cannot_see_users_identity_variants(self):
        # get profile identity variants without logging in
        response = self.client.get(self.profile_identity_variant_list_url)
        # response should be 302 redirect to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/profile/identity-variant/')

#     # user can update their profile identity variants 
    def test_user_can_update_their_identity_variants(self):
        # post login
        self.client.login(username=self.valid_username, password=self.valid_password)
        # create a profile identity variant
        self.client.post(self.profile_identity_variant_create_url, self.valid_identity_variant_data)
        update_response = self.client.post(self.profile_identity_variant_update_url(1), self.valid_updated_identity_variant_data, follow=True)
        # after edit and follow redirect to list of variants now list should have variant with updated value 
        # response data should contain new variant 
        self.assertContains(update_response, self.valid_updated_identity_variant_data['label'])
        self.assertContains(update_response, self.valid_updated_identity_variant_data['context'])
        self.assertContains(update_response, self.valid_updated_identity_variant_data['variant'])

#     # stranger cannot update users profile identity variants
    def test_stranger_cannot_update_users_identity_variants(self):
        # log in, create variant, log out and try to access it as stranger to update 
        self.client.login(username=self.valid_username, password=self.valid_password)
        self.client.post(self.profile_identity_variant_create_url, self.valid_identity_variant_data)
        self.client.logout()    
        # now try to update as stranger
        response = self.client.put(self.profile_identity_variant_detail_url(1), self.valid_updated_identity_variant_data)
        # response should be 302 redirect to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/profile/identity-variant/1/')

#     # user can delete their profile identity variants
    def test_user_can_delete_their_identity_variants(self):
        # login, create 
        self.client.login(username=self.valid_username, password=self.valid_password)
        self.client.post(self.profile_identity_variant_create_url, self.valid_identity_variant_data)
        # post delete profile identity variant
        response = self.client.post(self.profile_identity_variant_delete_url(1), follow=True)
        # now redirect should be list that no longer contain the variant 
        self.assertNotContains(response, self.valid_identity_variant_data['label'])
        self.assertNotContains(response, self.valid_identity_variant_data['context'])
        self.assertNotContains(response, self.valid_identity_variant_data['variant'])

#     # stranger cannot delete users profile identity variants
#     def test_stranger_cannot_delete_users_identity_variants(self):
        # log in, create variant, log out and try to access it as stranger to update 
        self.client.login(username=self.valid_username, password=self.valid_password)
        self.client.post(self.profile_identity_variant_create_url, self.valid_identity_variant_data)
        self.client.logout()   
        # now try to delete as stranger
        response = self.client.post(self.profile_identity_variant_delete_url(1))
        # response should be 302 redirect to login 
        self.assertRedirects(response, '/accounts/login/?next=/profile/identity-variant/1/delete/')

    


# ## REQUESTS ## 
# # Send 
class RequestsSendTests(TestCase):
    def setUp(self):
        # I need at least two users to test requests between them
        # Create valid user credentials
        self.valid_username1 = 'Johny'
        self.valid_password1 = 'test123123'
        self.valid_email1 = 'johny@example.com'
        # Create a user with valid credentials
        self.user = User.objects.create_user(
            username=self.valid_username1,
            email=self.valid_email1,
            password=self.valid_password1,
        )  
        self.valid_user1_login_data = {
            'username': 'Johny',
            'password': 'test123123',
        }

        self.valid_username2 = 'Michael'
        self.valid_password2 = 'test123123'
        self.valid_email2 = 'michael@example.com'
        # Create a user with valid credentials
        self.user2 = User.objects.create_user(
            username=self.valid_username2,
            email=self.valid_email2,
            password=self.valid_password2,
        )
        self.valid_user2_login_data = {
            'username': 'Michael',
            'password': 'test123123',
        }

        # user that will try to do malicuous actions
        self.valid_username3 = 'Ezma'
        self.valid_password3 = 'test123123'
        self.valid_email3 = 'ezma@example.cam'
        # Create a user with valid credentials
        self.user3 = User.objects.create_user(
            username=self.valid_username3,
            email=self.valid_email3,
            password=self.valid_password3,
        )
        self.valid_user3_login_data = {
            'username': 'Ezma',
            'password': 'test123123',
        }

        self.valid_request_identity_variant_data = {
            'label': 'First Name in Polish',
            'context': 'First name in Polish language.',
        }   

        self.valid_updated_request_identity_variant_data = {
            'label': 'Super First Name in Polish',
            'context': 'Super first name in Polish language.',
        }

        self.valid_request_reasoning = 'Dental office requesting information'
        self.valid_updated_reasoning = 'Super Dental office requesting information'

        # Define URLs for requests
        self.request_send_list_url = reverse('request-send-list')
        self.request_send_create_url = reverse('request-send-create')
        self.request_send_detail_url = lambda pk: reverse('request-send-detail', args=[pk])
        self.request_send_update_url = lambda pk: reverse('request-send-update', args=[pk])
        self.request_send_delete_url = lambda pk: reverse('request-send-delete', args=[pk])
        
        # RequestSendRequestIdentityVariant URLs
        self.request_send_request_identity_variant_create_url = lambda pk: reverse('request-send-request-identity-variant-create', args=[pk])
        self.request_send_request_identity_variant_detail_url = lambda pk, riv_pk: reverse('request-send-request-identity-variant-detail', args=[pk, riv_pk])
        self.request_send_request_identity_variant_update_url = lambda pk, riv_pk: reverse('request-send-request-identity-variant-update', args=[pk, riv_pk])
        self.request_send_request_identity_variant_delete_url = lambda pk, riv_pk: reverse('request-send-request-identity-variant-delete', args=[pk, riv_pk])

        
#     # user can create new sent requests
    def test_user_can_create_new_sent_requests(self):
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        response = self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning}, follow=True)
        # response should be 200 after redirect 
        self.assertEqual(response.status_code, 200)
        # now the page should have request details with all the new request information present in html
        self.assertContains(response, self.valid_username2)
        self.assertContains(response, self.valid_request_reasoning)



#     # user can not create sent requests for other users, checking post injections 
    def test_user_cannot_create_sent_requests_for_other_users(self):
        # user 3 Ezma, tryes to create request for other users 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_send_create_url, {
            'sender': self.valid_username1,  # injection attempt to change sender, should be ignored by server 
            'receiver': self.valid_username2,
            'request_reasoning': 'Createing a request from user1 to user2, but I am malicious Emza - user3.'
        }, follow=True)
        # it should be sucsesfull, but not the way malicious user planned, because sender is server side written 
        self.assertEqual(response.status_code, 200)
        #  check that sender should be logged in user, not attempted valid_username1, by getting just created request from db 
        latest_request = Request.objects.latest('id')
        self.assertNotEqual(latest_request.sender.username, self.valid_username1) # server should not set sender from injoection 
        self.assertEqual(latest_request.sender.username, self.valid_username3)

#     # stranger cannot create sent requests for users
    def test_stranger_cannot_create_sent_requests_for_users(self):
        # post create request without logging in
        response = self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        # response should be 302 redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/create/')

    # user can see their sent requests
    def test_user_can_see_their_sent_requests(self):
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        # now list should have that created request 
        response = self.client.get(self.request_send_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.valid_username2)
        self.assertContains(response, self.valid_request_reasoning)


    # user can not see other users sent requests, as they are not sender
    def test_user_cannot_see_other_users_sent_requests(self):
        # user3 can not see user1 sent requests, as Ezma is not a sender    
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # now log in user3, and get list 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.get(self.request_send_list_url)
        # response should be 200 OK, but list should not have user1 request
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.valid_username2)
        self.assertNotContains(response, self.valid_request_reasoning)

    # stranger cannot see users sent requests
    def test_stranger_cannot_see_users_sent_requests(self):
        # post get sent requests without logging in
        response = self.client.get(self.request_send_list_url)
        # stranger should be redirected to try to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/')

    # user can see details of their sent requests
    def test_user_can_see_details_of_their_sent_requests(self):
        # post login and create request 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        # get detail for that request
        response = self.client.get(self.request_send_detail_url(1))
        # should be 200 and include the request information
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.valid_username2)
        self.assertContains(response, self.valid_request_reasoning)

    # user cannot see details of other users sent requests, as they are not sender
    def test_user_cannot_see_details_of_other_users_sent_requests(self):
        # malicious Ezma (user3) can not see user1 detail sent request, as user3 is not a sender 
        # login and create request as user 1, logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # now Ezma will try to access it
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.get(self.request_send_detail_url(1))
        # respond should be 404, since ezma cant even see request id 1 
        self.assertEqual(response.status_code, 404)

#     # stranger cannot see users sent requests details
    def test_stranger_cannot_see_users_sent_requests_details(self):
        # strangel will try to see without loging in 
        # login and create request as user 1, logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # stranger tries to get details 
        response = self.client.get(self.request_send_detail_url(1))
        # stranger should be redirected to try to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/')

#     # user can update their sent requests
    def test_user_can_update_their_sent_requests(self):
        # login and create one 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        # now update 
        response = self.client.post(self.request_send_update_url(1), {'request_reasoning':self.valid_updated_reasoning}, follow=True)
        # now updated after follow detail view should contain new udpated data 
        self.assertContains(response, self.valid_updated_reasoning)
       

#     # user cannot update other users sent requests, as they are not sender
    def test_user_cannot_update_other_users_sent_requests(self):
        # user 3 tries to update users1 request 
        # login user 1, create request logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # login user3 try to post update 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_send_update_url(1), {'request_reasoning':self.valid_updated_reasoning}, follow=True)
        # since user3 doesnt even see requenst id 1 it should be 404 not found 
        self.assertEqual(response.status_code, 404)

#     # stranger cannot update users sent requests
    def test_stranger_cannot_update_users_sent_requests(self):
        # stranger tries to updates users request by using the request id 
        # login user 1, create request logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # now stranger tries to update that request 
        response = self.client.post(self.request_send_update_url(1), {'request_reasoning':self.valid_updated_reasoning})
        # response shold be redirect to login page 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/edit/')

#     # user can delete their sent requests
    def test_user_can_delete_their_sent_requests(self):
        # login and create request 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        # now delete the request
        response = self.client.post(self.request_send_delete_url(1), follow=True)
        # after delete redirected result should be list of request and since deleted it shouldnt be there 
        self.assertNotContains(response, self.valid_username2)
        self.assertNotContains(response, self.valid_request_reasoning)


#     # other user cannot delete users sent requests, as they are not sender
    def test_user_cannot_delete_other_users_sent_requests(self):
        # user 3 tries to delete users1 request 
        # login user 1, create request logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # login user3 try to delete users 1 request 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_send_delete_url(1))
        # response should be 404 not found, since user 3 does not even see such a resource from db 
        self.assertEqual(response.status_code, 404)


#     # stranger cannot delete users sent requests
    def test_stranger_cannot_delete_users_sent_requests(self):
        # stranger will try to delete users 1 request id1 
        # login user 1, create request logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # now try to delete as stranger 
        response = self.client.post(self.request_send_delete_url(1))
        # response shold be redirect to login page 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/delete/')

    # user can create request identity variants for their sent requests
    def test_user_can_create_request_identity_variants_for_sent_requests(self): 
        # post login, and create request 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        # now create request identity variant
        response = self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        # followed page should now have variant data
        self.assertContains(response, self.valid_request_identity_variant_data['label'])
        self.assertContains(response, self.valid_request_identity_variant_data['context'])


#     # user cannot create request identity variants for other users sent requests, as they are not sender
    def test_user_cannot_create_request_identity_variants_for_other_users_sent_requests(self):  
        # Emza cant create request identity variant for user 1 request 
        # login in as user1, create request, logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()
        # now log in as user3 and try to add RequestIdentityVariant to users1 request 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        # response should be 404 not found since user3 cant even see request id 1
        self.assertEqual(response.status_code, 404)

#     # stranger cannot create request identity variants for users sent requests
    def test_stranger_cannot_create_request_identity_variants_for_users_sent_requests(self):
        # stranger will try to add RequestIdentityVariant to users1 request 
        # login in as user1, create request, logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.logout()      
        # now stranger tries to add variant 
        response = self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data)
        # response should be redirect to login page for not authenticated user 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/request-identity-variant/create/')

    
# # user can see their request identity variants for sent requests
    def test_user_can_see_their_request_identity_variants_for_sent_requests(self):  
        # post login, and create request, create variant for request 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        # now get detail view to view it 
        response = self.client.get(self.request_send_request_identity_variant_detail_url(1, 1))
        # response should be 200, and the html should have label and variant data 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.valid_request_identity_variant_data['label'])
        self.assertContains(response, self.valid_request_identity_variant_data['context'])

#     # user cannot see other users request identity variants for sent requests, as they are not sender
    def test_user_cannot_see_other_users_request_identity_variants_for_sent_requests(self):
        # Ezma user can not see users one request identity variant 
        # login in as user 1, create request and variant, logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        self.client.logout()
        # now login as Ezma, and try to view that variant
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.get(self.request_send_request_identity_variant_detail_url(1, 1))
        # response should be 404, as Ezma is not the sender
        self.assertEqual(response.status_code, 404)     

#     # stranger can not see users request identity variants detail
    def test_stranger_cannot_see_users_request_identity_variants_detail(self):
        # stranger should not be able to see details for user1 requst identity variant 
        # login in as user 1, create request and variant, logout 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        self.client.logout()
        # get details without being authenticated 
        response = self.client.get(self.request_send_request_identity_variant_detail_url(1, 1))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/request-identity-variant/1/')

#     # user can update request identity variant
    def test_user_can_update_request_identity_variant(self):
        # login user1, create request and variant 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        # now update variant 
        response = self.client.post(self.request_send_request_identity_variant_update_url(1, 1), self.valid_updated_request_identity_variant_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.valid_updated_request_identity_variant_data['label'])
        self.assertContains(response, self.valid_updated_request_identity_variant_data['context'])

#     # user can not update other users request identity variant
    def test_user_cannot_update_other_users_request_identity_variant(self):
        # Ezma tries updates users1 requst identity variant 
        # login user1, create request and variant, logout
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        self.client.logout()
        # now login as Ezma and try to update users1 variant 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_send_request_identity_variant_update_url(1, 1), self.valid_updated_request_identity_variant_data, follow=True)
        # response should be 404, as Ezma is not the sender
        self.assertEqual(response.status_code, 404)     

#     # stranger can not update users request identity variant
    def test_stranger_cannot_update_users_request_identity_variant(self):
        # stranger can not update users1 request identity variant 
        # login user1, create request and variant, logout
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        self.client.logout()
        # try updating as stranger 
        response = self.client.post(self.request_send_request_identity_variant_update_url(1, 1), self.valid_updated_request_identity_variant_data)
        # response should be 302 , redirect for stranger to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/request-identity-variant/1/edit/')

#     # user sender can not update link field that is meant for receiver to manage 
    def test_user_sender_can_not_update_link_field_for_receiver(self):
        # Ezma tries to steal users profile identity variants, by changing send request - request identity variant receivers link field 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        # set the data with fishing 
        updated_data = {    
            'label': 'Super First Name in Polish',
            'context': 'Superupdated first name in Polish language.',
            'user_provided_variant': '1',  # maliciuos attempt 'user_provided_variant' is read only sender should not be able to update it and fish the request user data 
        }
        response = self.client.post(self.request_send_request_identity_variant_update_url(1, 1), updated_data, follow=True)
        # label and context should be changed, but user_provided_variant should still stay none 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, updated_data['label'])
        self.assertContains(response, updated_data['context'])
        self.assertContains(response, '---') # its '---' for none in hmtl, or receiver variant if not none 

#     # stranger can not update users request identity variant link field
    def test_stranger_cannot_update_users_request_identity_variant_link_field(self):
        # stranger should not be able to update variant 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        self.client.logout()
        # set the data with fishing 
        updated_data = {    
            'label': 'Super First Name in Polish',
            'context': 'Superupdated first name in Polish language.',
            'user_provided_variant': '1',  # maliciuos attempt 'user_provided_variant' is read only sender should not be able to update it and fish the request user data 
        }
        response = self.client.post(self.request_send_request_identity_variant_update_url(1, 1), updated_data)
        # response should be 302 , redirect for stranger to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/request-identity-variant/1/edit/')
        

#     # user can delete request identity variant
    def test_user_can_delete_request_identity_variant(self):
        # login, create request and request variant 
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        # now delete variant
        response = self.client.post(self.request_send_request_identity_variant_delete_url(1, 1), follow=True)
        # it should go back to request detail, and variant data should not be there since it got deleted 
        self.assertNotContains(response, self.valid_request_identity_variant_data['label'])
        self.assertNotContains(response, self.valid_request_identity_variant_data['context'])

#     # user can not delete other users request identity variant
    def test_user_cannot_delete_other_users_request_identity_variant(self):
        # Ezma tries to delete users 1 request identity variant 
        # Login as user1, create request, create variant, logout
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        self.client.logout()
        # now login as Ezma and try to delete it 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # attempt to delete users1 variant 
        response = self.client.post(self.request_send_request_identity_variant_delete_url(1, 1))
        # response should be 404, as Ezma is not the sender, so does not Even see such a resource
        self.assertEqual(response.status_code, 404)

#     # stranger can not delete users request identity variant    
    def test_stranger_cannot_delete_users_request_identity_variant(self):
        # Stranger tries to delete request identity variant for user 1 
        # Login as user1, create request, create variant, logout
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        self.client.post(self.request_send_create_url, {'receiver': self.valid_username2, 'request_reasoning':self.valid_request_reasoning})
        self.client.post(self.request_send_request_identity_variant_create_url(1), self.valid_request_identity_variant_data, follow=True)
        self.client.logout()
        # now strenger tries to delete it 
        response = self.client.post(self.request_send_request_identity_variant_delete_url(1, 1))
        # response should be 302 , redirect for stranger to login 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/send/1/request-identity-variant/1/delete/')
        



# # Received 

class RequestsReceiveTests(TestCase):
    def setUp(self):
        # I need at least two users to test requests between them
        # Create valid user credentials
        self.valid_username1 = 'Johny'
        self.valid_password1 = 'test123123'
        self.valid_email1 = 'johny@example.com'
        # Create a user with valid credentials
        self.user1 = User.objects.create_user(
            username=self.valid_username1,
            email=self.valid_email1,
            password=self.valid_password1,
        )  
        self.valid_user1_login_data = {
            'username': 'Johny',
            'password': 'test123123',
        }

        self.valid_username2 = 'Michael'
        self.valid_password2 = 'test123123'
        self.valid_email2 = 'michael@example.com'
        # Create a user with valid credentials
        self.user2 = User.objects.create_user(
            username=self.valid_username2,
            email=self.valid_email2,
            password=self.valid_password2,
        )
        self.valid_user2_login_data = {
            'username': 'Michael',
            'password': 'test123123',
        }

        # user that will try to do malicuous actions
        self.valid_username3 = 'Ezma'
        self.valid_password3 = 'test123123'
        self.valid_email3 = 'ezma@example.cam'
        # Create a user with valid credentials
        self.user3 = User.objects.create_user(
            username=self.valid_username3,
            email=self.valid_email3,
            password=self.valid_password3,
        )
        self.valid_user3_login_data = {
            'username': 'Ezma',
            'password': 'test123123',
        }

        self.valid_request_identity_variant_data = {
            'label': 'First Name in Polish',
            'context': 'First name in Polish language.',
        }   
        
        # create requests, since i already tested that user can create sent request, i will set them in setup 
        # create a request from user1 to user2
        self.valid_request_reasoning = 'Dental office information'
        self.request1 = Request.objects.create(
            sender=self.user1,
            receiver=self.user2,
            request_reasoning=self.valid_request_reasoning,
        )

        # create request identity variant for request1
        self.request_identity_variant1 = RequestIdentityVariant.objects.create(
            request=self.request1,
            label='First Name in Polish',
            context='First name in Polish language.',
        )

        # create profile identity variant for user2
        self.profile_identity_variant1 = ProfileIdentityVariant.objects.create(
            user=self.user2,
            label='First Name in Polish',
            context='First name in Polish language.',
            variant='Michal'
        )

        self.profile_identity_variant2 = ProfileIdentityVariant.objects.create(
            user=self.user2,
            label='First Name in Polish, Polish alphabet',
            context='My first name in Polish language, but also with Polish alphabet.',
            variant='Michał'
        )

        
        # Define URLs for requests
        self.request_receive_list_url = reverse('request-receive-list')
        self.request_receive_detail_url = lambda pk: reverse('request-receive-detail', args=[pk])
        self.request_receive_accept_url = lambda pk: reverse('request-receive-accept', args=[pk])
        self.request_receive_deny_url = lambda pk: reverse('request-receive-deny', args=[pk])
        
        # RequestReceiveRequestIdentityVariant URLs
        self.request_receive_request_identity_variant_detail_url = lambda pk, riv_pk: reverse('request-receive-request-identity-variant-detail', args=[pk, riv_pk])
        self.request_receive_request_identity_variant_update_url = lambda pk, riv_pk: reverse('request-receive-request-identity-variant-update', args=[pk, riv_pk])
        
       
#     # user can see list of received requests
    def test_user_can_see_list_of_received_requests(self):
        # login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # get received requests
        response = self.client.get(self.request_receive_list_url)
        # now page should have requests details with all the requests information present, like sender and reasoning
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.valid_username1) 
        self.assertContains(response, self.valid_request_reasoning)

 
#     # user can not see other  users list of received requests 
    def test_user_cannot_see_other_users_list_of_received_requests(self):
        # user3 should not be able to see users2 received requests
        # login 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # get list 
        response = self.client.get(self.request_receive_list_url)
        # it should have users3 requests so. 200, but not users2 requst present 
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.valid_username1) 
        self.assertNotContains(response, self.valid_request_reasoning)


#     # stranger cannot see users received requests
    def test_stranger_cannot_see_users_received_requests(self):
        # without login in get list of received request 
        response = self.client.get(self.request_receive_list_url)
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/')

#     # user can see details of their received requests
    def test_user_can_see_details_of_their_received_requests(self):
        # login, and get detail for the request
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.get(self.request_receive_detail_url(1))
        # response should be 200 OK, and contain request info
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.valid_username1)
        self.assertContains(response, self.valid_request_reasoning)

#     # user cannot see details of other users received requests, as they are not receiver
    def test_user_cannot_see_details_of_other_users_received_requests(self):    
        # Ezma tries to see user2 received request details
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.get(self.request_receive_detail_url(1))
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger cannot see users received requests details
    def test_stranger_cannot_see_users_received_requests_details(self):
        # without login in get details of received request
        response = self.client.get(self.request_receive_detail_url(1))
        # response shold be redirect to login page 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/')


#     # user can accept their received request
    def test_user_can_accept_their_received_request(self):
        # login as user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # accept the received request
        response = self.client.post(self.request_receive_accept_url(1), follow=True)  # request id is 1
        # response should be 200 OK, and now it should include accepted 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'accepted')

#     # user can not accept others users requests 
    def test_user_cannot_accept_other_users_received_request(self):
        # Ezma can't accept users2 request
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_receive_accept_url(1), follow=True)  # request id is 1
        # response should be 404 Not Found, since user 3 does not even see that request
        self.assertEqual(response.status_code, 404)

#     # stranger cannot accept users received requests
    def test_stranger_cannot_accept_users_received_requests(self):
        # stranger tries to accept user2 received request 
        response = self.client.post(self.request_receive_accept_url(1))  # request id is 1
        # response should be 302, to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/accept/')

#   

#     # user can deny their received request 
    def test_user_can_deny_their_received_request(self):
        # user2 can deny request
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.post(self.request_receive_deny_url(1), follow=True)  # request id is 1
        # response should be 200 OK, and now it should include denied
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'denied')

#     # user can not deny other users requests
    def test_user_cannot_deny_other_users_received_request(self):
        # user3 Ezma tries to deny user2's request
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_receive_deny_url(1), follow=True)  # request id is 1
        # response should be 404 Not Found, since user 3 does not even see that request
        self.assertEqual(response.status_code, 404)

#     # stranger cannot deny users received requests
    def test_stranger_cannot_deny_users_received_requests(self):
        # stranger tries to deny user2  request
        response = self.client.post(self.request_receive_deny_url(1))  # request id is 1
        # response should be 302, to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/deny/')

#     # user can see requequest identity variants list, for request 
    def test_user_can_see_request_identity_variants_for_their_received_requests(self):
        # user can see identity variants in the received request
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.get(self.request_receive_detail_url(1))
        # response should be 200, and request detail view should have list of variants
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.request_identity_variant1.label)
        self.assertContains(response, self.request_identity_variant1.context)

#     # user cannot see request identity variants for other users  
    def test_user_cannot_see_request_identity_variants_for_other_users_received_requests(self):
        # user3 tries to see user2 request identity variants
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.get(self.request_receive_detail_url(1))
        # response should be 404 Not Found, since user 3 does not even see that request
        self.assertEqual(response.status_code, 404)

#     # stranger cannot see users request identity variants for received requests
    def test_stranger_cannot_see_users_request_identity_variants_for_received_requests(self):
        # stranger tries to see user2 request identity variants
        response = self.client.get(self.request_receive_detail_url(1))
        # response should be 302, to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/')

#     # user receiver can not see request identity variant detail for their received request that is pending 
    def test_user_receiver_can_not_see_request_identity_variant_detail_for_their_received_requests_that_are_pending(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # get request identity variant detail for received requests
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 403 forbidden 
        self.assertEqual(response.status_code, 403)

#     # user can not see other users request identity variant detail ( using receiver end point ) that is pending 
    def test_user_cannot_see_other_users_request_identity_variant_detail_pending(self):
        # Ezma tries to see user2 request identity variant detail
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # try to get request identity variant detail
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not see users request identity variant detail  that is pending 
    def test_stranger_cannot_see_users_request_identity_variant_detail_pending(self):
        # stranger, not authenticated tries to see users2 requst identity variant detail 
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 302, to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/')

#     # user can not see request identity variant detail, that is declined 
    def test_user_receiver_can_not_see_request_identity_variant_detail_for_their_received_requests_that_are_denied(self):
        # login as user2, deny request, and try to see requent identity variant detail 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.post(self.request_receive_deny_url(1))
        # now try to get request identity variant detail for denied request
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 403 forbidden 
        self.assertEqual(response.status_code, 403)

#     # user can not see other users request identity variant detail ( using receiver end point ) that is denied
    def test_user_cannot_see_other_users_request_identity_variant_detail_denied(self):
        # Ezma tries to see request identity variant detail for request that is denied of other user 
        # first login user2 and deny request logout 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.post(self.request_receive_deny_url(1))
        self.client.logout()
        # login as user3 and try to see request identity variant detail
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not see users request identity variant detail  that is denied   
    def test_stranger_cannot_see_users_request_identity_variant_detail_denied(self):
        # first login user2 and deny the request
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.post(self.request_receive_deny_url(1))
        self.client.logout()
        # now try to get request identity variant detail as stranger
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 302 redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/')

#     # user can accept request that is pending 
    def test_user_can_accept_request_that_is_pending(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # accept the received request
        response = self.client.post(self.request_receive_accept_url(1), follow=True)
        # response should be 200 OK, and html should contain the updated status
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'accepted')

#     # user can not accept request for other user that is pending 
    def test_user_cannot_accept_other_users_request_that_is_pending(self):
#         # Ezma (user3) can not accept user2 request  
#         # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # try to accept the received request
        response = self.client.post(self.request_receive_accept_url(1))
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not accept users request that is pending
    def test_stranger_cannot_accept_users_request_that_is_pending(self):
        # user2 request is trying to be accepted by stranger
        response = self.client.post(self.request_receive_accept_url(1))
        # response should be 302 redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/accept/')

#     # user can change their mind and accept request that is denied
    def test_user_can_accept_request_that_is_denied(self):
        # user2 can deny request
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_deny_url(1), follow=True) 
        # now accept the denied request
        response = self.client.post(self.request_receive_accept_url(1), follow=True)
        # response should be 200 OK, and now it should include accepted
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'accepted')

#     # user can not accept other users request that is denied
    def test_user_cannot_accept_other_users_request_that_is_denied(self):
        # Ezma tries to accept users2 request that has been denied 
        # login user, deny request 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_deny_url(1), follow=True) 
        self.client.logout()  
        # Login as Ezma and try to malicously change that 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_receive_accept_url(1), follow=True)
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not accept users request that is denied
    def test_stranger_cannot_accept_users_request_that_is_denied(self):
        # stranger will try to accept user2 request that is denied
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_deny_url(1), follow=True) 
        self.client.logout()  
        # now try to accept that as stranger 
        response = self.client.post(self.request_receive_accept_url(1))
        # response should be 302, redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/accept/')

#     # user can deny request that is pending
    def test_user_can_deny_request_that_is_pending(self):
        # user2 can deny request
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.post(self.request_receive_deny_url(1), follow=True)
        # response should be 200 OK, and have status denied 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'denied')


#     # user can not deny other users request that is pending
    def test_user_cannot_deny_other_users_request_that_is_pending(self):
        # Ezma (user3) can not deny user2 request
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_receive_deny_url(1), follow=True)
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not deny users request that is pending
    def test_stranger_cannot_deny_users_request_that_is_pending(self):
        # now try to deny that as stranger
        response = self.client.post(self.request_receive_deny_url(1))
        # response should be 302, redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/deny/')

#     # user can change their minde and deny request that is accepted 
    def test_user_can_deny_request_that_is_accepted(self):
        # user2 login, accept request 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1), follow=True)
        # now try to deny
        response = self.client.post(self.request_receive_deny_url(1), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'denied')

#     # user can not deny other users request that is accepted
    def test_user_cannot_deny_other_users_request_that_is_accepted(self):
        # Ezma will try to accept request has has been denied, of other user 
        # user2 login, accept request, logout 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.logout()
        # login as Ezma and attempt to deny it
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_receive_deny_url(1), follow=True)
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not deny users request that is accepted
    def test_stranger_cannot_deny_users_request_that_is_accepted(self):
        # stranger will try to deny the request, that has been accepted 
        # user2 login, accept request, logout 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.logout()
        # now stranger tries to deny it
        response = self.client.post(self.request_receive_deny_url(1))
        # response should be 302 redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/deny/')

#     # user can see request identity variant detail for accepted request
    def test_user_can_see_request_identity_variant_detail_for_accepted_request(self):
        # with accepted request, request identity variant details should be avaible
        # login, accept request, and get variant detail
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 200 OK, and contain variant details 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.request_identity_variant1.label)
        self.assertContains(response, self.request_identity_variant1.context)

#     # user can not see other users request identity variant detail ( using receiver end point ) for accepted request
    def test_user_cannot_see_other_users_request_identity_variant_detail_for_accepted_request(self):
        # Ezma will try to see users2 request identity variants, for accepted request 
        # login as user2, accept request, logout
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.logout()
        # login ezma, and try to get users2 request identity variant detail
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 404 Not Found, since resource should not be visible
        self.assertEqual(response.status_code, 404)

        # stranger can not see other users request identity variant detail, for accepted request
    def test_stranger_cannot_see_other_users_request_identity_variant_detail_for_accepted_request(self):
        # stranger will try to access other users request identity variant
        # login user2, accept request logout
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.logout()
        # try to access as stranger
        response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
        # response should be 302 redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/')

#     # user can link request identity variant with profile identity variant for accepted request
    def test_user_can_link_request_identity_variant_with_profile_identity_variant_for_accepted_request(self):
        # login as user, and accept request
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        # now link request identity variant with profile identity variant
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1}, follow=True)
        # response should be 200, and the link should be created, and page now should contain the linked profile identity variant
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile_identity_variant1.variant)

#     # user can not link other users request identity variant with profile identity variant for accepted request
    def test_user_cannot_link_other_users_request_identity_variant_with_profile_identity_variant_for_accepted_request(self):
        # Ezma will try to maliciusly link users2 request identity variant for request that is accepted
        # login user2, accept request, logout
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.logout()
        # now Ezma tries to link user2 request identity variant with profile identity variant
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1}, follow=True)
        # response should be 404, no resource found
        self.assertEqual(response.status_code, 404)

#     # stranger can not link users request identity variant with profile identity variant for accepted request
    def test_stranger_cannot_link_users_request_identity_variant_with_profile_identity_variant_for_accepted_request(self):
        # stranger will try to add link for user 2 
        # login user2, accept request, logout
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.logout()
        # try to update as stranger
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # response should be 302 redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/edit/')


#     # user can not link request identity variant with profile identity variant for pending request
    def test_user_cannot_link_request_identity_variant_with_profile_identity_variant_for_pending_request(self):
        # login and try to link request request identity variant with profile identity variant
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # response should be 403 Forbidden, as the request is pending
        self.assertEqual(response.status_code, 403)

#     # user can not link other users request identity variant with profile identity variant for pending request
    def test_user_cannot_link_other_users_request_identity_variant_with_profile_identity_variant_for_pending_request(self): 
        # Ezma (user3) can not link user2 request identity variant with profile identity variant, as user3  is not receiver    
        # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # try to link request identity variant with profile identity variant
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not link users request identity variant with profile identity variant for pending request
    def test_stranger_cannot_link_users_request_identity_variant_with_profile_identity_variant_for_pending_request(self):
        # try to link request identity variant with profile identity variant without logging in
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # response should be 302 redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/edit/')

#     # user can not link request identity variant with profile identity variant for denied request
    def test_user_cannot_link_request_identity_variant_with_profile_identity_variant_for_denied_request(self):
        # post login user2 and deny request 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_deny_url(1))
        # now try to link request identity variant with profile identity variant
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # response should be 403 Forbidden, as the request is denied
        self.assertEqual(response.status_code, 403)   

#     # user can not link other users request identity variant with profile identity variant for denied request
    def test_user_cannot_link_other_users_request_identity_variant_with_profile_identity_variant_for_denied_request(self):
        # login as user 2 and deny the request first
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_deny_url(1))
        self.client.logout()  # log out user2
        # now Ezma tries to link user2 request identity variant with profile identity variant
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # now try to link other users request identity variant with profile identity variant
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # response sholuld be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)
        
#     # stranger can not link users request identity variant with profile identity variant for denied request
    def test_stranger_cannot_link_users_request_identity_variant_with_profile_identity_variant_for_denied_request(self):
        # login user 2, deny request, logout  
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_deny_url(1))
        self.client.logout()  # log out user2
        # try to link without logging in 
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # response should be 302 redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/edit/')


#     # user can update link field of request identity variant to link it with different profile identity variant
    def test_user_can_update_link_field_of_request_identity_variant_to_link_it_with_different_profile_identity_variant(self):
        # post login user2 and accept request 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.post(self.request_receive_accept_url(1))
        # now link request identity variant with profile identity variant
        self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # now update link field to link it with different profile identity variant
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 2}, follow=True)
        # response should be 200, and included updated variant 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profile_identity_variant2.variant)


#     # other user can not update link field of request identity variant to link it with profile identity variant
    def test_other_user_cannot_update_link_field_of_request_identity_variant_to_link_it_with_profile_identity_variant(self):
        # Ezma tries to change links 
        # login user2, accept request, link , logout
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        self.client.logout()
        # login as Ezma and try to change users2 link 
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 2}, follow=True)
        # response should be 404 becasue Ezma does not have such a resaurce to be found
        self.assertEqual(response.status_code, 404)

#     # stranger can not update link field of request identity variant to link it with profile identity variant      
    def test_stranger_cannot_update_link_field_of_request_identity_variant_to_link_it_with_profile_identity_variant(self):
        # stranger tries to change link 
        # login user2, accept request, link , logout
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        self.client.logout()
        # without login in try to change link
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 2})
        # 302 redirect, to login page 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/edit/')
        

#     # user receiver can not update request identity variant detail other thenk link field 
    def test_user_receiver_can_not_update_request_identity_variant_detail_other_than_link_field(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # try to update request identity variant detail
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'label': 'new label'})
        # response should be 403 Forbidden, as the request is pending
        self.assertEqual(response.status_code, 403)

#     # user (that is not a sender ) can not update other users request identity variant detail ( using receiver end point )
    def test_user_cannot_update_other_users_request_identity_variant_detail(self):
        # Ezma (user3) can not update user2 request identity variant detail, as user3 is not receiver    
        # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # try to update request identity variant detail
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'label': 'new label'})
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, 404)

#     # stranger can not update users request identity variant detail 
    def test_stranger_cannot_update_users_request_identity_variant_detail(self):
        # try to update request identity variant detail without logging in
        response = self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'label': 'new label'})
        # response should be 302 redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/request/receive/1/request-identity-variant/1/edit/')

#     # test if links get cleaned, when user is changing from accepted to denied
    def test_links_get_disconnected_upon_denying_the_request(self):
        # post login user2 and accept request, and link variant 
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        self.client.post(self.request_receive_accept_url(1))
        self.client.post(self.request_receive_request_identity_variant_update_url(1, 1), {'profile_link': 1})
        # now deny the request, and check if data is wiped out
        response = self.client.post(self.request_receive_deny_url(1), follow=True)
        # response after follow to request detail should be 200, and variant should be no longer there
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.profile_identity_variant1.variant)
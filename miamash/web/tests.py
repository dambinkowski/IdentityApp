from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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


#     # user cannot log in with bad credentials
#     def test_user_cannot_login_with_bad_credentials(self):
#         # post login wrong password
#         response = self.client.post(self.login_url, self.wrong_user_login_password_data)
#         # repsonse should be 400 Bad Request
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # post login wrong username
#         response = self.client.post(self.login_url, self.wrong_user_login_username_data)
#         # response should be 400 Bad Request
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     # user can log out
#     def test_user_can_logout(self):
#         # post login
#         self.client.login(username=self.valid_username, password=self.valid_password)
#         # post logout
#         response = self.client.post(self.logout_url)
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have a 'detail' message
#         self.assertEqual(response.json()['detail'],'Successfully logged out.')

#     # user can register with good credentials
#     def test_user_can_register_with_good_credentials(self):
#         # post register with valid data
#         response = self.client.post(self.register_url, self.valid_user_registration_data)
#         # response should be 201 Created
#         print(response.status_code, response.json())
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # response data should have a 'key' which is a token
#         self.assertIn('key', response.json())  

#     # test if user is unique
#     def test_user_cannot_register_with_existing_username(self):
#         # post register with existing username
#         response = self.client.post(self.register_url, username=self.valid_username, email='john1@example.com', password=self.valid_password)
#         print(response.status_code, response.json())
#         # response should be 400 Bad Request
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # response data should have a 'username' error
#         self.assertIn('username', response.json())
#         self.assertIn('email', response.json())

#     # user cannot register with bad credentials
#     def test_user_cannot_register_with_bad_credentials(self):
#         # post register with invalid data
#         response = self.client.post(self.register_url, self.invalid_user_registration_data)
#         # response should be 400 Bad Request
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # response data should have a 'username', 'email', 'password1', 'password2' errors
#         self.assertIn('username', response.json())
#         self.assertIn('email', response.json())
#         self.assertIn('password1', response.json())
#         self.assertIn('password2', response.json())
        

# ## PROFILE IDENTITY VARIANTS ## 
# class ProfileIdentityVariantsTests(APITestCase):
#     def setUp(self):
#         # Create valid user credentials
#         self.valid_username = 'Johny'
#         self.valid_password = 'test123123'
#         self.valid_email = 'johny@example.com'
#         # Create a user with valid credentials
#         self.user = User.objects.create_user(
#             username=self.valid_username,
#             email=self.valid_email,
#             password=self.valid_password,
#         )  

#         self.valid_user_login_data = {
#             'username': 'Johny',
#             'password': 'test123123',
#         }

#         self.valid_identity_variant_data = {
#             'label': 'First Name',
#             'context': 'Firstname also known as given name.',
#             'variant': 'John',
#         }

#         self.valid_updated_identity_variant_data = {
#             'label': 'Polish firstname',
#             'context': 'This has to be Polish letters first name.',
#             'variant': 'Janusz',
#         }
#         # Define URLs for profile identity variants
#         self.profile_identity_variant_list_create_url = reverse('api-profile-identity-variant-list-create')
#         self.profile_identity_variant_detail_url = lambda pk: reverse('api-profile-identity-variant-detail', args=[pk])

#     # user can create their profile identity variants
#     def test_user_can_create_their_identity_variants(self):
#         # log in the user
#         self.client.login(username=self.valid_username, password=self.valid_password)
#         # post create profile identity variant
#         response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
#         # response should be 201 Created
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # response data should have a fields 'label', 'context', 'variant'
#         self.assertIn('label', response.json())
#         self.assertIn('context', response.json())
#         self.assertIn('variant', response.json())
#         # response data should have the same data as the one sent
#         self.assertEqual(response.json()['label'], self.valid_identity_variant_data['label'])
#         self.assertEqual(response.json()['context'], self.valid_identity_variant_data['context'])
#         self.assertEqual(response.json()['variant'], self.valid_identity_variant_data['variant'])


#     # stranger cannot create users profile identity variants
#     def test_stranger_cannot_create_users_identity_variants(self):
#         # post create profile identity variant without logging in
#         response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


#     # user can see their identity varians 
#     def test_user_can_see_their_identity_variants(self):
#         # post login
#         self.client.login(username=self.valid_username, password=self.valid_password)
#         # get profile identity variants
#         response = self.client.get(self.profile_identity_variant_list_create_url)
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should be a list
#         self.assertIsInstance(response.json(), list)

#     # stranger cannot see users profile identity variants 
#     def test_stranger_cannot_see_users_identity_variants(self):
#         # get profile identity variants without logging in
#         response = self.client.get(self.profile_identity_variant_list_create_url)
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can update their profile identity variants 
#     def test_user_can_update_their_identity_variants(self):
#         # post login
#         self.client.login(username=self.valid_username, password=self.valid_password)
#         # create a profile identity variant
#         create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created profile identity variant id
#         identity_variant_id = create_response.json()['id']
#         # post update profile identity variant
#         response = self.client.put(self.profile_identity_variant_detail_url(identity_variant_id), self.valid_updated_identity_variant_data)
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated data
#         self.assertEqual(response.json()['label'], self.valid_updated_identity_variant_data['label'])
#         self.assertEqual(response.json()['context'], self.valid_updated_identity_variant_data['context'])
#         self.assertEqual(response.json()['variant'], self.valid_updated_identity_variant_data['variant'])

#     # stranger cannot update users profile identity variants
#     def test_stranger_cannot_update_users_identity_variants(self):
#         # log in, create variant, log out and try to access it as stranger to update 
#         self.client.login(username=self.valid_username, password=self.valid_password)
#         create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         identity_variant_id = create_response.json()['id']
#         self.client.logout()    
#         # now try to update as stranger
#         response = self.client.put(self.profile_identity_variant_detail_url(identity_variant_id), self.valid_updated_identity_variant_data)
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can delete their profile identity variants
#     def test_user_can_delete_their_identity_variants(self):
#         # post login
#         self.client.login(username=self.valid_username, password=self.valid_password)
#         # create a profile identity variant
#         create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created profile identity variant id
#         identity_variant_id = create_response.json()['id']
#         # post delete profile identity variant
#         response = self.client.delete(self.profile_identity_variant_detail_url(identity_variant_id))
#         # response should be 204 No Content
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     # stranger cannot delete users profile identity variants
#     def test_stranger_cannot_delete_users_identity_variants(self):
#         # log in, create variant, log out and try to access it as stranger to delete 
#         self.client.login(username=self.valid_username, password=self.valid_password)
#         create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         identity_variant_id = create_response.json()['id']
#         self.client.logout()    
#         # now try to delete as stranger
#         response = self.client.delete(self.profile_identity_variant_detail_url(identity_variant_id))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    


# ## REQUESTS ## 
# # Send 
# class RequestsSendTests(TestCase):
#     def setUp(self):
#         # I need at least two users to test requests between them
#         # Create valid user credentials
#         self.valid_username1 = 'Johny'
#         self.valid_password1 = 'test123123'
#         self.valid_email1 = 'johny@example.com'
#         # Create a user with valid credentials
#         self.user = User.objects.create_user(
#             username=self.valid_username1,
#             email=self.valid_email1,
#             password=self.valid_password1,
#         )  
#         self.valid_user1_login_data = {
#             'username': 'Johny',
#             'password': 'test123123',
#         }

#         self.valid_username2 = 'Michael'
#         self.valid_password2 = 'test123123'
#         self.valid_email2 = 'michael@example.com'
#         # Create a user with valid credentials
#         self.user2 = User.objects.create_user(
#             username=self.valid_username2,
#             email=self.valid_email2,
#             password=self.valid_password2,
#         )
#         self.valid_user2_login_data = {
#             'username': 'Michael',
#             'password': 'test123123',
#         }

#         # user that will try to do malicuous actions
#         self.valid_username3 = 'Ezma'
#         self.valid_password3 = 'test123123'
#         self.valid_email3 = 'ezma@example.cam'
#         # Create a user with valid credentials
#         self.user3 = User.objects.create_user(
#             username=self.valid_username3,
#             email=self.valid_email3,
#             password=self.valid_password3,
#         )
#         self.valid_user3_login_data = {
#             'username': 'Ezma',
#             'password': 'test123123',
#         }

#         self.valid_request_identity_variant_data = {
#             'label': 'First Name in Polish',
#             'context': 'First name in Polish language.',
#         }   

#         # Define URLs for requests
#         self.request_send_list_create_url = reverse('api-request-send-list-create')
#         self.request_send_detail_url = lambda pk: reverse('api-request-send-detail', args=[pk]) 
#         self.request_send_request_identity_variant_list_create_url = lambda pk: reverse('api-request-send-request-identity-variant-list-create', args=[pk])
#         self.request_send_request_identity_variant_detail_url = lambda pk, request_identity_variant_pk: reverse('api-request-send-request-identity-variant-detail', args=[pk, request_identity_variant_pk])

#     # user can create new sent requests
#     def test_user_can_create_new_sent_requests(self):
#         # post login
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'I need your identity information for this test.'})
#         # response should be 201 Created
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # response data should have a 'receiver' field with the username of the receiver
#         self.assertIn('receiver_username', response.json())
#         self.assertEqual(response.json()['receiver_username'], self.valid_username2)
#         self.assertIn('request_reasoning', response.json())
#         self.assertEqual(response.json()['request_reasoning'], 'I need your identity information for this test.')

#     # user can not create sent requests for other users, checking post injections 
#     def test_user_cannot_create_sent_requests_for_other_users(self):
#         # user3 is malicious user trying to create request from user1 to user2, that should not be possible 
#         # server does not take client data for sender, it uses loged in credentials to determine that
#         # so the result should be still suscessful, but the sender will be user3, not user1
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # post create request
#         response = self.client.post(self.request_send_list_create_url, {
#             'sender_username': self.valid_username1,  # injection attempt to change sender, should be ignored by server 
#             'receiver_username': self.valid_username2,
#             'request_reasoning': 'Createing a request from user1 to user2, but I am malicious Emza - user3.'
#         })
#         # response should be 201 Created
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # response data should have a 'receiver' field with the username of the receiver
#         self.assertIn('receiver_username', response.json())
#         self.assertEqual(response.json()['receiver_username'], self.valid_username2)
#         self.assertIn('request_reasoning', response.json())
#         self.assertEqual(response.json()['request_reasoning'], 'Createing a request from user1 to user2, but I am malicious Emza - user3.')
#         data = response.json()
#         # since response does not contain sender_username, i am going to pull request from database to check sender
#         # and it should be user3, not malicious attept to change it to user1
#         req = Request.objects.get(id=data['id'])
#         self.assertEqual(req.sender, self.user3) # should be user3/logged in user, not user1
#         self.assertNotEqual(req.sender, self.user) # should not be user1, as it was injection attempt

#     # stranger cannot create sent requests for users
#     def test_stranger_cannot_create_sent_requests_for_users(self):
#         # post create request without logging in
#         response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'I just want your data'})
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can see their sent requests
#     def test_user_can_see_their_sent_requests(self):
#         # post login
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'This is dental office, we need your identity information.'})
#         # get sent requests
#         response = self.client.get(self.request_send_list_create_url)
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should be a list
#         self.assertIsInstance(response.json(), list)
#         # response data should have the created request
#         self.assertGreater(len(response.json()), 0)  # should have at least one request
#         # check if the created request is in the response data
#         created_request = response.json()[0]
#         self.assertEqual(created_request['receiver_username'], self.valid_username2)
#         self.assertEqual(created_request['request_reasoning'], 'This is dental office, we need your identity information.')


#     # user can not see other users sent requests, as they are not sender
#     def test_user_cannot_see_other_users_sent_requests(self):
#         # user3 can not see user1 sent requests, as Ezma is not a sender    
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'This is dental office, we need your identity information.'})
#         # now log in user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # get sent requests
#         response = self.client.get(self.request_send_list_create_url)
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should be a list
#         self.assertIsInstance(response.json(), list)
#         # response data should be empty, as user3 is not sender of any requests
#         self.assertEqual(len(response.json()), 0)

#     # stranger cannot see users sent requests
#     def test_stranger_cannot_see_users_sent_requests(self):
#         # post get sent requests without logging in
#         response = self.client.get(self.request_send_list_create_url)
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can see details of their sent requests
#     def test_user_can_see_details_of_their_sent_requests(self):
#         # post login
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # get details of the sent request
#         response = self.client.get(self.request_send_detail_url(request_id))
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the created request details
#         self.assertIn('receiver_username', response.json())
#         self.assertEqual(response.json()['receiver_username'], self.valid_username2)
#         self.assertIn('request_reasoning', response.json())
#         self.assertEqual(response.json()['request_reasoning'], 'Dental office data request.')

#     # user cannot see details of other users sent requests, as they are not sender
#     def test_user_cannot_see_details_of_other_users_sent_requests(self):
#         # malicious Ezma (user3) can not see user1 detail sent request, as user3 is not a sender 
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # now log in Ezma
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # get details of the sent request
#         response = self.client.get(self.request_send_detail_url(request_id))
#         # response should be 404 Not Found, as user3 is not sender of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger cannot see users sent requests details
#     def test_stranger_cannot_see_users_sent_requests_details(self):
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         self.client.logout()  # log out user1
#         # now try to get details as stranger
#         response = self.client.get(self.request_send_detail_url(request_id))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can update their sent requests
#     def test_user_can_update_their_sent_requests(self):
#         # post login
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # post update request
#         response = self.client.put(self.request_send_detail_url(request_id), {'receiver_username': self.valid_username2, 'request_reasoning':'Super dental office data request.'})
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated data
#         self.assertIn('receiver_username', response.json())
#         self.assertEqual(response.json()['receiver_username'], self.valid_username2)
#         self.assertIn('request_reasoning', response.json())
#         self.assertEqual(response.json()['request_reasoning'], 'Super dental office data request.')

#     # user cannot update other users sent requests, as they are not sender
#     def test_user_cannot_update_other_users_sent_requests(self):
#         # Ezma  can not update user1 sent requests, as user3 is not sender
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # now log in user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # post update request
#         response = self.client.put(self.request_send_detail_url(request_id), {'receiver_username': self.valid_username2, 'request_reasoning':'Malicious attempt to update request.'})
#         # since this system queries from database only requests where sender is logged in user, so trying to get that id request will just result not found 
#         # response should be 404 Not Found, as user3 is not sender of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger cannot update users sent requests
#     def test_stranger_cannot_update_users_sent_requests(self):
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.client.logout()  # log out user1
#         # now try to update as stranger
#         # post update request without logging in
#         response = self.client.put(self.request_send_detail_url(create_response.json()['id']), {'receiver_username': self.valid_username2, 'request_reasoning':'Malicious attempt to update request.'})
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can delete their sent requests
#     def test_user_can_delete_their_sent_requests(self):
#         # post login
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # post delete request
#         response = self.client.delete(self.request_send_detail_url(request_id))
#         # response should be 204 No Content
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     # other user cannot delete users sent requests, as they are not sender
#     def test_user_cannot_delete_other_users_sent_requests(self):
#         # user3 can not delete user1 sent requests, as user3 is not sender    
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # now log in user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # post delete request
#         response = self.client.delete(self.request_send_detail_url(request_id))
#         # response should be 404 Not Found, as user3 is not sender of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger cannot delete users sent requests
#     def test_stranger_cannot_delete_users_sent_requests(self):
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.client.logout()  # log out user1
#         # now try to delete as stranger
#         # post delete request without logging in
#         response = self.client.delete(self.request_send_detail_url(create_response.json()['id']))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can create request identity variants for their sent requests
#     def test_user_can_create_request_identity_variants_for_sent_requests(self): 
#         # post login
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # post create request identity variant
#         response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         # response should be 201 Created
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # response data should have a 'label', 'context', 'variant' fields
#         self.assertIn('label', response.json())
#         self.assertIn('context', response.json())

#         # response data should have the same data as the one sent
#         self.assertEqual(response.json()['label'], self.valid_request_identity_variant_data['label'])
#         self.assertEqual(response.json()['context'], self.valid_request_identity_variant_data['context'])

#     # user cannot create request identity variants for other users sent requests, as they are not sender
#     def test_user_cannot_create_request_identity_variants_for_other_users_sent_requests(self):  
#         # Ezma user3 can not create request identity variants for user1 sent requests, as user3 is not sender    
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # now log in user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # post create request identity variant
#         response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         # response should be 404 Not Found, as user3 is not sender of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger cannot create request identity variants for users sent requests
#     def test_stranger_cannot_create_request_identity_variants_for_users_sent_requests(self):
#         # post login user1
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.client.logout()  # log out user1
#         # now try to create request identity variant as stranger
#         response = self.client.post(self.request_send_request_identity_variant_list_create_url(create_response.json()['id']), self.valid_request_identity_variant_data)
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)        

    
# # user can see their request identity variants for sent requests
#     def test_user_can_see_their_request_identity_variants_for_sent_requests(self):  
#         # post login
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         # post create request
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_response.json()['id']
#         # post create request identity variant
#         self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         # get request identity variants for sent requests
#         response = self.client.get(self.request_send_request_identity_variant_list_create_url(request_id))
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should be a list
#         self.assertIsInstance(response.json(), list)
#         # response data should have the created request identity variant
#         self.assertGreater(len(response.json()), 0)
#         # check if the created request identity variant is in the response data
#         created_request_identity_variant = response.json()[0]
#         self.assertEqual(created_request_identity_variant['label'], self.valid_request_identity_variant_data['label'])
#         self.assertEqual(created_request_identity_variant['context'], self.valid_request_identity_variant_data['context'])      

#     # user cannot see other users request identity variants for sent requests, as they are not sender
#     def test_user_cannot_see_other_users_request_identity_variants_for_sent_requests(self):
#         # Ezma (user3) can not see user1 request identity variants for sent requests, as Ezma not sender    
#         # post login user1, create request and request identity variant
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_request_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         # response should be 201 Created
#         self.assertEqual(create_request_response.status_code, status.HTTP_201_CREATED)
#         # get the created request id
#         request_id = create_request_response.json()['id']
#         # post create request identity variant
#         create_request_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         # response should be 201 Created
#         self.assertEqual(create_request_variant_response.status_code, status.HTTP_201_CREATED)
#         responseGotData = self.client.get(self.request_send_request_identity_variant_list_create_url(request_id))
#         # response got data sohuld be 200 OK and should contain the created request identity variant
#         self.assertEqual(responseGotData.status_code, status.HTTP_200_OK)
#         self.assertIsInstance(responseGotData.json(), list)
#         self.assertGreater(len(responseGotData.json()), 0)
#         # check if the created request identity variant is in the response data
#         created_request_identity_variant = responseGotData.json()[0]
#         self.assertEqual(created_request_identity_variant['label'], self.valid_request_identity_variant_data['label'])
#         self.assertEqual(created_request_identity_variant['context'], self.valid_request_identity_variant_data['context'])
#         # log out user1 and log in user3
#         self.client.logout()
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # now malicious Ezma (user3) tries to see request identity variants that user1 sent to user2
#         # DRF does not check parent permissions, Security-through-obscurity 
#         response = self.client.get(self.request_send_request_identity_variant_list_create_url(request_id))
#         # response should de 200, but it should be different then responseGotData
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should be a list
#         self.assertIsInstance(response.json(), list)
#         # response data should be empty, as user3 is not sender of any requests
#         self.assertEqual(len(response.json()), 0)
#         # there should be no label or context in the response data
#         self.assertNotIn('label', response.json())
#         self.assertNotIn('context', response.json())
#         # response data should be different for user1 that is sender and user3 that is not sender
#         self.assertNotEqual(responseGotData.json(), response.json())

#     # user can see request identity variants detail
#     def test_user_can_see_request_identity_variants_detail(self):
#         # post login, create request, and create request identity variant
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         # i have request_id and request identity variant id, now i can get the request identity variant detail
#         response = self.client.get(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id))
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the created request identity variant details
#         self.assertIn('label', response.json())
#         self.assertEqual(response.json()['label'], self.valid_request_identity_variant_data['label'])
#         self.assertIn('context', response.json())
#         self.assertEqual(response.json()['context'], self.valid_request_identity_variant_data['context'])
#         print("Response line 710", response.json()['label'])

#     # user can not see other users request identity variants detail
#     def test_user_cannot_see_other_users_request_identity_variants_detail(self):
#         # Ezma (user3) can not see user1 request identity variants detail, as user3 is not sender    
#         # login user 1, create request and variant 
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         self.client.logout()  # log out user1
#         # now log in user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # try to get request identity variant detail
#         response = self.client.get(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id))
#         # response should be 404 Not Found, as user3 is not sender of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)      

#     # stranger can not see users request identity variants detail
#     def test_stranger_cannot_see_users_request_identity_variants_detail(self):
#         # post login user1, create request and variant 
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         self.client.logout()  # log out user1
#         # now try to get request identity variant detail as stranger
#         response = self.client.get(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can update request identity variant 
#     def test_user_can_update_request_identity_variant(self):
#         # post login user 1, create request, and create request identity variant
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED) 
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         # now update the request identity variant
#         updated_data = {
#             'label': 'Updated First Name in Polish',
#             'context': 'Updated first name in Polish language.',
#         }
#         response = self.client.put(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id), updated_data)
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated data
#         self.assertIn('label', response.json())
#         self.assertEqual(response.json()['label'], updated_data['label'])
#         self.assertIn('context', response.json())
#         self.assertEqual(response.json()['context'], updated_data['context'])

#     # user can not update other users request identity variant
#     def test_user_cannot_update_other_users_request_identity_variant(self):
#         # Ezma (user3) can not update user1 request identity variant, as user3 is not sender    
#         # post login user1, create request and variant 
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         self.client.logout()  # log out user1
#         # now log in user3, and try to update users1 request identity variant
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         updated_data = {
#             'label': 'Malicious Update First Name in Polish',
#             'context': 'Malicious updated first name in Polish language.',
#         }
#         response = self.client.put(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id), updated_data)
#         # response should be 404 Not Found, as user3 is not sender of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not update users request identity variant
#     def test_stranger_cannot_update_users_request_identity_variant(self):
#         # post login user1, create request and variant 
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         self.client.logout()  # log out user1
#         # now try to update request identity variant as stranger
#         updated_data = {
#             'label': 'Malicious Update First Name in Polish',
#             'context': 'Malicious updated first name in Polish language.',
#         }
#         response = self.client.put(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id), updated_data)
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user sender can not update link field that is meant for receiver to manage 
#     def test_user_sender_can_not_update_link_field_for_receiver(self):
#         # post login user1, create request, and create request identity variant
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED) 
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         # now try to update the link field
#         updated_data = {
#             'label': 'updated label',
#             'context': 'updated context',
#             'user_provided_variant': '1',  # 'user_provided_variant' is read only sender should not be able to update it and fish the request user data 
#         }
#         response = self.client.put(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id), updated_data)
#         # response should be 200 becaue label and context get updated, but user_provided_variant should not be updated
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated data
#         self.assertIn('label', response.json())
#         self.assertEqual(response.json()['label'], updated_data['label'])
#         self.assertIn('context', response.json())
#         self.assertEqual(response.json()['context'], updated_data['context'])
#         # user_provided_variant should not be updated, it should be read only for sender
#         self.assertIn('user_provided_variant', response.json())
#         self.assertEqual(response.json()['user_provided_variant'], None)  # should stay none instead of of attempted inser value 

#     # stranger can not update users request identity variant link field
#     def test_stranger_cannot_update_users_request_identity_variant_link_field(self):
#         # post login user1, create request and variant 
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         self.client.logout()  # log out user1
#         # now try to update request identity variant as stranger
#         updated_data = {    
#             'label': 'Malicious Update First Name in Polish',
#             'context': 'Malicious updated first name in Polish language.',
#             'user_provided_variant': '1',  # 'user_provided_variant' is read only sender should not be able to update it and fish the request user data 
#         }
#         response = self.client.put(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id), updated_data)
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can delete request identity variant
#     def test_user_can_delete_request_identity_variant(self):
#         # post login user1, create request, and create request identity variant
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED) 
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         # now delete the request identity variant
#         response = self.client.delete(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id))
#         # response should be 204 No Content
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         # to make sure I will try to get the deleted request identity variant
#         response = self.client.get(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id))
#         # response should be 404 Not Found, as the request identity variant was deleted
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # user can not delete other users request identity variant
#     def test_user_cannot_delete_other_users_request_identity_variant(self):
#         # Ezma (user3) can not delete user1 request identity variant, as user3 is not sender    
#         # post login user1, create request and variant 
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         self.client.logout()  # log out user1
#         # now log in user3, and try to delete users1 request identity variant
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         response = self.client.delete(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id))
#         # response should be 404 Not Found, as user3 is not sender of this request identity variant
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   

#     # stranger can not delete users request identity variant    
#     def test_stranger_cannot_delete_users_request_identity_variant(self):
#         # post login user1, create request and variant 
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
#         self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
#         request_id = create_response.json()['id']
#         create_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
#         self.assertEqual(create_variant_response.status_code, status.HTTP_201_CREATED)
#         request_identity_variant_id = create_variant_response.json()['id']
#         self.client.logout()  # log out user1
#         # now try to delete request identity variant as stranger
#         response = self.client.delete(self.request_send_request_identity_variant_detail_url(request_id, request_identity_variant_id))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# # Received 

# class RequestsReceiveTests(TestCase):
#     def setUp(self):
#         # I need at least two users to test requests between them
#         # Create valid user credentials
#         self.valid_username1 = 'Johny'
#         self.valid_password1 = 'test123123'
#         self.valid_email1 = 'johny@example.com'
#         # Create a user with valid credentials
#         self.user = User.objects.create_user(
#             username=self.valid_username1,
#             email=self.valid_email1,
#             password=self.valid_password1,
#         )  
#         self.valid_user1_login_data = {
#             'username': 'Johny',
#             'password': 'test123123',
#         }

#         self.valid_username2 = 'Michael'
#         self.valid_password2 = 'test123123'
#         self.valid_email2 = 'michael@example.com'
#         # Create a user with valid credentials
#         self.user2 = User.objects.create_user(
#             username=self.valid_username2,
#             email=self.valid_email2,
#             password=self.valid_password2,
#         )
#         self.valid_user2_login_data = {
#             'username': 'Michael',
#             'password': 'test123123',
#         }

#         # user that will try to do malicuous actions
#         self.valid_username3 = 'Ezma'
#         self.valid_password3 = 'test123123'
#         self.valid_email3 = 'ezma@example.cam'
#         # Create a user with valid credentials
#         self.user3 = User.objects.create_user(
#             username=self.valid_username3,
#             email=self.valid_email3,
#             password=self.valid_password3,
#         )
#         self.valid_user3_login_data = {
#             'username': 'Ezma',
#             'password': 'test123123',
#         }

#         self.valid_request_identity_variant_data = {
#             'label': 'First Name in Polish',
#             'context': 'First name in Polish language.',
#         }   

#         # create requests, since i already tested that user can create sent request, i will set them in setup 
#         # create a request from user1 to user2
#         self.request1 = Request.objects.create(
#             sender=self.user,
#             receiver=self.user2,
#             request_reasoning='Dental office data request.',
#         )

#         # create request identity variant for request1
#         self.request_identity_variant1 = RequestIdentityVariant.objects.create(
#             request=self.request1,
#             label='First Name in Polish',
#             context='First name in Polish language.',
#         )

#         # create profile identity variant for user2
#         self.profile_identity_variant1 = ProfileIdentityVariant.objects.create(
#             user=self.user2,
#             label='First Name in Polish',
#             context='First name in Polish language.',
#             variant='Michal'
#         )

#         self.profile_identity_variant2 = ProfileIdentityVariant.objects.create(
#             user=self.user2,
#             label='First Name in Polish, Polish alphabet',
#             context='My first name in Polish language, but also with Polish alphabet.',
#             variant='Michał'
#         )

#         # Define URLs for requests
#         self.request_receive_list_url = reverse('api-request-receive-list')
#         self.request_receive_detail_url = lambda pk: reverse('api-request-receive-detail', args=[pk]) 
#         self.request_receive_request_identity_variant_list_url = lambda pk: reverse('api-request-receive-request-identity-variant-list', args=[pk])
#         self.request_receive_request_identity_variant_detail_url = lambda pk, request_identity_variant_pk: reverse('api-request-receive-request-identity-variant-detail', args=[pk, request_identity_variant_pk])
#         self.request_receive_accept_url = lambda pk: reverse('api-request-receive-accept', args=[pk])
#         self.request_receive_deny_url = lambda pk: reverse('api-request-receive-deny', args=[pk])       

#     # user can see list of received requests
#     def test_user_can_see_list_of_received_requests(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # get received requests
#         response = self.client.get(self.request_receive_list_url)
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should be a list
#         self.assertIsInstance(response.json(), list)
#         # response data should have the created request
#         self.assertGreater(len(response.json()), 0)
#         # check if the created request is in the response data
#         received_request = response.json()[0]
#         self.assertEqual(received_request['sender_username'], self.valid_username1)
#         self.assertEqual(received_request['request_reasoning'], 'Dental office data request.')  

#     # user can not see other  users list of received requests 
#     def test_user_cannot_see_other_users_list_of_received_requests(self):
#         # user3 can not see user2 received requests, as user3 is not receiver    
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password2)
#         # get received requests
#         response = self.client.get(self.request_receive_list_url)
#         # response should be 200 OK, because its correct request 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response should be list, but it should be empy, because the only request in database is from user1 to user2
#         # and user3 should not be able to see it 
#         self.assertIsInstance(response.json(), list)
#         self.assertEqual(len(response.json()), 0)

#     # stranger cannot see users received requests
#     def test_stranger_cannot_see_users_received_requests(self):
#         # get received requests without logging in
#         response = self.client.get(self.request_receive_list_url)
#         # response should be 401 Unauthorized 
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can see details of their received requests
#     def test_user_can_see_details_of_their_received_requests(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # get details of the received request
#         response = self.client.get(self.request_receive_detail_url(1))  # request id is 1, as it is the first request created in setup
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK) 
#         # response data should have the created request details
#         self.assertIn('sender_username', response.json())
#         self.assertEqual(response.json()['sender_username'], self.valid_username1)
#         self.assertIn('request_reasoning', response.json())
#         self.assertEqual(response.json()['request_reasoning'], 'Dental office data request.')
#         # request detail also has list of request identity variants, so i will check if it is there
#         self.assertIn('request_identity_variants', response.json())
#         # request identity variants should be a list
#         self.assertIsInstance(response.json()['request_identity_variants'], list)
#         # request identity variants should have at least one item, as we created one in setup
#         self.assertGreater(len(response.json()['request_identity_variants']), 0)
#         # check if the created request identity variant is in the response data
#         created_request_identity_variant = response.json()['request_identity_variants'][0]
#         self.assertEqual(created_request_identity_variant['label'], self.request_identity_variant1.label)
#         self.assertEqual(created_request_identity_variant['context'], self.request_identity_variant1.context)

#     # user cannot see details of other users received requests, as they are not receiver
#     def test_user_cannot_see_details_of_other_users_received_requests(self):    
#         # Ezma (user3) can not see user2 received requests, as user3 is not receiver    
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # get details of the received request
#         response = self.client.get(self.request_receive_detail_url(1))
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger cannot see users received requests details
#     def test_stranger_cannot_see_users_received_requests_details(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # get details of the received request
#         response = self.client.get(self.request_receive_detail_url(1))  # request id is 1 
#         self.client.logout()  # log out user2
#         # now try to get details as stranger
#         response = self.client.get(self.request_receive_detail_url(1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can accept their received request
#     def test_user_can_accept_their_received_request(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # accept the received request
#         response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request status
#         self.assertIn('status', response.json())
#         self.assertEqual(response.json()['status'], 'accepted')

#     # user can not accept others users requests 
#     def test_user_cannot_accept_other_users_received_request(self):
#         # Ezma can not accept the request for user 2   
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # accept the received request
#         response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
#         # response should be 404 Not Found, since user 3  does not even see that request 
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger cannot accept users received requests
#     def test_stranger_cannot_accept_users_received_requests(self):
#         # user 2 request is trying to be accepted by stranger
#         response = self.client.put(self.request_receive_accept_url(1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can deny their received request 
#     def test_user_can_deny_their_received_request(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # deny the received request
#         response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request status
#         self.assertIn('status', response.json())
#         self.assertEqual(response.json()['status'], 'denied')

#     # user can not deny other users requests
#     def test_user_cannot_deny_other_users_received_request(self):
#         # Ezma can not deny the request for user 2   
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # deny the received request
#         response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
#         # response should be 404 Not Found, since user 3 does not even see that request 
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger cannot deny users received requests
#     def test_stranger_cannot_deny_users_received_requests(self):
#         # user 2 request is trying to be denied by stranger
#         response = self.client.put(self.request_receive_deny_url(1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can see requequest identity variants list, for request 
#     def test_user_can_see_request_identity_variants_for_their_received_requests(self):  
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # get request identity variants for received requests
#         response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should be a list
#         self.assertIsInstance(response.json(), list)
#         # response data should have the created request identity variant
#         self.assertGreater(len(response.json()), 0)
#         # check if the created request identity variant is in the response data
#         created_request_identity_variant = response.json()[0]
#         self.assertEqual(created_request_identity_variant['label'], self.request_identity_variant1.label)
#         self.assertEqual(created_request_identity_variant['context'], self.request_identity_variant1.context)       

#     # user cannot see request identity variants for other users  
#     def test_user_cannot_see_request_identity_variants_for_other_users_received_requests(self):
#         # user3 Ezma tries to see user2 identity variants for request their received
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # get request identity variants for received requests
#         response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
#         # response should empty list, since there is no resources to show that user 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsInstance(response.json(), list)
#         self.assertEqual(len(response.json()), 0)

#     # stranger cannot see users request identity variants for received requests
#     def test_stranger_cannot_see_users_request_identity_variants_for_received_requests(self):
#         # get request identity variants for received requests without logging in
#         response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user receiver can not see request identity variant detail for their received request that is pending 
#     def test_user_receiver_can_not_see_request_identity_variant_detail_for_their_received_requests_that_are_pending(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # get request identity variant detail for received requests
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 403 forbidden 
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#     # user can not see other users request identity variant detail ( using receiver end point ) that is pending 
#     def test_user_cannot_see_other_users_request_identity_variant_detail_pending(self): 
#         # Ezma (user3) can not see user2 request identity variant detail, as user3 is not receiver    
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # try to get request identity variant detail
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not see users request identity variant detail  that is pending 
#     def test_stranger_cannot_see_users_request_identity_variant_detail_pending(self):
#         # requestId is 1, and request identity variant id is 1
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


#     # user can not see request identity variant detail, that is declined 
#     def test_user_receiver_can_not_see_request_identity_variant_detail_for_their_received_requests_that_are_denied(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # first deny the request
#         response = self.client.put(self.request_receive_deny_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now try to get the request identity variant detail
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 403 Forbidden, as the request is denied
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     # user can not see other users request identity variant detail ( using receiver end point ) that is denied
#     def test_user_cannot_see_other_users_request_identity_variant_detail_denied(self):
#         # log in as user 2 and deny the request first 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_deny_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now Ezma (user3) tries to see user2 request identity variant detail,
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # now try to get request identity variant detail
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not see users request identity variant detail  that is denied   
#     def test_stranger_cannot_see_users_request_identity_variant_detail_denied(self):
#         # post login user2 and deny the request first 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_deny_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now try to get request identity variant detail as stranger
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


#     # user can accept request that is pending 
#     def test_user_can_accept_request_that_is_pending(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # accept the received request
#         response = self.client.put(self.request_receive_accept_url(1))
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request status
#         self.assertIn('status', response.json())
#         self.assertEqual(response.json()['status'], 'accepted') 

#     # user can not accept request for other user that is pending 
#     def test_user_cannot_accept_other_users_request_that_is_pending(self):
#         # Ezma (user3) can not accept user2 request  
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # try to accept the received request
#         response = self.client.put(self.request_receive_accept_url(1))
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not accept users request that is pending
#     def test_stranger_cannot_accept_users_request_that_is_pending(self):
#         # user2 request is trying to be accepted by stranger
#         response = self.client.put(self.request_receive_accept_url(1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can change their mind and accept request that is denied
#     def test_user_can_accept_request_that_is_denied(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # first deny the request
#         response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now accept the request
#         response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request status
#         self.assertIn('status', response.json())
#         self.assertEqual(response.json()['status'], 'accepted')

#     # user can not accept other users request that is denied
#     def test_user_cannot_accept_other_users_request_that_is_denied(self):
#         # post login user2 and deny request
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now Ezma tries to maliciously accept user2 request
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         response = self.client.put(self.request_receive_accept_url(1))
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not accept users request that is denied
#     def test_stranger_cannot_accept_users_request_that_is_denied(self):
#           # post login user2 and deny request
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now try to accetp the request as stranger, without logging in 
#         response = self.client.put(self.request_receive_accept_url(1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can deny request that is pending
#     def test_user_can_deny_request_that_is_pending(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # deny the received request
#         response = self.client.put(self.request_receive_deny_url(1))
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request status
#         self.assertIn('status', response.json())
#         self.assertEqual(response.json()['status'], 'denied')

#     # user can not deny other users request that is pending
#     def test_user_cannot_deny_other_users_request_that_is_pending(self):
#         # Ezma (user3) can not deny user2 request  
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # try to deny the received request
#         response = self.client.put(self.request_receive_deny_url(1))
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not deny users request that is pending
#     def test_stranger_cannot_deny_users_request_that_is_pending(self):
#         # now try to deny the request as stranger, without logging in
#         response = self.client.put(self.request_receive_deny_url(1))
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can change their minde and deny request that is accepted 
#     def test_user_can_deny_request_that_is_accepted(self):
#         # post login user2, and accept it 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now deny the request
#         response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request status
#         self.assertIn('status', response.json())
#         self.assertEqual(response.json()['status'], 'denied')

#     # user can not deny other users request that is accepted
#     def test_user_cannot_deny_other_users_request_that_is_accepted(self):
#         # post login user2, and accept it 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now Ezma tries to maliciously deny user2 request
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         response = self.client.put(self.request_receive_deny_url(1))
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not deny users request that is accepted
#     def test_stranger_cannot_deny_users_request_that_is_accepted(self):
#         # post login user2, and accept it 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now try to deny the request as stranger, without logging in
#         response = self.client.put(self.request_receive_deny_url(1))
#         # should be 401 since user is not authenticated 
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can see request identity variant detail for accepted request
#     def test_user_can_see_request_identity_variant_detail_for_accepted_request(self):
#         # post login user2 and accept request 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now get request identity variant detail for accepted request  
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the created request identity variant details
#         self.assertIn('label', response.json())
#         self.assertEqual(response.json()['label'], self.request_identity_variant1.label)
#         self.assertIn('context', response.json())
#         self.assertEqual(response.json()['context'], self.request_identity_variant1.context)
    
#     # user can not see other users request identity variant detail ( using receiver end point ) for accepted request
#     def test_user_cannot_see_other_users_request_identity_variant_detail_for_accepted_request(self):
#         # log in as user2, accept request, loggout, 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()
#         # now Ezma tries to see users2 request identity variant detail,
#         self.client.login(username=self.valid_username1, password=self.valid_password1)
#         response = self.client.get(self.request_receive_request_identity_variant_detail_url(1, 1))
#         # response should be 404 Not Found, as user1 is not receiver of this request and there is no resource to show 
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # user can link request identity variant with profile identity variant for accepted request
#     def test_user_can_link_request_identity_variant_with_profile_identity_variant_for_accepted_request(self):
#         # post login user2 and accept request 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now link request identity variant with profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request identity variant details
#         self.assertIn('link_to_id_profile_identity_variant', response.json())
#         # now the profile id is 1 
#         self.assertEqual(response.json()['link_to_id_profile_identity_variant'], 1)
#         # and part that is shared with the request person is the variant, so it should be the same as profile identity variant - variant field 
#         self.assertEqual(response.json()['user_provided_variant'], self.profile_identity_variant1.variant)
#         print(" code line 1436 ")
#         print(response.json()['user_provided_variant'])

#     # user can not link other users request identity variant with profile identity variant for accepted request
#     def test_user_cannot_link_other_users_request_identity_variant_with_profile_identity_variant_for_accepted_request(self):
#         # post login user2 and accept request 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now Ezma tries to link user2 request identity variant with profile identity variant
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response should be 404 Not Found
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not link users request identity variant with profile identity variant for accepted request
#     def test_stranger_cannot_link_users_request_identity_variant_with_profile_identity_variant_for_accepted_request(self):
#         # post login user2 and accept request 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now try to link request identity variant with profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # repsponse should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can not link request identity variant with profile identity variant for pending request
#     def test_user_cannot_link_request_identity_variant_with_profile_identity_variant_for_pending_request(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # try to link request identity variant with profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response should be 403 Forbidden, as the request is pending
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     # user can not link other users request identity variant with profile identity variant for pending request
#     def test_user_cannot_link_other_users_request_identity_variant_with_profile_identity_variant_for_pending_request(self): 
#         # Ezma (user3) can not link user2 request identity variant with profile identity variant, as user3  is not receiver    
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # try to link request identity variant with profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not link users request identity variant with profile identity variant for pending request
#     def test_stranger_cannot_link_users_request_identity_variant_with_profile_identity_variant_for_pending_request(self):
#         # try to link request identity variant with profile identity variant without logging in
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can not link request identity variant with profile identity variant for denied request
#     def test_user_cannot_link_request_identity_variant_with_profile_identity_variant_for_denied_request(self):
#         # post login user2 and deny request 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_deny_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now try to link request identity variant with profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response should be 403 Forbidden, as the request is denied
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)   

#     # user can not link other users request identity variant with profile identity variant for denied request
#     def test_user_cannot_link_other_users_request_identity_variant_with_profile_identity_variant_for_denied_request(self):
#         # login as user 2 and deny the request first
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_deny_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # now Ezma tries to link user2 request identity variant with profile identity variant
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # now try to link other users request identity variant with profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response sholuld be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
#     # stranger can not link users request identity variant with profile identity variant for denied request
#     def test_stranger_cannot_link_users_request_identity_variant_with_profile_identity_variant_for_denied_request(self):
#         # login user 2, deny request, logout  
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_deny_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client.logout()  # log out user2
#         # try to link without logging in 
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user can update link field of request identity variant to link it with different profile identity variant
#     def test_user_can_update_link_field_of_request_identity_variant_to_link_it_with_different_profile_identity_variant(self):
#         # post login user2 and accept request 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         response = self.client.put(self.request_receive_accept_url(1))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now link request identity variant with profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # now update link field to link it with different profile identity variant
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 2})
#         # response should be 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # response data should have the updated request identity variant details
#         self.assertIn('link_to_id_profile_identity_variant', response.json())
#         # now the profile id is 2 
#         self.assertEqual(response.json()['link_to_id_profile_identity_variant'], 2)
#         # and part that is shared with the request person is the variant, so it should be the same as profile identity variant - variant field 
#         self.assertEqual(response.json()['user_provided_variant'], self.profile_identity_variant2.variant)

#     # other user can not update link field of request identity variant to link it with profile identity variant
#     def test_other_user_cannot_update_link_field_of_request_identity_variant_to_link_it_with_profile_identity_variant(self):
#         # login user 3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # try to update link field
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 2})
#         # response should be 404 Not Found, as user3 is not receiver of this request, so there is no resource to even show 
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not update link field of request identity variant to link it with profile identity variant      
#     def test_stranger_cannot_update_link_field_of_request_identity_variant_to_link_it_with_profile_identity_variant(self):
#         # try to update link field without logging in
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 2})
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # user receiver can not update request identity variant detail other thenk link field 
#     def test_user_receiver_can_not_update_request_identity_variant_detail_other_than_link_field(self):
#         # post login user2
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         # try to update request identity variant detail
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'label': 'new label'})
#         # response should be 403 Forbidden, as the request is pending
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     # user (that is not a sender ) can not update other users request identity variant detail ( using receiver end point )
#     def test_user_cannot_update_other_users_request_identity_variant_detail(self):
#         # Ezma (user3) can not update user2 request identity variant detail, as user3 is not receiver    
#         # post login user3
#         self.client.login(username=self.valid_username3, password=self.valid_password3)
#         # try to update request identity variant detail
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'label': 'new label'})
#         # response should be 404 Not Found, as user3 is not receiver of this request
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     # stranger can not update users request identity variant detail 
#     def test_stranger_cannot_update_users_request_identity_variant_detail(self):
#         # try to update request identity variant detail without logging in
#         response = self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'label': 'new label'})
#         # response should be 401 Unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     # test if links get cleaned, when user is changing from accepted to denied
#     def test_links_get_disconnected_upon_denying_the_request(self):
#         # post login user2 and accept request, and link variant 
#         self.client.login(username=self.valid_username2, password=self.valid_password2)
#         self.client.put(self.request_receive_accept_url(1))
#         self.client.patch(self.request_receive_request_identity_variant_detail_url(1, 1), {'link_to_id_profile_identity_variant': 1})
#         # get the link data that sender sees 
#         response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
#         shared_variant = response.json()[0].get('user_provided_variant')
#         self.assertEqual(shared_variant, self.profile_identity_variant1.variant)
#         print("shared_variant: ", shared_variant)
#         # now deny the request, data should be wiped and no longer shared 
#         self.client.put(self.request_receive_deny_url(1))
#         response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
#         cleaned_variant = response.json()[0].get('user_provided_variant')
#         # now cleaned variant shoud be different then shared variant, just by denying the request
#         self.assertNotEqual(shared_variant, cleaned_variant)
#         # and shared cleaned_variant shoud be None
#         self.assertIsNone(cleaned_variant)
#         # that means that just deying the request, destroy the link to users private information 
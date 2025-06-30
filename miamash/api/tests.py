from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 
from django.contrib.auth import get_user_model
from core.models import Request, ProfileIdentityVariant, RequestIdentityVariant
User = get_user_model() # in case of at some point using custom user model

# import response 
## REGISTRATION AND LOGIN ## 
class AuthenticationTests(APITestCase):
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

        # Create a user existing username 

        # Define URLs for registration, login, and logout
        self.register_url = reverse('rest_register')
        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        

    # user can log in  with good credentials
    def test_user_can_login_with_good_credentials(self):
        # post login 
        response = self.client.post(self.login_url, self.valid_user_login_data)
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should have a 'key' which is a token
        self.assertIn('key', response.json())  

    # user cannot log in with bad credentials
    def test_user_cannot_login_with_bad_credentials(self):
        # post login wrong password
        response = self.client.post(self.login_url, self.wrong_user_login_password_data)
        # repsonse should be 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # post login wrong username
        response = self.client.post(self.login_url, self.wrong_user_login_username_data)
        # response should be 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # user can log out
    def test_user_can_logout(self):
        # post login
        self.client.login(username=self.valid_username, password=self.valid_password)
        # post logout
        response = self.client.post(self.logout_url)
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should have a 'detail' message
        self.assertEqual(response.json()['detail'],'Successfully logged out.')

    # user can register with good credentials
    def test_user_can_register_with_good_credentials(self):
        # post register with valid data
        response = self.client.post(self.register_url, self.valid_user_registration_data)
        # response should be 201 Created
        print(response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # response data should have a 'key' which is a token
        self.assertIn('key', response.json())  

    # test if user is unique
    def test_user_cannot_register_with_existing_username(self):
        # post register with existing username
        response = self.client.post(self.register_url, username=self.valid_username, email='john1@example.com', password=self.valid_password)
        print(response.status_code, response.json())
        # response should be 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # response data should have a 'username' error
        self.assertIn('username', response.json())
        self.assertIn('email', response.json())

    # user cannot register with bad credentials
    def test_user_cannot_register_with_bad_credentials(self):
        # post register with invalid data
        response = self.client.post(self.register_url, self.invalid_user_registration_data)
        # response should be 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # response data should have a 'username', 'email', 'password1', 'password2' errors
        self.assertIn('username', response.json())
        self.assertIn('email', response.json())
        self.assertIn('password1', response.json())
        self.assertIn('password2', response.json())
        

## PROFILE IDENTITY VARIANTS ## 
class ProfileIdentityVariantsTests(APITestCase):
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
        self.profile_identity_variant_list_create_url = reverse('profile-identity-variant-list-create')
        self.profile_identity_variant_detail_url = lambda pk: reverse('profile-identity-variant-detail', args=[pk])     

    # user can create their profile identity variants
    def test_user_can_create_their_identity_variants(self):
        # log in the user
        self.client.login(username=self.valid_username, password=self.valid_password)
        # post create profile identity variant
        response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
        # response should be 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # response data should have a fields 'label', 'context', 'variant'
        self.assertIn('label', response.json())
        self.assertIn('context', response.json())
        self.assertIn('variant', response.json())
        # response data should have the same data as the one sent
        self.assertEqual(response.json()['label'], self.valid_identity_variant_data['label'])
        self.assertEqual(response.json()['context'], self.valid_identity_variant_data['context'])
        self.assertEqual(response.json()['variant'], self.valid_identity_variant_data['variant'])


    # stranger cannot create users profile identity variants
    def test_stranger_cannot_create_users_identity_variants(self):
        # post create profile identity variant without logging in
        response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # user can see their identity varians 
    def test_user_can_see_their_identity_variants(self):
        # post login
        self.client.login(username=self.valid_username, password=self.valid_password)
        # get profile identity variants
        response = self.client.get(self.profile_identity_variant_list_create_url)
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should be a list
        self.assertIsInstance(response.json(), list)

    # stranger cannot see users profile identity variants 
    def test_stranger_cannot_see_users_identity_variants(self):
        # get profile identity variants without logging in
        response = self.client.get(self.profile_identity_variant_list_create_url)
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can update their profile identity variants 
    def test_user_can_update_their_identity_variants(self):
        # post login
        self.client.login(username=self.valid_username, password=self.valid_password)
        # create a profile identity variant
        create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created profile identity variant id
        identity_variant_id = create_response.json()['id']
        # post update profile identity variant
        response = self.client.put(self.profile_identity_variant_detail_url(identity_variant_id), self.valid_updated_identity_variant_data)
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should have the updated data
        self.assertEqual(response.json()['label'], self.valid_updated_identity_variant_data['label'])
        self.assertEqual(response.json()['context'], self.valid_updated_identity_variant_data['context'])
        self.assertEqual(response.json()['variant'], self.valid_updated_identity_variant_data['variant'])

    # stranger cannot update users profile identity variants
    def test_stranger_cannot_update_users_identity_variants(self):
        # log in, create variant, log out and try to access it as stranger to update 
        self.client.login(username=self.valid_username, password=self.valid_password)
        create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        identity_variant_id = create_response.json()['id']
        self.client.logout()    
        # now try to update as stranger
        response = self.client.put(self.profile_identity_variant_detail_url(identity_variant_id), self.valid_updated_identity_variant_data)
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can delete their profile identity variants
    def test_user_can_delete_their_identity_variants(self):
        # post login
        self.client.login(username=self.valid_username, password=self.valid_password)
        # create a profile identity variant
        create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created profile identity variant id
        identity_variant_id = create_response.json()['id']
        # post delete profile identity variant
        response = self.client.delete(self.profile_identity_variant_detail_url(identity_variant_id))
        # response should be 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # stranger cannot delete users profile identity variants
    def test_stranger_cannot_delete_users_identity_variants(self):
        # log in, create variant, log out and try to access it as stranger to delete 
        self.client.login(username=self.valid_username, password=self.valid_password)
        create_response = self.client.post(self.profile_identity_variant_list_create_url, self.valid_identity_variant_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        identity_variant_id = create_response.json()['id']
        self.client.logout()    
        # now try to delete as stranger
        response = self.client.delete(self.profile_identity_variant_detail_url(identity_variant_id))
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    


## REQUESTS ## 
# Send 
class RequestsSendTests(APITestCase):
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

        # Define URLs for requests
        self.request_send_list_create_url = reverse('request-send-list-create')
        self.request_send_detail_url = lambda pk: reverse('request-send-detail', args=[pk]) 
        self.request_send_request_identity_variant_list_create_url = lambda pk: reverse('request-send-request-identity-variant-list-create', args=[pk])
        self.request_send_request_identity_variant_detail_url = lambda pk, request_identity_variant_pk: reverse('request-send-request-identity-variant-detail', args=[pk, request_identity_variant_pk])

    # user can create new sent requests
    def test_user_can_create_new_sent_requests(self):
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'I need your identity information for this test.'})
        # response should be 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # response data should have a 'receiver' field with the username of the receiver
        self.assertIn('receiver_username', response.json())
        self.assertEqual(response.json()['receiver_username'], self.valid_username2)
        self.assertIn('request_reasoning', response.json())
        self.assertEqual(response.json()['request_reasoning'], 'I need your identity information for this test.')

    # user can not create sent requests for other users, checking post injections 
    def test_user_cannot_create_sent_requests_for_other_users(self):
        # user3 is malicious user trying to create request from user1 to user2, that should not be possible 
        # server does not take client data for sender, it uses loged in credentials to determine that
        # so the result should be still suscessful, but the sender will be user3, not user1
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # post create request
        response = self.client.post(self.request_send_list_create_url, {
            'sender_username': self.valid_username1,  # injection attempt to change sender, should be ignored by server 
            'receiver_username': self.valid_username2,
            'request_reasoning': 'Createing a request from user1 to user2, but I am malicious Emza - user3.'
        })
        # response should be 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # response data should have a 'receiver' field with the username of the receiver
        self.assertIn('receiver_username', response.json())
        self.assertEqual(response.json()['receiver_username'], self.valid_username2)
        self.assertIn('request_reasoning', response.json())
        self.assertEqual(response.json()['request_reasoning'], 'Createing a request from user1 to user2, but I am malicious Emza - user3.')
        data = response.json()
        # since response does not contain sender_username, i am going to pull request from database to check sender
        # and it should be user3, not malicious attept to change it to user1
        req = Request.objects.get(id=data['id'])
        self.assertEqual(req.sender, self.user3) # should be user3/logged in user, not user1
        self.assertNotEqual(req.sender, self.user) # should not be user1, as it was injection attempt

    # stranger cannot create sent requests for users
    def test_stranger_cannot_create_sent_requests_for_users(self):
        # post create request without logging in
        response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'I just want your data'})
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can see their sent requests
    def test_user_can_see_their_sent_requests(self):
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'This is dental office, we need your identity information.'})
        # get sent requests
        response = self.client.get(self.request_send_list_create_url)
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should be a list
        self.assertIsInstance(response.json(), list)
        # response data should have the created request
        self.assertGreater(len(response.json()), 0)  # should have at least one request
        # check if the created request is in the response data
        created_request = response.json()[0]
        self.assertEqual(created_request['receiver_username'], self.valid_username2)
        self.assertEqual(created_request['request_reasoning'], 'This is dental office, we need your identity information.')


    # user can not see other users sent requests, as they are not sender
    def test_user_cannot_see_other_users_sent_requests(self):
        # user3 can not see user1 sent requests, as Ezma is not a sender    
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'This is dental office, we need your identity information.'})
        # now log in user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # get sent requests
        response = self.client.get(self.request_send_list_create_url)
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should be a list
        self.assertIsInstance(response.json(), list)
        # response data should be empty, as user3 is not sender of any requests
        self.assertEqual(len(response.json()), 0)

    # stranger cannot see users sent requests
    def test_stranger_cannot_see_users_sent_requests(self):
        # post get sent requests without logging in
        response = self.client.get(self.request_send_list_create_url)
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can see details of their sent requests
    def test_user_can_see_details_of_their_sent_requests(self):
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # get details of the sent request
        response = self.client.get(self.request_send_detail_url(request_id))
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should have the created request details
        self.assertIn('receiver_username', response.json())
        self.assertEqual(response.json()['receiver_username'], self.valid_username2)
        self.assertIn('request_reasoning', response.json())
        self.assertEqual(response.json()['request_reasoning'], 'Dental office data request.')

    # user cannot see details of other users sent requests, as they are not sender
    def test_user_cannot_see_details_of_other_users_sent_requests(self):
        # malicious Ezma (user3) can not see user1 detail sent request, as she is not a sender 
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # now log in Ezma
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # get details of the sent request
        response = self.client.get(self.request_send_detail_url(request_id))
        # response should be 404 Not Found, as user3 is not sender of this request
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # stranger cannot see users sent requests details
    def test_stranger_cannot_see_users_sent_requests_details(self):
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        self.client.logout()  # log out user1
        # now try to get details as stranger
        response = self.client.get(self.request_send_detail_url(request_id))
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can update their sent requests
    def test_user_can_update_their_sent_requests(self):
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # post update request
        response = self.client.put(self.request_send_detail_url(request_id), {'receiver_username': self.valid_username2, 'request_reasoning':'Super dental office data request.'})
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should have the updated data
        self.assertIn('receiver_username', response.json())
        self.assertEqual(response.json()['receiver_username'], self.valid_username2)
        self.assertIn('request_reasoning', response.json())
        self.assertEqual(response.json()['request_reasoning'], 'Super dental office data request.')

    # user cannot update other users sent requests, as they are not sender
    def test_user_cannot_update_other_users_sent_requests(self):
        # Ezma  can not update user1 sent requests, as she is not sender
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # now log in user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # post update request
        response = self.client.put(self.request_send_detail_url(request_id), {'receiver_username': self.valid_username2, 'request_reasoning':'Malicious attempt to update request.'})
        # since this system queries from database only requests where sender is logged in user, so trying to get that id request will just result not found 
        # response should be 404 Not Found, as user3 is not sender of this request
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # stranger cannot update users sent requests
    def test_stranger_cannot_update_users_sent_requests(self):
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        self.client.logout()  # log out user1
        # now try to update as stranger
        # post update request without logging in
        response = self.client.put(self.request_send_detail_url(create_response.json()['id']), {'receiver_username': self.valid_username2, 'request_reasoning':'Malicious attempt to update request.'})
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can delete their sent requests
    def test_user_can_delete_their_sent_requests(self):
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # post delete request
        response = self.client.delete(self.request_send_detail_url(request_id))
        # response should be 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # other user cannot delete users sent requests, as they are not sender
    def test_user_cannot_delete_other_users_sent_requests(self):
        # user3 can not delete user1 sent requests, as she is not sender    
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # now log in user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # post delete request
        response = self.client.delete(self.request_send_detail_url(request_id))
        # response should be 404 Not Found, as user3 is not sender of this request
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # stranger cannot delete users sent requests
    def test_stranger_cannot_delete_users_sent_requests(self):
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        self.client.logout()  # log out user1
        # now try to delete as stranger
        # post delete request without logging in
        response = self.client.delete(self.request_send_detail_url(create_response.json()['id']))
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can create request identity variants for their sent requests
    def test_user_can_create_request_identity_variants_for_sent_requests(self): 
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # post create request identity variant
        response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
        # response should be 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # response data should have a 'label', 'context', 'variant' fields
        self.assertIn('label', response.json())
        self.assertIn('context', response.json())

        # response data should have the same data as the one sent
        self.assertEqual(response.json()['label'], self.valid_request_identity_variant_data['label'])
        self.assertEqual(response.json()['context'], self.valid_request_identity_variant_data['context'])

    # user cannot create request identity variants for other users sent requests, as they are not sender
    def test_user_cannot_create_request_identity_variants_for_other_users_sent_requests(self):  
        # Ezma user3 can not create request identity variants for user1 sent requests, as she is not sender    
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # now log in user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # post create request identity variant
        response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
        # response should be 404 Not Found, as user3 is not sender of this request
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # stranger cannot create request identity variants for users sent requests
    def test_stranger_cannot_create_request_identity_variants_for_users_sent_requests(self):
        # post login user1
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        self.client.logout()  # log out user1
        # now try to create request identity variant as stranger
        response = self.client.post(self.request_send_request_identity_variant_list_create_url(create_response.json()['id']), self.valid_request_identity_variant_data)
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)        

    
# user can see their request identity variants for sent requests
    def test_user_can_see_their_request_identity_variants_for_sent_requests(self):  
        # post login
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        # post create request
        create_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_response.json()['id']
        # post create request identity variant
        self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
        # get request identity variants for sent requests
        response = self.client.get(self.request_send_request_identity_variant_list_create_url(request_id))
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should be a list
        self.assertIsInstance(response.json(), list)
        # response data should have the created request identity variant
        self.assertGreater(len(response.json()), 0)
        # check if the created request identity variant is in the response data
        created_request_identity_variant = response.json()[0]
        self.assertEqual(created_request_identity_variant['label'], self.valid_request_identity_variant_data['label'])
        self.assertEqual(created_request_identity_variant['context'], self.valid_request_identity_variant_data['context'])      

    # user cannot see other users request identity variants for sent requests, as they are not sender
    def test_user_cannot_see_other_users_request_identity_variants_for_sent_requests(self):
        # Ezma (user3) can not see user1 request identity variants for sent requests, as Ezma not sender    
        # post login user1, create request and request identity variant
        self.client.login(username=self.valid_username1, password=self.valid_password1)
        create_request_response = self.client.post(self.request_send_list_create_url, {'receiver_username': self.valid_username2, 'request_reasoning':'Dental office data request.'})
        # response should be 201 Created
        self.assertEqual(create_request_response.status_code, status.HTTP_201_CREATED)
        # get the created request id
        request_id = create_request_response.json()['id']
        # post create request identity variant
        create_request_variant_response = self.client.post(self.request_send_request_identity_variant_list_create_url(request_id), self.valid_request_identity_variant_data)
        # response should be 201 Created
        self.assertEqual(create_request_variant_response.status_code, status.HTTP_201_CREATED)
        responseGotData = self.client.get(self.request_send_request_identity_variant_list_create_url(request_id))
        # response got data sohuld be 200 OK and should contain the created request identity variant
        self.assertEqual(responseGotData.status_code, status.HTTP_200_OK)
        self.assertIsInstance(responseGotData.json(), list)
        self.assertGreater(len(responseGotData.json()), 0)
        # check if the created request identity variant is in the response data
        created_request_identity_variant = responseGotData.json()[0]
        self.assertEqual(created_request_identity_variant['label'], self.valid_request_identity_variant_data['label'])
        self.assertEqual(created_request_identity_variant['context'], self.valid_request_identity_variant_data['context'])
        # log out user1 and log in user3
        self.client.logout()
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # now malicious Ezma (user3) tries to see request identity variants that user1 sent to user2
        # DRF does not check parent permissions, Security-through-obscurity 
        response = self.client.get(self.request_send_request_identity_variant_list_create_url(request_id))
        # response should de 200, but it should be different then responseGotData
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should be a list
        self.assertIsInstance(response.json(), list)
        # response data should be empty, as user3 is not sender of any requests
        self.assertEqual(len(response.json()), 0)
        # there should be no label or context in the response data
        self.assertNotIn('label', response.json())
        self.assertNotIn('context', response.json())
        # response data should be different for user1 that is sender and user3 that is not sender
        self.assertNotEqual(responseGotData.json(), response.json())





# Received 

class RequestsReceiveTests(APITestCase):
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

        # create requests, since i already tested that user can create sent request, i will set them in setup 
        # create a request from user1 to user2
        self.request1 = Request.objects.create(
            sender=self.user,
            receiver=self.user2,
            request_reasoning='Dental office data request.',
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
        )

        # Define URLs for requests
        self.request_receive_list_url = reverse('request-receive-list')
        self.request_receive_detail_url = lambda pk: reverse('request-receive-detail', args=[pk]) 
        self.request_receive_request_identity_variant_list_url = lambda pk: reverse('request-receive-request-identity-variant-list', args=[pk])
        self.request_receive_request_identity_variant_detail_url = lambda pk, request_identity_variant_pk: reverse('request-receive-request-identity-variant-detail', args=[pk, request_identity_variant_pk])
        self.request_receive_accept_url = lambda pk: reverse('request-receive-accept', args=[pk])
        self.request_receive_deny_url = lambda pk: reverse('request-receive-deny', args=[pk])       

    # user can see list of received requests
    def test_user_can_see_list_of_received_requests(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # get received requests
        response = self.client.get(self.request_receive_list_url)
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should be a list
        self.assertIsInstance(response.json(), list)
        # response data should have the created request
        self.assertGreater(len(response.json()), 0)
        # check if the created request is in the response data
        received_request = response.json()[0]
        self.assertEqual(received_request['sender_username'], self.valid_username1)
        self.assertEqual(received_request['request_reasoning'], 'Dental office data request.')  

    # user can not see other  users list of received requests 
    def test_user_cannot_see_other_users_list_of_received_requests(self):
        # user3 can not see user2 received requests, as she is not receiver    
        # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password2)
        # get received requests
        response = self.client.get(self.request_receive_list_url)
        # response should be 200 OK, because its correct request 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response should be list, but it should be empy, because the only request in database is from user1 to user2
        # and user3 should not be able to see it 
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 0)

    # stranger cannot see users received requests
    def test_stranger_cannot_see_users_received_requests(self):
        # get received requests without logging in
        response = self.client.get(self.request_receive_list_url)
        # response should be 401 Unauthorized 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can see details of their received requests
    def test_user_can_see_details_of_their_received_requests(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # get details of the received request
        response = self.client.get(self.request_receive_detail_url(1))  # request id is 1, as it is the first request created in setup
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        # response data should have the created request details
        self.assertIn('sender_username', response.json())
        self.assertEqual(response.json()['sender_username'], self.valid_username1)
        self.assertIn('request_reasoning', response.json())
        self.assertEqual(response.json()['request_reasoning'], 'Dental office data request.')
        # request detail also has list of request identity variants, so i will check if it is there
        self.assertIn('request_identity_variants', response.json())
        # request identity variants should be a list
        self.assertIsInstance(response.json()['request_identity_variants'], list)
        # request identity variants should have at least one item, as we created one in setup
        self.assertGreater(len(response.json()['request_identity_variants']), 0)
        # check if the created request identity variant is in the response data
        created_request_identity_variant = response.json()['request_identity_variants'][0]
        self.assertEqual(created_request_identity_variant['label'], self.request_identity_variant1.label)
        self.assertEqual(created_request_identity_variant['context'], self.request_identity_variant1.context)

    # user cannot see details of other users received requests, as they are not receiver
    def test_user_cannot_see_details_of_other_users_received_requests(self):    
        # Ezma (user3) can not see user2 received requests, as she is not receiver    
        # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # get details of the received request
        response = self.client.get(self.request_receive_detail_url(1))
        # response should be 404 Not Found, as user3 is not receiver of this request
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # stranger cannot see users received requests details
    def test_stranger_cannot_see_users_received_requests_details(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # get details of the received request
        response = self.client.get(self.request_receive_detail_url(1))  # request id is 1 
        self.client.logout()  # log out user2
        # now try to get details as stranger
        response = self.client.get(self.request_receive_detail_url(1))
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can accept their received request
    def test_user_can_accept_their_received_request(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # accept the received request
        response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should have the updated request status
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'accepted')

    # user can not accept others users requests 
    def test_user_cannot_accept_other_users_received_request(self):
        # Ezma can not accept the request for user 2   
        # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # accept the received request
        response = self.client.put(self.request_receive_accept_url(1))  # request id is 1 
        # response should be 404 Not Found, since user 3  does not even see that request 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # stranger cannot accept users received requests
    def test_stranger_cannot_accept_users_received_requests(self):
        # user 2 request is trying to be accepted by stranger
        response = self.client.put(self.request_receive_accept_url(1))
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can deny their received request 
    def test_user_can_deny_their_received_request(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # deny the received request
        response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should have the updated request status
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'denied')

    # user can not deny other users requests
    def test_user_cannot_deny_other_users_received_request(self):
        # Ezma can not deny the request for user 2   
        # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # deny the received request
        response = self.client.put(self.request_receive_deny_url(1))  # request id is 1 
        # response should be 404 Not Found, since user 3 does not even see that request 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # stranger cannot deny users received requests
    def test_stranger_cannot_deny_users_received_requests(self):
        # user 2 request is trying to be denied by stranger
        response = self.client.put(self.request_receive_deny_url(1))
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can see requequest identity variants list, for request 
    def test_user_can_see_request_identity_variants_for_their_received_requests(self):  
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        # get request identity variants for received requests
        response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
        # response should be 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response data should be a list
        self.assertIsInstance(response.json(), list)
        # response data should have the created request identity variant
        self.assertGreater(len(response.json()), 0)
        # check if the created request identity variant is in the response data
        created_request_identity_variant = response.json()[0]
        self.assertEqual(created_request_identity_variant['label'], self.request_identity_variant1.label)
        self.assertEqual(created_request_identity_variant['context'], self.request_identity_variant1.context)       

    # user cannot see request identity variants for other users  
    def test_user_cannot_see_request_identity_variants_for_other_users_received_requests(self):
        # user3 Ezma tries to see user2 identity variants for request their received
        # post login user3
        self.client.login(username=self.valid_username3, password=self.valid_password3)
        # get request identity variants for received requests
        response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
        # response should empty list, since there is no resources to show that user 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 0)

    # stranger cannot see users request identity variants for received requests
    def test_stranger_cannot_see_users_request_identity_variants_for_received_requests(self):
        # get request identity variants for received requests without logging in
        response = self.client.get(self.request_receive_request_identity_variant_list_url(1))
        # response should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # user can link request identity variants with profile identity variants
    def test_user_can_link_request_identity_variants_with_profile_identity_variants(self):
        # post login user2
        self.client.login(username=self.valid_username2, password=self.valid_password2)
        response = self.client.put(
            self.request_receive_request_identity_variant_detail_url(1, 1),
            {'profile_identity_variant_id': 1}
        )
        # response should be 200 OK
        print('test_user_can_link_request_identity_variants_with_profile_identity_variants : ')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        


    # user can not link other users request identity variants with profile identity variants

    # stranger cannot link users request identity variants with profile identity variants

    # user can not link request identity variants to requests that are pending or declined

    # when user changes variant from accepted to decilned, links should be wiped out 

  

  


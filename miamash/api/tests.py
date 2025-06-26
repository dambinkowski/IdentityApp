from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 
from django.contrib.auth import get_user_model
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
        # first log in
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

# user can see their identity varians 

# stranger cannot see users profile identity variants 

# user can update their profile identity variants 

# stranger cannot update users profile identity variants

# user can delete their profile identity variants

# stranger cannot delete users profile identity variants

# user can create their profile identity variants

# stranger cannot create users profile identity variants


## REQUESTS ## 
# Send 
# user can see their sent requests

# stranger cannot see users sent requests

# user can create new sent requests

# stranger cannot create sent requests for users

# user can update their sent requests

# stranger cannot update users sent requests

# user can delete their sent requests

# stranger cannot delete users sent requests

# user can see request identity variants for their sent requests

# stranger cannot see request identity variants for users sent requests

# user can create request identity variants for their sent requests

# stranger cannot create request identity variants for users sent requests







# Received 

# stranger cannot see users sent requests


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse 
from django.contrib.auth import get_user_model
User = get_user_model() # in case of at some point using custom user model

# import response 
## REGISTRATION AND LOGIN ## 
class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.username = 'Johny'
        self.password = 'test123123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

        self.valid_user_data = {
            'username': 'Johny',
            'password': 'test123123',
        }

        self.wrong_password_data = {
            'username': 'Johny',
            'password': 'wrongpassword',
        }   

        self.wrong_username_data = {
            'username': 'WrongUser',
            'password': 'test123123',
        }

        # Define URLs for registration, login, and logout

        self.register_url = reverse('rest_register')
        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        

    # user can log in  with good credentials
    def test_user_can_login_with_good_credentials(self):
        response = self.client.post(self.login_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)  


    # user cannot log in with bad credentials

    # user can log out

    # user can register with good credentials

    # user cannot register with bad credentials



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


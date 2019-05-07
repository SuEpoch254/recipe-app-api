from django.test import TestCase
from django.contrib.auth import get_user_model
# reverse is used to generate the API url
from django.urls import reverse
# rest framework test helper tools such as APIClient to make requests to the
# API and see what the response is.
from rest_framework.test import APIClient
# Let's use status to make the tests a bit easier to read and understand
from rest_framework import status

# At the beginning of the test we need a constant variable for the create user
# url.
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Helper function to create new user"""
    # We add a helper function to create some example users for the test.
    # So instead of creating users individually we just call the helper
    # function. ** params is a dynamic list of variable length of arguments
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""
    # Test class. The instructors preference is to call Public those tests that
    # are not authenticated. While Private are those tests that require auth.

    def setUp(self):
        # Let's create is once and we can reuse it for all of the tests
        self.client = APIClient()

    ##########################################################################
    #  USER TESTS
    ##########################################################################

    def test_create_valid_user_success(self):
        """Test creating using with a valid payload is successful"""
        # The payload is the object passed to the API in the request.
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'name',
        }
        # Post request to our url for creating users
        res = self.client.post(CREATE_USER_URL, payload)
        # Check the outcome is what we expect.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Check object is actually created.
        user = get_user_model().objects.get(**res.data)
        # Note: **res.data should look very similar to
        # Let's asset if password True
        self.assertTrue(user.check_password(payload['password']))
        # We don't want to password to be returned in the request
        # It's a potential security vulnerability. ****
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        # Let's create the user and what we will expect is a 400 bad request
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@londonappdev.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    ##########################################################################
    #  TOKEN TESTS
    ##########################################################################

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        # Post wrong pwd
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        # The data created by the previous test is deleted before starting
        # the next test. So the user with the credentials below won't exist
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_password(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_email(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
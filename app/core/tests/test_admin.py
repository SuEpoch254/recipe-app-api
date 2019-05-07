from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

# It is not recommended to test the dependencies of your project.
# Only test your code functionality. Django is expected to work.
# However we need to adjust admin to acommodate for the custom
# user model.


class AdminSiteTests(TestCase):
    """Test class to test amdin
    Note: Initially we will get the error
    <django.urls.exceptions.NoReverseMatch: Reverse for
    'core_user_changelist' not found> which means we don't have
    the admin.py."""

    def setUp(self):
        """Things that need to be done before every test"""
        # Create new test client
        self.client = Client()
        # For that we need a new admin user to test
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123'
        )
        # Make sure the user is logged into our client
        self.client.force_login(self.admin_user)
        # Finally we create a regular user that is not authenticated
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            name='Test User Full Name',
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        # Generates the url for the list user page.
        # These urls are defined in the django documentation
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """Test that the user edit page works"""
        # First generate url like /admin/core/user/<id>
        # args=[self.user.id] is how the id is customized
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


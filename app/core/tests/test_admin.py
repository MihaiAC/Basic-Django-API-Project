"""
Tests for the Django admin modifications.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        # Create Django test client - dummy browser
        self.client = Client()

        # Admin.
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )

        # Simulate the effect of a user logging into the site.
        # Skips authentication and verification steps.
        self.client.force_login(self.admin_user)

        # Non-admin user.
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

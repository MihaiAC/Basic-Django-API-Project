"""
Tests for app models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    # Do we have a separate dummy DB for testing?
    def test_create_user_with_email_successful(self):
        """Tests successful creation of user with email."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that emails are normalized for new users."""
        sample_emails = [
            ("test1@EXAMPLE.com", "test1@example.com"),
            ("Test2@Example.com", "Test2@example.com"),
            ("TEST3@EXAMPLE.com", "TEST3@example.com"),
        ]

        for original_email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(
                email=original_email, password="sample123"
            )
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that create user raises exception with empty email."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "pass123")

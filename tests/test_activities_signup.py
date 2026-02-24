"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup).

This module tests signing up a student for an extracurricular activity.
"""

import pytest


class TestActivitySignup:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid_activity_and_email(self, client):
        """
        Test successful signup for an activity.
        
        Arrange: Prepare a new email not yet signed up for an activity
        Act: POST GET /activities/Chess Club/signup with email query parameter
        Assert: Response status is 200 and returns success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_email_returns_error(self, client):
        """
        Test that signing up with an email already enrolled returns 400 error.
        
        Arrange: Sign up with an email first
        Act: Try to sign up the same email for the same activity again
        Assert: Response status is 400 and error message indicates duplicate signup
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up for Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 400
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test that signing up for a non-existent activity returns 404 error.
        
        Arrange: Prepare a non-existent activity name and valid email
        Act: POST to signup endpoint with invalid activity name
        Assert: Response status is 404 and error message indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_multiple_activities_different_emails(self, client):
        """
        Test that a new email can sign up for multiple different activities.
        
        Arrange: Prepare a new email and two different activities
        Act: Sign up for Chess Club, then sign up for Programming Class
        Assert: Both signups succeed with 200 status
        """
        # Arrange
        email = "multiplesignup@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # Act - First signup
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )

        # Act - Second signup
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

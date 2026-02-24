"""
Tests for the remove from activity endpoint (DELETE /activities/{activity_name}/signup).

This module tests removing a student from an extracurricular activity.
"""

import pytest


class TestActivityRemove:
    """Test suite for the DELETE /activities/{activity_name}/signup endpoint."""

    def test_remove_valid_signup(self, client):
        """
        Test successfully removing a student from an activity they're signed up for.
        
        Arrange: Sign up a new email for an activity first
        Act: DELETE the signup for that email and activity
        Assert: Response status is 200 and returns success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "removetest@mergington.edu"
        
        # First, sign up
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_not_signed_up_returns_error(self, client):
        """
        Test that removing a student not signed up returns 400 error.
        
        Arrange: Use an email that never signed up for the activity
        Act: DELETE the signup endpoint with email not enrolled
        Assert: Response status is 400 and error indicates student not signed up
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notsignedup@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 400
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_remove_from_nonexistent_activity_returns_404(self, client):
        """
        Test that removing from a non-existent activity returns 404 error.
        
        Arrange: Prepare a non-existent activity name and any email
        Act: DELETE the signup endpoint with invalid activity name
        Assert: Response status is 404 and error indicates activity not found
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_then_remove_then_remove_again(self, client):
        """
        Test that removing twice (signup -> remove -> remove again) fails on second removal.
        
        Arrange: Sign up an email for an activity
        Act: Remove the email (success), then try to remove again (should fail)
        Assert: First removal is 200, second removal is 400
        """
        # Arrange
        activity_name = "Programming Class"
        email = "doubleremove@mergington.edu"
        
        # Sign up first
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - First removal
        response1 = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act - Second removal
        response2 = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400

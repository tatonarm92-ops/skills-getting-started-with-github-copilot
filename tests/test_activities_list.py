"""
Tests for the activities list endpoint (GET /activities).

This module tests retrieving all available extracurricular activities.
"""

import pytest


class TestActivitiesList:
    """Test suite for the GET /activities endpoint."""

    def test_get_all_activities_success(self, client):
        """
        Test that GET /activities returns all activities with correct structure.
        
        Arrange: TestClient is ready, expect 9 activities in the system
        Act: Make GET request to /activities
        Assert: Response status is 200 and contains all expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Debate Team",
            "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert len(data) == 9
        for activity_name in expected_activities:
            assert activity_name in data
            activity = data[activity_name]
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity
            assert isinstance(activity["participants"], list)

    def test_get_all_activities_response_structure(self, client):
        """
        Test that each activity in the response has the correct data structure.
        
        Arrange: TestClient is ready
        Act: Make GET request to /activities
        Assert: Each activity has required fields with correct types
        """
        # Arrange
        # Client is provided by fixture

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in data.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_details, dict)
            assert isinstance(activity_details["description"], str)
            assert isinstance(activity_details["schedule"], str)
            assert isinstance(activity_details["max_participants"], int)
            assert isinstance(activity_details["participants"], list)
            assert activity_details["max_participants"] > 0

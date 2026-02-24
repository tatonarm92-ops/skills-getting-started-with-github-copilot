"""
Tests for the root endpoint (GET /).

This module tests the root endpoint that redirects to the static index.html file.
"""

import pytest


class TestRoot:
    """Test suite for the root endpoint."""

    def test_root_redirect(self, client):
        """
        Test that GET / redirects to /static/index.html.
        
        Arrange: TestClient is ready
        Act: Make GET request to /
        Assert: Response status is 307 Temporary Redirect and location header is set
        """
        # Arrange
        # Client is provided by fixture

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers.get("location", "")

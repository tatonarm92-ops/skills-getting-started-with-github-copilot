"""
Pytest configuration and shared fixtures for the test suite.

This module provides common fixtures used across all test modules,
including the FastAPI TestClient for testing endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for testing the FastAPI application.
    
    Yields:
        TestClient: A test client for making requests to the app.
    """
    return TestClient(app)

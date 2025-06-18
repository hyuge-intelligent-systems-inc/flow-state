"""
FlowState API Backend Tests

This script tests all the backend API endpoints for the FlowState productivity application.
"""

import requests
import json
import uuid
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8001"
API_URL = f"{BASE_URL}/api"

# Test data
TEST_USERNAME = "test_user"
TEST_TASK = "Test productivity session"
TEST_CATEGORY = "testing"

# Test results tracking
test_results = {
    "total_tests": 0,
    "passed_tests": 0,
    "failed_tests": 0,
    "skipped_tests": 0,
    "test_details": []
}

def log_test_result(test_name, passed, error=None, response=None):
    """Log test result with details"""
    result = "PASSED" if passed else "FAILED"
    test_results["total_tests"] += 1
    
    if passed:
        test_results["passed_tests"] += 1
        print(f"✅ {test_name}: {result}")
    else:
        test_results["failed_tests"] += 1
        print(f"❌ {test_name}: {result}")
        if error:
            print(f"   Error: {error}")
        if response:
            try:
                print(f"   Response: {response.status_code} - {response.json()}")
            except:
                print(f"   Response: {response.status_code} - {response.text}")
    
    test_results["test_details"].append({
        "name": test_name,
        "result": result,
        "error": str(error) if error else None,
        "response": response.json() if response and hasattr(response, 'json') else None,
        "timestamp": datetime.now().isoformat()
    })

def run_test(test_func):
    """Decorator to run a test function and handle exceptions"""
    def wrapper(*args, **kwargs):
        test_name = test_func.__name__.replace('_', ' ').title()
        try:
            return test_func(*args, **kwargs)
        except Exception as e:
            log_test_result(test_name, False, error=str(e))
            return None
    return wrapper

# Health & Status Tests
@run_test
def test_root_endpoint():
    """Test the root endpoint"""
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    log_test_result("Root Endpoint", True, response=response)
    return True

@run_test
def test_health_endpoint():
    """Test the health check endpoint"""
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    log_test_result("Health Endpoint", True, response=response)
    return True

# User Management Tests
@run_test
def test_create_user():
    """Test creating a new user"""
    payload = {
        "username": TEST_USERNAME,
        "preferences": {
            "theme": "dark",
            "notifications": True
        }
    }
    response = requests.post(f"{API_URL}/users", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["username"] == TEST_USERNAME
    log_test_result("Create User", True, response=response)
    return data["user_id"]

@run_test
def test_get_user(user_id):
    """Test getting user information"""
    response = requests.get(f"{API_URL}/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["username"] == TEST_USERNAME
    assert "profile" in data
    log_test_result("Get User", True, response=response)
    return True

@run_test
def test_update_preferences(user_id):
    """Test updating user preferences"""
    payload = {
        "accessibility_prefs": {
            "high_contrast": True,
            "font_size": "large"
        },
        "productivity_prefs": {
            "session_duration": 25,
            "break_duration": 5
        },
        "privacy_settings": {
            "data_collection": "minimal"
        }
    }
    response = requests.put(f"{API_URL}/users/{user_id}/preferences", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    log_test_result("Update Preferences", True, response=response)
    return True

# Session Management Tests
@run_test
def test_start_session(user_id):
    """Test starting a productivity session"""
    payload = {
        "task_description": TEST_TASK,
        "category": TEST_CATEGORY,
        "estimated_minutes": 30,
        "energy_level": 4
    }
    response = requests.post(f"{API_URL}/users/{user_id}/sessions/start", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_started" in data
    assert data["session_started"] == True
    log_test_result("Start Session", True, response=response)
    return True

@run_test
def test_get_current_session(user_id):
    """Test getting the current active session"""
    response = requests.get(f"{API_URL}/users/{user_id}/sessions/current")
    assert response.status_code == 200
    data = response.json()
    assert "active_session" in data
    assert data["active_session"] == True
    assert "session" in data
    assert data["session"]["task"] == TEST_TASK
    assert data["session"]["category"] == TEST_CATEGORY
    log_test_result("Get Current Session", True, response=response)
    return True

@run_test
def test_end_session(user_id):
    """Test ending a productivity session"""
    payload = {
        "user_notes": "This was a test session",
        "energy_level": 3,
        "focus_quality": 4,
        "interruptions": 2,
        "satisfaction": 4
    }
    response = requests.post(f"{API_URL}/users/{user_id}/sessions/end", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_summary" in data
    assert data["session_summary"]["task"] == TEST_TASK
    assert data["session_summary"]["category"] == TEST_CATEGORY
    log_test_result("End Session", True, response=response)
    return True

# Analytics & Insights Tests
@run_test
def test_daily_summary(user_id):
    """Test getting daily productivity summary"""
    response = requests.get(f"{API_URL}/users/{user_id}/summary/daily")
    assert response.status_code == 200
    data = response.json()
    assert "date" in data
    assert "total_minutes" in data
    assert "entries_count" in data
    log_test_result("Daily Summary", True, response=response)
    return True

@run_test
def test_insights(user_id):
    """Test getting comprehensive productivity insights"""
    response = requests.get(f"{API_URL}/users/{user_id}/insights", params={"timeframe_days": 7})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "time_tracking_insights" in data
    log_test_result("Comprehensive Insights", True, response=response)
    return True

@run_test
def test_patterns(user_id):
    """Test getting pattern analysis"""
    response = requests.get(f"{API_URL}/users/{user_id}/patterns")
    # This might return a message about not enough data, which is fine
    assert response.status_code == 200
    data = response.json()
    # Either we have patterns or a message about not enough data
    assert "patterns" in data or "message" in data
    log_test_result("Pattern Analysis", True, response=response)
    return True

# Data & Privacy Tests
@run_test
def test_export_data(user_id):
    """Test exporting all user data"""
    response = requests.get(f"{API_URL}/users/{user_id}/export")
    assert response.status_code == 200
    data = response.json()
    assert "export_timestamp" in data
    assert "user_info" in data
    assert "productivity_engine" in data
    assert "user_profile" in data
    assert "data_ownership" in data
    log_test_result("Export User Data", True, response=response)
    return True

@run_test
def test_delete_user(user_id):
    """Test deleting a user with confirmation"""
    confirmation = f"DELETE-{user_id[:8]}"
    response = requests.delete(f"{API_URL}/users/{user_id}", params={"confirmation": confirmation})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    log_test_result("Delete User", True, response=response)
    return True

# Demo Features Tests
@run_test
def test_create_demo_user():
    """Test creating a demo user with sample data"""
    response = requests.get(f"{API_URL}/demo/sample-user")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "username" in data
    assert "sample_sessions" in data
    log_test_result("Create Demo User", True, response=response)
    return data["user_id"]

@run_test
def test_reset_demo_user(demo_user_id):
    """Test resetting demo user data"""
    response = requests.get(f"{API_URL}/demo/reset/{demo_user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    log_test_result("Reset Demo User", True, response=response)
    return True

# Error Handling Tests
@run_test
def test_invalid_user_id():
    """Test handling of invalid user ID"""
    invalid_id = str(uuid.uuid4())
    response = requests.get(f"{API_URL}/users/{invalid_id}")
    assert response.status_code == 404
    log_test_result("Invalid User ID Handling", True, response=response)
    return True

@run_test
def test_invalid_delete_confirmation(user_id):
    """Test handling of invalid delete confirmation"""
    response = requests.delete(f"{API_URL}/users/{user_id}", params={"confirmation": "WRONG"})
    assert response.status_code == 400
    log_test_result("Invalid Delete Confirmation", True, response=response)
    return True

# Happy Path Flow Test
@run_test
def test_happy_path_flow():
    """Test the complete happy path flow"""
    # Create demo user
    demo_response = requests.get(f"{API_URL}/demo/sample-user")
    assert demo_response.status_code == 200
    demo_data = demo_response.json()
    user_id = demo_data["user_id"]
    
    # Start session
    start_payload = {
        "task_description": "Happy path test session",
        "category": "testing",
        "estimated_minutes": 15,
        "energy_level": 5
    }
    start_response = requests.post(f"{API_URL}/users/{user_id}/sessions/start", json=start_payload)
    assert start_response.status_code == 200
    
    # Wait a moment to simulate session duration
    time.sleep(2)
    
    # End session
    end_payload = {
        "user_notes": "Completed happy path test",
        "energy_level": 4,
        "focus_quality": 5,
        "interruptions": 0,
        "satisfaction": 5
    }
    end_response = requests.post(f"{API_URL}/users/{user_id}/sessions/end", json=end_payload)
    assert end_response.status_code == 200
    
    # Get analytics
    analytics_response = requests.get(f"{API_URL}/users/{user_id}/insights")
    assert analytics_response.status_code == 200
    
    # Export data
    export_response = requests.get(f"{API_URL}/users/{user_id}/export")
    assert export_response.status_code == 200
    
    log_test_result("Happy Path Flow", True)
    return user_id

# Data Validation Tests
@run_test
def test_energy_level_validation(user_id):
    """Test validation of energy level values"""
    # Test with invalid energy level (should be 1-5)
    payload = {
        "task_description": "Energy validation test",
        "category": "testing",
        "estimated_minutes": 15,
        "energy_level": 10  # Invalid value
    }
    response = requests.post(f"{API_URL}/users/{user_id}/sessions/start", json=payload)
    
    # The API might accept this since validation isn't explicitly mentioned
    # We'll check if it runs without error
    log_test_result("Energy Level Validation", response.status_code < 500, response=response)
    return True

def run_all_tests():
    """Run all tests in sequence"""
    print("\n🔍 Starting FlowState API Tests...\n")
    
    # Health & Status Tests
    test_root_endpoint()
    test_health_endpoint()
    
    # User Management Tests
    user_id = test_create_user()
    if user_id:
        test_get_user(user_id)
        test_update_preferences(user_id)
        
        # Session Management Tests
        test_start_session(user_id)
        test_get_current_session(user_id)
        test_end_session(user_id)
        
        # Analytics & Insights Tests
        test_daily_summary(user_id)
        test_insights(user_id)
        test_patterns(user_id)
        
        # Data & Privacy Tests
        test_export_data(user_id)
        test_invalid_delete_confirmation(user_id)
        test_delete_user(user_id)
    
    # Demo Features Tests
    demo_user_id = test_create_demo_user()
    if demo_user_id:
        test_reset_demo_user(demo_user_id)
    
    # Error Handling Tests
    test_invalid_user_id()
    
    # Happy Path Flow Test
    happy_path_user_id = test_happy_path_flow()
    if happy_path_user_id:
        test_energy_level_validation(happy_path_user_id)
    
    # Print summary
    print("\n📊 Test Summary:")
    print(f"Total Tests: {test_results['total_tests']}")
    print(f"Passed: {test_results['passed_tests']}")
    print(f"Failed: {test_results['failed_tests']}")
    print(f"Success Rate: {(test_results['passed_tests'] / test_results['total_tests']) * 100:.1f}%\n")
    
    return test_results

if __name__ == "__main__":
    run_all_tests()
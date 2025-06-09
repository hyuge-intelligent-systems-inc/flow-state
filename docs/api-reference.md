
FlowState API Reference
Overview
The FlowState API provides programmatic access to time tracking, productivity analytics, and AI-powered insights. The API follows RESTful principles and returns JSON responses.
Base URL: https://api.flowstate.app/v1
Authentication: Bearer token (JWT)
Rate Limiting: 1000 requests per hour per API key
Authentication
Get API Token
httpPOST /auth/token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
Response:
json{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200..."
}
Using Authentication
Include the Bearer token in the Authorization header:
httpAuthorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Core Resources
Time Tracking
Start Time Entry
httpPOST /time-entries
Content-Type: application/json
Authorization: Bearer {token}

{
  "description": "Working on FlowState API documentation",
  "project_id": "proj_abc123",
  "tags": ["documentation", "api"],
  "billable": true
}
Response:
json{
  "id": "entry_xyz789",
  "description": "Working on FlowState API documentation",
  "project_id": "proj_abc123",
  "tags": ["documentation", "api"],
  "billable": true,
  "start_time": "2025-01-20T14:30:00Z",
  "end_time": null,
  "duration": null,
  "status": "running",
  "created_at": "2025-01-20T14:30:00Z",
  "updated_at": "2025-01-20T14:30:00Z"
}
Stop Time Entry
httpPATCH /time-entries/{entry_id}/stop
Authorization: Bearer {token}
Response:
json{
  "id": "entry_xyz789",
  "description": "Working on FlowState API documentation",
  "project_id": "proj_abc123",
  "tags": ["documentation", "api"],
  "billable": true,
  "start_time": "2025-01-20T14:30:00Z",
  "end_time": "2025-01-20T16:45:00Z",
  "duration": 8100,
  "status": "completed",
  "created_at": "2025-01-20T14:30:00Z",
  "updated_at": "2025-01-20T16:45:00Z"
}
Get Time Entries
httpGET /time-entries?start_date=2025-01-20&end_date=2025-01-21&project_id=proj_abc123
Authorization: Bearer {token}
Query Parameters:

start_date (string): Filter entries from this date (ISO 8601)
end_date (string): Filter entries to this date (ISO 8601)
project_id (string): Filter by project ID
billable (boolean): Filter by billable status
page (integer): Page number for pagination (default: 1)
per_page (integer): Items per page (default: 50, max: 200)

Response:
json{
  "data": [
    {
      "id": "entry_xyz789",
      "description": "Working on FlowState API documentation",
      "project_id": "proj_abc123",
      "tags": ["documentation", "api"],
      "billable": true,
      "start_time": "2025-01-20T14:30:00Z",
      "end_time": "2025-01-20T16:45:00Z",
      "duration": 8100,
      "status": "completed",
      "created_at": "2025-01-20T14:30:00Z",
      "updated_at": "2025-01-20T16:45:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 50,
    "total": 1,
    "total_pages": 1
  }
}
Projects
Create Project
httpPOST /projects
Content-Type: application/json
Authorization: Bearer {token}

{
  "name": "FlowState Development",
  "description": "Main development project for FlowState app",
  "color": "#3B82F6",
  "billable_rate": 150.00,
  "currency": "USD",
  "client_id": "client_def456"
}
Get Projects
httpGET /projects
Authorization: Bearer {token}
Response:
json{
  "data": [
    {
      "id": "proj_abc123",
      "name": "FlowState Development",
      "description": "Main development project for FlowState app",
      "color": "#3B82F6",
      "billable_rate": 150.00,
      "currency": "USD",
      "client_id": "client_def456",
      "archived": false,
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    }
  ]
}
Analytics
Get Productivity Summary
httpGET /analytics/summary?period=week&start_date=2025-01-13
Authorization: Bearer {token}
Query Parameters:

period (string): day, week, month, year
start_date (string): Start date for the period (ISO 8601)
project_id (string): Filter by specific project
complexity_level (string): simple, standard, advanced (determines detail level)

Response:
json{
  "period": "week",
  "start_date": "2025-01-13",
  "end_date": "2025-01-19",
  "total_duration": 28800,
  "billable_duration": 21600,
  "productivity_score": 0.78,
  "focus_sessions": 12,
  "average_session_length": 2400,
  "top_projects": [
    {
      "project_id": "proj_abc123",
      "name": "FlowState Development",
      "duration": 18000,
      "percentage": 62.5
    }
  ],
  "daily_breakdown": [
    {
      "date": "2025-01-13",
      "duration": 7200,
      "productivity_score": 0.82,
      "focus_sessions": 3
    }
  ]
}
Get Flow State Analysis
httpGET /analytics/flow-states?start_date=2025-01-13&end_date=2025-01-19
Authorization: Bearer {token}
Response:
json{
  "flow_sessions": [
    {
      "id": "flow_session_abc",
      "start_time": "2025-01-18T09:15:00Z",
      "end_time": "2025-01-18T11:30:00Z",
      "duration": 8100,
      "intensity_score": 0.89,
      "interruptions": 1,
      "project_id": "proj_abc123",
      "triggers": ["morning_routine", "quiet_environment"],
      "quality_rating": 4.5
    }
  ],
  "optimal_times": [
    {
      "day_of_week": "tuesday",
      "time_range": "09:00-11:30",
      "flow_probability": 0.78
    }
  ],
  "environmental_factors": {
    "best_locations": ["home_office", "coffee_shop_quiet"],
    "optimal_duration": "90-120_minutes",
    "common_disruptors": ["notifications", "meetings"]
  }
}
AI Insights
Get Procrastination Analysis
httpGET /ai/procrastination-analysis?days=30
Authorization: Bearer {token}
Response:
json{
  "procrastination_patterns": [
    {
      "trigger": "complex_documentation_tasks",
      "frequency": 0.65,
      "average_delay": 3600,
      "suggested_interventions": [
        "break_into_smaller_chunks",
        "use_pomodoro_technique",
        "pair_with_preferred_tasks"
      ]
    }
  ],
  "root_causes": [
    {
      "cause": "task_ambiguity",
      "confidence": 0.78,
      "evidence": ["incomplete_task_descriptions", "frequent_clarification_requests"]
    }
  ],
  "recommendations": [
    {
      "type": "behavioral",
      "suggestion": "Start complex tasks with 2-minute planning session",
      "expected_impact": "medium",
      "implementation_difficulty": "low"
    }
  ]
}
Get Habit Suggestions
httpGET /ai/habit-suggestions
Authorization: Bearer {token}
Response:
json{
  "suggested_habits": [
    {
      "id": "habit_morning_review",
      "name": "Morning Priority Review",
      "description": "Spend 5 minutes reviewing top 3 priorities",
      "frequency": "daily",
      "optimal_time": "09:00",
      "difficulty": "low",
      "evidence_basis": "Users with morning planning show 23% higher task completion",
      "personalization_factors": ["works_best_in_morning", "responds_to_structure"]
    }
  ],
  "habit_progress": [
    {
      "habit_id": "habit_pomodoro",
      "name": "Pomodoro Sessions",
      "current_streak": 5,
      "success_rate": 0.72,
      "trend": "improving"
    }
  ]
}
Privacy & Data Control
Get Privacy Settings
httpGET /privacy/settings
Authorization: Bearer {token}
Response:
json{
  "data_processing": {
    "local_only": true,
    "cloud_analytics": false,
    "ai_insights": true,
    "third_party_sharing": false
  },
  "retention_policy": {
    "raw_data_days": 90,
    "aggregated_data_years": 2,
    "ai_model_data": "anonymized_indefinite"
  },
  "export_options": {
    "formats": ["json", "csv", "xml"],
    "last_export": "2025-01-10T15:30:00Z"
  }
}
Update Privacy Settings
httpPATCH /privacy/settings
Content-Type: application/json
Authorization: Bearer {token}

{
  "data_processing": {
    "cloud_analytics": true,
    "ai_insights": true
  }
}
Export Data
httpPOST /privacy/export
Content-Type: application/json
Authorization: Bearer {token}

{
  "format": "json",
  "include_analytics": true,
  "date_range": {
    "start": "2024-01-01",
    "end": "2025-01-20"
  }
}
Response:
json{
  "export_id": "export_xyz123",
  "status": "processing",
  "estimated_completion": "2025-01-20T15:45:00Z",
  "download_url": null
}
Team & Enterprise Features
Team Management
Get Team Members
httpGET /teams/{team_id}/members
Authorization: Bearer {token}
Get Team Analytics
httpGET /teams/{team_id}/analytics?period=week
Authorization: Bearer {token}
Response:
json{
  "team_productivity": {
    "total_hours": 320,
    "collaboration_index": 0.72,
    "workload_balance": 0.85
  },
  "member_summary": [
    {
      "user_id": "user_123",
      "name": "Alice Johnson",
      "hours": 40,
      "productivity_score": 0.83,
      "focus_time_percentage": 0.65
    }
  ],
  "collaboration_patterns": {
    "peak_overlap_hours": ["10:00-12:00", "14:00-16:00"],
    "communication_efficiency": 0.78,
    "meeting_overhead": 0.23
  }
}
Webhooks
Configure Webhooks
httpPOST /webhooks
Content-Type: application/json
Authorization: Bearer {token}

{
  "url": "https://your-app.com/flowstate-webhook",
  "events": ["time_entry.started", "time_entry.stopped", "daily_summary.generated"],
  "secret": "your_webhook_secret"
}
Webhook Events
Time Entry Started
json{
  "event": "time_entry.started",
  "timestamp": "2025-01-20T14:30:00Z",
  "data": {
    "time_entry": {
      "id": "entry_xyz789",
      "description": "Working on API documentation",
      "project_id": "proj_abc123"
    }
  }
}
Daily Summary Generated
json{
  "event": "daily_summary.generated",
  "timestamp": "2025-01-20T23:00:00Z",
  "data": {
    "date": "2025-01-20",
    "total_duration": 28800,
    "productivity_score": 0.78,
    "focus_sessions": 4
  }
}
Error Handling
Error Response Format
json{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided data is invalid",
    "details": [
      {
        "field": "start_time",
        "message": "Start time cannot be in the future"
      }
    ],
    "request_id": "req_abc123"
  }
}
Common Error Codes

AUTHENTICATION_REQUIRED (401): Missing or invalid authentication
AUTHORIZATION_FAILED (403): Insufficient permissions
VALIDATION_ERROR (400): Invalid request data
RESOURCE_NOT_FOUND (404): Requested resource doesn't exist
RATE_LIMIT_EXCEEDED (429): Too many requests
INTERNAL_ERROR (500): Server error

Rate Limiting

Standard Plan: 1,000 requests/hour
Pro Plan: 5,000 requests/hour
Enterprise Plan: 50,000 requests/hour

Rate limit headers included in responses:
httpX-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642694400
SDKs and Libraries
Official SDKs

JavaScript/Node.js: npm install @flowstate/sdk
Python: pip install flowstate-sdk
Ruby: gem install flowstate-sdk
Go: go get github.com/flowstate/go-sdk

Example Usage (JavaScript)
javascriptimport FlowState from '@flowstate/sdk';

const client = new FlowState({
  apiKey: 'your_api_key',
  baseURL: 'https://api.flowstate.app/v1'
});

// Start time tracking
const entry = await client.timeEntries.start({
  description: 'Working on new feature',
  projectId: 'proj_abc123',
  tags: ['development', 'feature']
});

// Get analytics
const summary = await client.analytics.getSummary({
  period: 'week',
  startDate: '2025-01-13'
});
Changelog
v1.2.0 (2025-01-20)

Added flow state analysis endpoints
Enhanced privacy controls
Improved team analytics

v1.1.0 (2025-01-15)

Added AI insights endpoints
Webhook support
Team management features

v1.0.0 (2025-01-01)

Initial API release
Core time tracking functionality
Basic analytics and reporting

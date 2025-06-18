"""
FlowState FastAPI Backend Server
Exposes the FlowState productivity system through REST API
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add the src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import uuid

# Import enhanced FlowState modules
try:
    from enhanced_time_tracker import (
        MultiSessionTimeTracker, SessionTag, TimeEntry, 
        ConfidenceLevel, SessionStatus
    )
    
    # Mock ProductivityEngine for the enhanced system
    class ProductivityEngine:
        def __init__(self, user_id: str = "default_user"):
            self.user_id = user_id
            self.time_tracker = MultiSessionTimeTracker(user_id)
            
        def start_productivity_session(self, main_tag: str, sub_tag: str = None, 
                                     task_description: str = "", estimated_minutes: int = None, 
                                     context: Dict[str, Any] = None) -> Dict[str, Any]:
            entry = self.time_tracker.start_session(
                main_tag=main_tag,
                sub_tag=sub_tag,
                task_description=task_description,
                estimated_minutes=estimated_minutes
            )
            
            return {
                "session_started": True,
                "session_id": entry.session_id,
                "tag": str(entry.tag),
                "guidance": {"suggestions": [], "insights": [], "warnings": [], "confidence_notes": []},
                "ui_config": {},
                "user_control": {
                    "modify_estimate": "Available anytime during session",
                    "change_tag": "Available anytime",
                    "disable_guidance": "All suggestions can be ignored",
                    "stop_early": "No minimum session length required"
                },
                "system_status": "optimal"
            }
        
        def end_productivity_session(self, session_id: str, user_notes: str = "", 
                                   energy_level: int = 3, focus_quality: int = 3, 
                                   interruptions: int = 0, satisfaction: int = 3) -> Dict[str, Any]:
            completed_entry = self.time_tracker.end_session(
                session_id=session_id,
                user_notes=user_notes,
                energy_level=energy_level,
                focus_quality=focus_quality,
                interruptions=interruptions
            )
            
            if not completed_entry:
                return {"error": "Session not found or already completed"}
            
            return {
                "session_summary": {
                    "session_id": completed_entry.session_id,
                    "tag": str(completed_entry.tag),
                    "main_tag": completed_entry.tag.main_tag,
                    "sub_tag": completed_entry.tag.sub_tag,
                    "task": completed_entry.task_description,
                    "duration_minutes": completed_entry.duration_minutes(),
                    "focus_quality": completed_entry.focus_quality,
                    "energy_level": completed_entry.energy_level,
                    "interruptions": completed_entry.interruptions,
                    "satisfaction": satisfaction,
                    "confidence": completed_entry.confidence.value
                },
                "insights": [],
                "areas_for_reflection": [
                    f"How did the #{completed_entry.tag.main_tag} session align with your goals?",
                    "What would you change about this work session?"
                ],
                "positive_observations": [
                    f"Completed {completed_entry.duration_minutes()} minutes of focused work",
                    f"Self-assessed focus quality: {completed_entry.focus_quality}/5"
                ]
            }
        
        def get_active_sessions(self) -> Dict[str, Any]:
            return {
                "active_sessions": self.time_tracker.get_active_sessions(),
                "count": len(self.time_tracker.active_sessions)
            }
        
        def get_daily_productivity_summary(self, date: Optional[datetime] = None) -> Dict[str, Any]:
            return self.time_tracker.get_daily_summary(date)
        
        def get_comprehensive_insights(self, timeframe_days: int = 30) -> Dict[str, Any]:
            tag_analytics = self.time_tracker.get_tag_analytics(timeframe_days)
            estimation_accuracy = self.time_tracker.get_estimation_accuracy()
            
            return {
                "summary": {
                    "timeframe_days": timeframe_days, 
                    "data_sources": ["multi_session_tracking"], 
                    "confidence_levels": {},
                    "user_interpretation_guidance": "Your tags and patterns reflect your unique work style"
                },
                "time_tracking_insights": {
                    "active_days": timeframe_days,
                    "total_tracked_time": tag_analytics.get("total_time_minutes", 0),
                    "average_daily_time": tag_analytics.get("total_time_minutes", 0) / max(timeframe_days, 1),
                    "total_sessions": tag_analytics.get("total_entries", 0)
                },
                "tag_insights": tag_analytics,
                "estimation_accuracy": estimation_accuracy,
                "ai_insights": [
                    {
                        "description": insight,
                        "confidence": "moderate",
                        "limitations": "Based on your self-reported data and tagging patterns"
                    } for insight in tag_analytics.get("insights", [])
                ],
                "integration_insights": [
                    {
                        "type": "user_agency",
                        "description": f"You're using {len(tag_analytics.get('user_tags', []))} different tags to categorize your work",
                        "guidance": "This tagging system reflects your understanding of your work patterns"
                    }
                ],
                "next_steps": [
                    {
                        "title": "Refine Your Tags",
                        "description": "Consider if your current tags accurately reflect your work categories",
                        "rationale": "User-defined categories are more meaningful than preset ones",
                        "action": "Review and adjust tags that don't feel right to you"
                    }
                ],
                "limitations": [
                    "Analysis is based entirely on your self-reported data",
                    "Tag effectiveness depends on consistent usage",
                    "Individual context and external factors are not captured"
                ]
            }
        
        def get_patterns(self) -> Dict[str, Any]:
            """Get pattern analysis with honest limitations"""
            tag_analytics = self.time_tracker.get_tag_analytics()
            
            if tag_analytics.get("total_entries", 0) < 5:
                return {
                    "message": "Not enough data for pattern analysis",
                    "required_sessions": 5,
                    "current_sessions": tag_analytics.get("total_entries", 0),
                    "user_guidance": "Patterns will become visible as you track more sessions"
                }
            
            patterns = {}
            main_tag_analysis = tag_analytics.get("main_tag_analysis", {})
            
            for main_tag, data in main_tag_analysis.items():
                if data["session_count"] >= 3:  # Minimum for pattern recognition
                    patterns[f"{main_tag}_productivity"] = {
                        "description": f"During #{main_tag} activities, you average {data['avg_focus']:.1f}/5 focus and {data['avg_energy']:.1f}/5 energy",
                        "confidence": "moderate",
                        "sample_size": data["session_count"],
                        "limitations": "Pattern based on self-reported metrics during tagged sessions",
                        "user_interpretation_needed": True,
                        "supporting_data": {
                            "total_minutes": data["total_minutes"],
                            "avg_duration": data.get("avg_duration", 0),
                            "sub_tags_used": list(data.get("sub_tags", {}).keys())
                        }
                    }
            
            return {"patterns": patterns}
        
        def export_complete_user_data(self) -> Dict[str, Any]:
            return self.time_tracker.export_data()
    
    # Mock UserProfile for compatibility
    class UserProfile:
        def __init__(self, user_id: Optional[str] = None):
            self.user_id = user_id or str(uuid.uuid4())
            self.created_at = datetime.now()
            self.days_active = 0
            self.total_sessions = 0
            self.ui_complexity_level = 1
            self.current_productivity_mode = "maintenance"
        
        def track_usage(self, session_type: str = "general"):
            self.total_sessions += 1
        
        def update_accessibility_preferences(self, **kwargs):
            pass
        
        def update_productivity_preferences(self, **kwargs):
            pass
        
        def update_privacy_settings(self, **kwargs):
            pass
        
        def export_all_data(self) -> Dict[str, Any]:
            return {
                "user_profile": {
                    "user_id": self.user_id,
                    "created_at": self.created_at.isoformat(),
                    "days_active": self.days_active,
                    "total_sessions": self.total_sessions
                }
            }

except ImportError:
    from core.productivity_engine import ProductivityEngine, ProductivityMode
    from core.time_tracker import TimeTracker, ConfidenceLevel, TaskComplexity
    from core.user_profile import UserProfile, ProductivityMode as ProfileMode, PrivacyLevel
    from psychology.self_discovery import SelfDiscoveryGuide, ReflectionCategory, SupportLevel
except ImportError:
    # For demo purposes, create mock classes
    from enum import Enum
    from dataclasses import dataclass
    from typing import Dict, List, Optional, Any
    from datetime import datetime
    import uuid
    
    class ConfidenceLevel(Enum):
        HIGH = "high"
        MODERATE = "moderate" 
        LOW = "low"
        UNCERTAIN = "uncertain"
    
    class ProductivityMode(Enum):
        SURVIVAL = "survival"
        MAINTENANCE = "maintenance"
        GROWTH = "growth"
        MASTERY = "mastery"
    
    class TaskComplexity(Enum):
        SIMPLE = "simple"
        MODERATE = "moderate"
        COMPLEX = "complex"
        UNKNOWN = "unknown"
    
    class ReflectionCategory(Enum):
        PRODUCTIVITY_PATTERNS = "productivity_patterns"
        ENERGY_AWARENESS = "energy_awareness"
        
    class SupportLevel(Enum):
        MINIMAL = "minimal"
        GUIDED = "guided"
        COMPREHENSIVE = "comprehensive"
    
    @dataclass
    class TimeEntry:
        start_time: datetime
        end_time: Optional[datetime] = None
        task_description: str = ""
        category: str = "uncategorized"
        confidence: ConfidenceLevel = ConfidenceLevel.MODERATE
        user_notes: str = ""
        interruptions: int = 0
        energy_level: int = 3
        focus_quality: int = 3
        
        def duration_minutes(self) -> Optional[int]:
            if not self.end_time:
                return None
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        
        def is_complete(self) -> bool:
            return self.end_time is not None
    
    class TimeTracker:
        def __init__(self, user_id: str = "default_user"):
            self.user_id = user_id
            self.entries: List[TimeEntry] = []
            self.current_entry: Optional[TimeEntry] = None
            
        def start_timer(self, task_description: str = "", category: str = "work", estimated_minutes: Optional[int] = None) -> TimeEntry:
            if self.current_entry and not self.current_entry.is_complete():
                self.stop_timer()
            
            self.current_entry = TimeEntry(
                start_time=datetime.now(),
                task_description=task_description,
                category=category,
                confidence=ConfidenceLevel.MODERATE
            )
            self.entries.append(self.current_entry)
            return self.current_entry
        
        def stop_timer(self, user_notes: str = "", energy_level: int = 3, focus_quality: int = 3, interruptions: int = 0) -> Optional[TimeEntry]:
            if not self.current_entry or self.current_entry.is_complete():
                return None
            
            self.current_entry.end_time = datetime.now()
            self.current_entry.user_notes = user_notes
            self.current_entry.energy_level = energy_level
            self.current_entry.focus_quality = focus_quality
            self.current_entry.interruptions = interruptions
            
            completed_entry = self.current_entry
            self.current_entry = None
            return completed_entry
        
        def get_current_session(self) -> Optional[Dict]:
            if not self.current_entry:
                return None
            
            duration = int((datetime.now() - self.current_entry.start_time).total_seconds() / 60)
            
            return {
                "task": self.current_entry.task_description,
                "category": self.current_entry.category,
                "duration_minutes": duration,
                "start_time": self.current_entry.start_time.isoformat(),
                "confidence": self.current_entry.confidence.value
            }
        
        def add_manual_entry(self, start_time: datetime, duration_minutes: int,
                            task_description: str, category: str = "work",
                            confidence: ConfidenceLevel = ConfidenceLevel.LOW) -> TimeEntry:
            entry = TimeEntry(
                start_time=start_time,
                end_time=start_time + timedelta(minutes=duration_minutes),
                task_description=task_description,
                category=category,
                confidence=confidence
            )
            self.entries.append(entry)
            return entry
        
        def get_daily_summary(self, date: Optional[datetime] = None) -> Dict:
            if date is None:
                date = datetime.now().date()
            
            day_entries = [
                entry for entry in self.entries
                if entry.start_time.date() == date and entry.is_complete()
            ]
            
            if not day_entries:
                return {
                    "date": date.isoformat(),
                    "total_minutes": 0,
                    "entries_count": 0,
                    "categories": {},
                    "confidence": "no_data",
                    "limitations": "No time tracking data available for this date"
                }
            
            total_minutes = sum(entry.duration_minutes() or 0 for entry in day_entries)
            categories = {}
            
            for entry in day_entries:
                if entry.category not in categories:
                    categories[entry.category] = 0
                categories[entry.category] += entry.duration_minutes() or 0
            
            return {
                "date": date.isoformat(),
                "total_minutes": total_minutes,
                "entries_count": len(day_entries),
                "categories": categories,
                "confidence": ConfidenceLevel.MODERATE.value,
                "limitations": "Data based on user input and may include estimation errors",
                "average_energy": sum(e.energy_level for e in day_entries) / len(day_entries) if day_entries else 0,
                "average_focus": sum(e.focus_quality for e in day_entries) / len(day_entries) if day_entries else 0,
                "total_interruptions": sum(e.interruptions for e in day_entries)
            }
    
    class ProductivityEngine:
        def __init__(self, user_id: str = "default_user"):
            self.user_id = user_id
            self.time_tracker = TimeTracker(user_id)
            
        def start_productivity_session(self, task_description: str = "", category: str = "work", 
                                     estimated_minutes: Optional[int] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
            entry = self.time_tracker.start_timer(task_description, category, estimated_minutes)
            
            return {
                "session_started": True,
                "entry_id": entry.start_time.isoformat(),
                "guidance": {"suggestions": [], "insights": [], "warnings": [], "confidence_notes": []},
                "ui_config": {},
                "user_control": {
                    "modify_estimate": "Available anytime during session",
                    "change_category": "Available anytime",
                    "disable_guidance": "All suggestions can be ignored",
                    "stop_early": "No minimum session length required"
                },
                "system_status": "optimal"
            }
        
        def end_productivity_session(self, user_notes: str = "", energy_level: int = 3,
                                   focus_quality: int = 3, interruptions: int = 0,
                                   satisfaction: int = 3) -> Dict[str, Any]:
            completed_entry = self.time_tracker.stop_timer(user_notes, energy_level, focus_quality, interruptions)
            
            if not completed_entry:
                return {"error": "No active session to end"}
            
            return {
                "session_summary": {
                    "task": completed_entry.task_description,
                    "category": completed_entry.category,
                    "duration_minutes": completed_entry.duration_minutes(),
                    "focus_quality": completed_entry.focus_quality,
                    "energy_level": completed_entry.energy_level,
                    "interruptions": completed_entry.interruptions,
                    "satisfaction": satisfaction
                },
                "insights": [],
                "areas_for_reflection": [],
                "positive_observations": []
            }
        
        def get_daily_productivity_summary(self, date: Optional[datetime] = None) -> Dict[str, Any]:
            return self.time_tracker.get_daily_summary(date)
        
        def get_comprehensive_insights(self, timeframe_days: int = 30) -> Dict[str, Any]:
            return {
                "summary": {"timeframe_days": timeframe_days, "data_sources": ["time_tracking"], "confidence_levels": {}, "user_interpretation_guidance": ""},
                "time_tracking_insights": {
                    "active_days": min(timeframe_days, len(set(e.start_time.date() for e in self.time_tracker.entries if e.is_complete()))),
                    "total_tracked_time": sum(e.duration_minutes() or 0 for e in self.time_tracker.entries if e.is_complete()),
                    "average_daily_time": 45
                },
                "pattern_insights": {},
                "ai_insights": [],
                "integration_insights": [],
                "next_steps": [],
                "limitations": []
            }
        
        def export_complete_user_data(self) -> Dict[str, Any]:
            return {
                "user_id": self.user_id,
                "export_timestamp": datetime.now().isoformat(),
                "productivity_engine": {"entries": len(self.time_tracker.entries)},
                "data_ownership_statement": {"ownership": "All data belongs entirely to the user"}
            }
    
    class UserProfile:
        def __init__(self, user_id: Optional[str] = None):
            self.user_id = user_id or str(uuid.uuid4())
            self.created_at = datetime.now()
            self.days_active = 0
            self.total_sessions = 0
            self.ui_complexity_level = 1
            self.current_productivity_mode = ProductivityMode.MAINTENANCE
        
        def track_usage(self, session_type: str = "general"):
            self.total_sessions += 1
        
        def export_all_data(self) -> Dict[str, Any]:
            return {
                "user_profile": {
                    "user_id": self.user_id,
                    "created_at": self.created_at.isoformat(),
                    "days_active": self.days_active,
                    "total_sessions": self.total_sessions
                }
            }

app = FastAPI(
    title="FlowState API",
    description="Human-Centered Productivity Intelligence API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="/app/frontend/build/static"), name="static")

# In-memory storage for demo (in production, use proper database)
users_db: Dict[str, Dict] = {}
engines_db: Dict[str, ProductivityEngine] = {}
profiles_db: Dict[str, UserProfile] = {}

# Pydantic models for API requests/responses
class StartSessionRequest(BaseModel):
    task_description: str = ""
    main_tag: str  # Required: Primary hashtag-like identifier
    sub_tag: Optional[str] = None  # Optional: Additional description
    estimated_minutes: Optional[int] = None
    energy_level: int = 3
    
class EndSessionRequest(BaseModel):
    session_id: str  # Required: Which session to end
    user_notes: str = ""
    energy_level: int = 3
    focus_quality: int = 3
    interruptions: int = 0
    satisfaction: int = 3

class UserCreateRequest(BaseModel):
    username: str
    preferences: Optional[Dict[str, Any]] = None

class UpdatePreferencesRequest(BaseModel):
    accessibility_prefs: Optional[Dict[str, Any]] = None
    productivity_prefs: Optional[Dict[str, Any]] = None
    privacy_settings: Optional[Dict[str, Any]] = None

# Helper functions
def get_or_create_user_engine(user_id: str) -> ProductivityEngine:
    """Get or create productivity engine for user"""
    if user_id not in engines_db:
        engines_db[user_id] = ProductivityEngine(user_id)
    return engines_db[user_id]

def get_or_create_user_profile(user_id: str) -> UserProfile:
    """Get or create user profile"""
    if user_id not in profiles_db:
        profiles_db[user_id] = UserProfile(user_id)
    return profiles_db[user_id]

# API Routes

def demo_page():
    """Generate the FlowState demo page HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlowState - Live Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            border-radius: 15px;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: white;
        }
        h1 {
            color: #1F2937;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #6B7280;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }
        .philosophy {
            background: #F0F9FF;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #3B82F6;
            margin: 20px 0;
        }
        .demo-section {
            background: #F9FAFB;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .btn {
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin: 5px;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: #6B7280;
        }
        .status {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .status.success {
            background: #ECFDF5;
            border: 1px solid #10B981;
            color: #065F46;
        }
        .status.error {
            background: #FEF2F2;
            border: 1px solid #EF4444;
            color: #B91C1C;
        }
        .status.info {
            background: #EFF6FF;
            border: 1px solid #3B82F6;
            color: #1E40AF;
        }
        .result {
            background: #F3F4F6;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-family: monospace;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .workflow {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .step {
            background: white;
            border: 2px solid #E5E7EB;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            transition: border-color 0.3s;
        }
        .step.active {
            border-color: #3B82F6;
            background: #EFF6FF;
        }
        .step.completed {
            border-color: #10B981;
            background: #ECFDF5;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .metric {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border: 1px solid #E5E7EB;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #3B82F6;
        }
        .metric-label {
            color: #6B7280;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡</div>
            <h1>FlowState</h1>
            <p class="subtitle">Human-Centered Productivity Intelligence</p>
        </div>

        <div class="philosophy">
            <h3>🧠 The Philosophy</h3>
            <p>Most productivity apps assume you need to be optimized. FlowState assumes you need to be understood.</p>
        </div>

        <div class="status info" id="health-status">
            🔄 Checking system health...
        </div>

        <div class="demo-section">
            <h3>🚀 Live FlowState Demo</h3>
            <p>Experience the complete FlowState workflow:</p>
            
            <div class="workflow">
                <div class="step" id="step-1">
                    <div>👤</div>
                    <h4>Create User</h4>
                    <p>Generate demo account</p>
                </div>
                <div class="step" id="step-2">
                    <div>▶️</div>
                    <h4>Start Session</h4>
                    <p>Begin productivity tracking</p>
                </div>
                <div class="step" id="step-3">
                    <div>⏸️</div>
                    <h4>End Session</h4>
                    <p>Complete with feedback</p>
                </div>
                <div class="step" id="step-4">
                    <div>📊</div>
                    <h4>View Analytics</h4>
                    <p>See insights & patterns</p>
                </div>
            </div>

            <div style="text-align: center; margin: 20px 0;">
                <button class="btn" onclick="startDemo()">🎯 Start Complete Demo</button>
                <button class="btn btn-secondary" onclick="resetDemo()">🔄 Reset Demo</button>
            </div>

            <div class="metrics" id="metrics" style="display: none;">
                <div class="metric">
                    <div class="metric-value" id="total-time">0m</div>
                    <div class="metric-label">Total Focus Time</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="sessions">0</div>
                    <div class="metric-label">Sessions Today</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="energy">0/5</div>
                    <div class="metric-label">Avg Energy</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="focus">0/5</div>
                    <div class="metric-label">Avg Focus</div>
                </div>
            </div>
        </div>

        <div class="demo-section">
            <h3>🔧 Manual Testing</h3>
            <button class="btn" onclick="createUser()">Create Demo User</button>
            <button class="btn" onclick="startSession()">Start Session</button>
            <button class="btn" onclick="endSession()">End Session</button>
            <button class="btn" onclick="getDailySummary()">Get Daily Summary</button>
            <button class="btn" onclick="getInsights()">Get Insights</button>
        </div>

        <div id="results"></div>

        <div class="demo-section">
            <h3>✨ FlowState Principles in Action</h3>
            <ul style="text-align: left; color: #374151;">
                <li><strong>User Agency:</strong> All suggestions can be ignored or modified</li>
                <li><strong>Honest Limitations:</strong> Confidence levels on all insights</li>
                <li><strong>Privacy First:</strong> Your data belongs to you</li>
                <li><strong>Progressive Complexity:</strong> Features unlock based on usage</li>
                <li><strong>Individual Differences:</strong> Accommodates various work styles</li>
            </ul>
        </div>
    </div>

    <script>
        let currentUserId = null;
        let currentStep = 0;

        // Check system health on load
        window.onload = async function() {
            await checkHealth();
        };

        async function checkHealth() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                document.getElementById('health-status').innerHTML = `
                    ✅ System Status: <strong>${data.status}</strong> | 
                    Active Users: ${data.active_users} | 
                    ${new Date(data.timestamp).toLocaleTimeString()}
                `;
                document.getElementById('health-status').className = 'status success';
            } catch (error) {
                document.getElementById('health-status').innerHTML = '❌ Backend not responding';
                document.getElementById('health-status').className = 'status error';
            }
        }

        function updateStep(step) {
            // Reset all steps
            for (let i = 1; i <= 4; i++) {
                const stepEl = document.getElementById(`step-${i}`);
                stepEl.className = 'step';
                if (i < step) stepEl.className = 'step completed';
                if (i === step) stepEl.className = 'step active';
            }
        }

        function showResult(title, data, isError = false) {
            const results = document.getElementById('results');
            const className = isError ? 'status error' : 'status success';
            results.innerHTML = `
                <div class="${className}">
                    <strong>${title}</strong>
                </div>
                <div class="result">${JSON.stringify(data, null, 2)}</div>
            `;
        }

        async function startDemo() {
            currentStep = 1;
            updateStep(1);
            await sleep(500);
            
            await createUser();
            await sleep(1000);
            
            updateStep(2);
            await startSession();
            await sleep(3000);
            
            updateStep(3);
            await endSession();
            await sleep(1000);
            
            updateStep(4);
            await getDailySummary();
            
            // Show metrics
            document.getElementById('metrics').style.display = 'grid';
        }

        async function resetDemo() {
            currentUserId = null;
            currentStep = 0;
            updateStep(0);
            document.getElementById('results').innerHTML = '';
            document.getElementById('metrics').style.display = 'none';
            showResult('Demo Reset', { message: 'Ready to start fresh!' });
        }

        async function createUser() {
            try {
                const response = await fetch('/api/demo/sample-user');
                const data = await response.json();
                currentUserId = data.user_id;
                
                showResult('✅ Demo User Created', {
                    user_id: data.user_id,
                    username: data.username,
                    sample_sessions: data.sample_sessions
                });
                
                return data;
            } catch (error) {
                showResult('❌ Error Creating User', { error: error.message }, true);
                throw error;
            }
        }

        async function startSession() {
            if (!currentUserId) {
                await createUser();
            }

            try {
                const response = await fetch(`/api/users/${currentUserId}/sessions/start`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        task_description: 'FlowState Live Demo Session',
                        category: 'work',
                        estimated_minutes: 30,
                        energy_level: 4
                    })
                });
                const data = await response.json();
                
                showResult('▶️ Session Started', {
                    session_started: data.session_started,
                    entry_id: data.entry_id,
                    system_status: data.system_status
                });
                
                return data;
            } catch (error) {
                showResult('❌ Error Starting Session', { error: error.message }, true);
                throw error;
            }
        }

        async function endSession() {
            if (!currentUserId) {
                showResult('❌ No Active User', { message: 'Please create a user first' }, true);
                return;
            }

            try {
                const response = await fetch(`/api/users/${currentUserId}/sessions/end`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_notes: 'Excellent FlowState demo session!',
                        energy_level: 4,
                        focus_quality: 5,
                        interruptions: 0,
                        satisfaction: 5
                    })
                });
                const data = await response.json();
                
                showResult('⏸️ Session Ended', {
                    task: data.session_summary.task,
                    duration: `${data.session_summary.duration_minutes} minutes`,
                    focus_quality: `${data.session_summary.focus_quality}/5`,
                    satisfaction: `${data.session_summary.satisfaction}/5`
                });
                
                return data;
            } catch (error) {
                showResult('❌ Error Ending Session', { error: error.message }, true);
                throw error;
            }
        }

        async function getDailySummary() {
            if (!currentUserId) {
                showResult('❌ No Active User', { message: 'Please create a user first' }, true);
                return;
            }

            try {
                const response = await fetch(`/api/users/${currentUserId}/summary/daily`);
                const data = await response.json();
                
                showResult('📊 Daily Summary', {
                    date: data.date,
                    total_minutes: data.total_minutes,
                    sessions: data.entries_count,
                    average_energy: data.average_energy?.toFixed(1),
                    average_focus: data.average_focus?.toFixed(1),
                    categories: Object.keys(data.categories || {})
                });

                // Update metrics display
                document.getElementById('total-time').textContent = `${data.total_minutes}m`;
                document.getElementById('sessions').textContent = data.entries_count;
                document.getElementById('energy').textContent = `${data.average_energy?.toFixed(1) || 0}/5`;
                document.getElementById('focus').textContent = `${data.average_focus?.toFixed(1) || 0}/5`;
                
                return data;
            } catch (error) {
                showResult('❌ Error Getting Summary', { error: error.message }, true);
                throw error;
            }
        }

        async function getInsights() {
            if (!currentUserId) {
                showResult('❌ No Active User', { message: 'Please create a user first' }, true);
                return;
            }

            try {
                const response = await fetch(`/api/users/${currentUserId}/insights?timeframe_days=7`);
                const data = await response.json();
                
                showResult('🧠 Productivity Insights', {
                    active_days: data.time_tracking_insights?.active_days || 0,
                    total_tracked_time: data.time_tracking_insights?.total_tracked_time || 0,
                    average_daily_time: data.time_tracking_insights?.average_daily_time || 0,
                    data_sources: data.summary?.data_sources || [],
                    limitations: data.limitations?.slice(0, 2) || []
                });
                
                return data;
            } catch (error) {
                showResult('❌ Error Getting Insights', { error: error.message }, true);
                throw error;
            }
        }

        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    </script>
</body>
</html>
    """

@app.get("/demo", response_class=HTMLResponse)
async def demo_route():
    """Serve the demo page"""
    return demo_page()

# API Routes

@app.get("/")
async def root():
    """API status endpoint"""
    return {
        "message": "FlowState API is running",
        "version": "1.0.0",
        "philosophy": "The first productivity app that works with your psychology, not against it"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_users": len(engines_db)
    }

# User Management
@app.post("/api/users")
async def create_user(request: UserCreateRequest):
    """Create a new user"""
    user_id = str(uuid.uuid4())
    
    # Create user profile
    profile = UserProfile(user_id)
    profile.created_at = datetime.now()
    profiles_db[user_id] = profile
    
    # Create productivity engine
    engine = ProductivityEngine(user_id)
    engines_db[user_id] = engine
    
    # Store user info
    users_db[user_id] = {
        "user_id": user_id,
        "username": request.username,
        "created_at": datetime.now().isoformat(),
        "preferences": request.preferences or {}
    }
    
    return {
        "user_id": user_id,
        "username": request.username,
        "message": "User created successfully"
    }

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Get user information"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = get_or_create_user_profile(user_id)
    user_info = users_db[user_id]
    
    return {
        "user_id": user_id,
        "username": user_info["username"],
        "created_at": user_info["created_at"],
        "profile": {
            "productivity_mode": profile.current_productivity_mode.value,
            "days_active": profile.days_active,
            "total_sessions": profile.total_sessions,
            "ui_complexity_level": profile.ui_complexity_level
        }
    }

@app.put("/api/users/{user_id}/preferences")
async def update_user_preferences(user_id: str, request: UpdatePreferencesRequest):
    """Update user preferences"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = get_or_create_user_profile(user_id)
    
    if request.accessibility_prefs:
        profile.update_accessibility_preferences(**request.accessibility_prefs)
    
    if request.productivity_prefs:
        profile.update_productivity_preferences(**request.productivity_prefs)
    
    if request.privacy_settings:
        profile.update_privacy_settings(**request.privacy_settings)
    
    return {"message": "Preferences updated successfully"}

# Session Management
@app.post("/api/users/{user_id}/sessions/start")
async def start_session(user_id: str, request: StartSessionRequest):
    """Start a productivity session with user-defined tags"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    profile = get_or_create_user_profile(user_id)
    
    # Start session with enhanced tagging system
    session_result = engine.start_productivity_session(
        main_tag=request.main_tag,
        sub_tag=request.sub_tag,
        task_description=request.task_description,
        estimated_minutes=request.estimated_minutes,
        context={"energy_level": request.energy_level}
    )
    
    # Track usage
    profile.track_usage("productivity_session")
    
    return session_result

@app.post("/api/users/{user_id}/sessions/end")
async def end_session(user_id: str, request: EndSessionRequest):
    """End a specific productivity session"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    
    session_result = engine.end_productivity_session(
        session_id=request.session_id,
        user_notes=request.user_notes,
        energy_level=request.energy_level,
        focus_quality=request.focus_quality,
        interruptions=request.interruptions,
        satisfaction=request.satisfaction
    )
    
    if "error" in session_result:
        raise HTTPException(status_code=404, detail=session_result["error"])
    
    return session_result

@app.get("/api/users/{user_id}/sessions/active")
async def get_active_sessions(user_id: str):
    """Get all currently active sessions"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    return engine.get_active_sessions()

@app.get("/api/users/{user_id}/sessions/current")
async def get_current_session(user_id: str):
    """Get current active sessions (legacy compatibility)"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    active_sessions = engine.get_active_sessions()
    
    # For backward compatibility, return the first active session
    if active_sessions["active_sessions"]:
        return {
            "active_session": True,
            "session": active_sessions["active_sessions"][0],
            "total_active": active_sessions["count"],
            "all_sessions": active_sessions["active_sessions"]
        }
    else:
        return {"active_session": False, "total_active": 0}

@app.get("/api/users/{user_id}/sessions/{session_id}")
async def get_session(user_id: str, session_id: str):
    """Get specific session details"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    session = engine.time_tracker.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@app.post("/api/users/{user_id}/sessions/{session_id}/pause")
async def pause_session(user_id: str, session_id: str):
    """Pause a session (future enhancement)"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    result = engine.time_tracker.pause_session(session_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session paused", "session_id": session_id}

@app.post("/api/users/{user_id}/sessions/{session_id}/resume")
async def resume_session(user_id: str, session_id: str):
    """Resume a paused session (future enhancement)"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    result = engine.time_tracker.resume_session(session_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session resumed", "session_id": session_id}

@app.delete("/api/users/{user_id}/sessions/{session_id}")
async def cancel_session(user_id: str, session_id: str):
    """Cancel a session without recording completion"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    result = engine.time_tracker.cancel_session(session_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session cancelled", "session_id": session_id}

# Analytics and Insights
@app.get("/api/users/{user_id}/summary/daily")
async def get_daily_summary(user_id: str, date: Optional[str] = None):
    """Get daily productivity summary"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    
    if date:
        try:
            target_date = datetime.fromisoformat(date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")
    else:
        target_date = None
    
    summary = engine.get_daily_productivity_summary(target_date)
    return summary

@app.get("/api/users/{user_id}/insights")
async def get_insights(user_id: str, timeframe_days: int = 30):
    """Get comprehensive productivity insights"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    insights = engine.get_comprehensive_insights(timeframe_days)
    
    return insights

@app.get("/api/users/{user_id}/patterns")
async def get_patterns(user_id: str):
    """Get pattern analysis"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    patterns = engine.get_patterns()
    
    return patterns

# Tag Management Endpoints
@app.get("/api/users/{user_id}/tags")
async def get_user_tags(user_id: str):
    """Get all tags the user has used"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    tags = engine.time_tracker.get_user_tags()
    
    return {
        "user_tags": tags,
        "count": len(tags),
        "suggestion": "Use tags that feel natural to describe your work"
    }

@app.get("/api/users/{user_id}/tags/analytics")
async def get_tag_analytics(user_id: str, timeframe_days: int = 30):
    """Get detailed analytics based on user's tagging patterns"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    analytics = engine.time_tracker.get_tag_analytics(timeframe_days)
    
    return analytics

@app.get("/api/users/{user_id}/estimation-accuracy")
async def get_estimation_accuracy(user_id: str):
    """Get user's time estimation accuracy"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    accuracy = engine.time_tracker.get_estimation_accuracy()
    
    return accuracy

# Self-Discovery Features
@app.post("/api/users/{user_id}/self-discovery/start")
async def start_self_discovery(user_id: str, category: str, support_level: str = "guided"):
    """Start a self-discovery session"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    
    try:
        reflection_category = ReflectionCategory(category)
        support_level_enum = SupportLevel(support_level)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category or support level")
    
    discovery_session = engine.start_self_discovery_session(
        reflection_category, support_level_enum
    )
    
    return discovery_session

# Data Export and Privacy
@app.get("/api/users/{user_id}/export")
async def export_user_data(user_id: str):
    """Export all user data"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    profile = get_or_create_user_profile(user_id)
    
    # Export from all modules
    engine_data = engine.export_complete_user_data()
    profile_data = profile.export_all_data()
    user_data = users_db[user_id]
    
    return {
        "export_timestamp": datetime.now().isoformat(),
        "user_info": user_data,
        "productivity_engine": engine_data,
        "user_profile": profile_data,
        "data_ownership": "This data belongs entirely to the user"
    }

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: str, confirmation: str):
    """Delete user and all data"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    expected_confirmation = f"DELETE-{user_id[:8]}"
    if confirmation != expected_confirmation:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid confirmation. Required: {expected_confirmation}"
        )
    
    # Delete from all storage
    del users_db[user_id]
    if user_id in engines_db:
        del engines_db[user_id]
    if user_id in profiles_db:
        del profiles_db[user_id]
    
    return {"message": "User and all data deleted successfully"}

# Demo Helper Endpoints
@app.get("/api/demo/sample-user")
async def create_sample_user():
    """Create a sample user with demo data using the new tagging system"""
    user_id = str(uuid.uuid4())
    username = f"demo_user_{user_id[:8]}"
    
    # Create user
    profile = UserProfile(user_id)
    engine = ProductivityEngine(user_id)
    
    # Add sample sessions with diverse tagging
    sample_sessions = [
        {"task": "Client project planning", "main_tag": "work", "sub_tag": "client-meeting", "duration": 45, "energy": 4, "focus": 4},
        {"task": "React tutorial", "main_tag": "learning", "sub_tag": "react", "duration": 60, "energy": 3, "focus": 5},
        {"task": "Email management", "main_tag": "admin", "sub_tag": "email", "duration": 25, "energy": 2, "focus": 3},
        {"task": "Morning workout", "main_tag": "exercise", "sub_tag": "cardio", "duration": 30, "energy": 5, "focus": 4},
        {"task": "Team standup", "main_tag": "work", "sub_tag": "meeting", "duration": 15, "energy": 3, "focus": 3},
        {"task": "Writing blog post", "main_tag": "creative", "sub_tag": "writing", "duration": 90, "energy": 4, "focus": 5},
        {"task": "Meditation", "main_tag": "wellness", "sub_tag": "mindfulness", "duration": 20, "energy": 4, "focus": 4}
    ]
    
    # Create sessions with realistic time spread
    for i, session in enumerate(sample_sessions):
        # Create time entry manually for demo
        start_time = datetime.now() - timedelta(hours=len(sample_sessions)-i, minutes=15)
        end_time = start_time + timedelta(minutes=session["duration"])
        
        session_entry = TimeEntry(
            session_id=str(uuid.uuid4()),
            start_time=start_time,
            tag=SessionTag(main_tag=session["main_tag"], sub_tag=session["sub_tag"]),
            task_description=session["task"],
            end_time=end_time,
            status=SessionStatus.COMPLETED,
            confidence=ConfidenceLevel.MODERATE,
            energy_level=session["energy"],
            focus_quality=session["focus"],
            interruptions=0 if session["focus"] >= 4 else 1
        )
        
        engine.time_tracker.entries.append(session_entry)
        engine.time_tracker.user_tags.add(session["main_tag"])
    
    # Store user
    users_db[user_id] = {
        "user_id": user_id,
        "username": username,
        "created_at": datetime.now().isoformat(),
        "preferences": {},
        "is_demo": True
    }
    engines_db[user_id] = engine
    profiles_db[user_id] = profile
    
    return {
        "user_id": user_id,
        "username": username,
        "message": "Sample user created with enhanced tagging demo data",
        "sample_sessions": len(sample_sessions),
        "unique_main_tags": len(engine.time_tracker.user_tags),
        "sample_tags": list(engine.time_tracker.user_tags)
    }

@app.get("/api/demo/reset/{user_id}")
async def reset_demo_user(user_id: str):
    """Reset demo user data"""
    if user_id not in users_db or not users_db[user_id].get("is_demo"):
        raise HTTPException(status_code=404, detail="Demo user not found")
    
    # Reset engine and profile
    engines_db[user_id] = ProductivityEngine(user_id)
    profiles_db[user_id] = UserProfile(user_id)
    
    return {"message": "Demo user data reset"}

# Serve the React app for any unmatched routes (MUST BE LAST!)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve React app for frontend routes"""
    # For demo route, serve the demo page first
    if full_path == "demo" or full_path == "demo/":
        return demo_page()
    
    # Try to serve React build files for frontend routes
    try:
        with open("/app/frontend/build/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        # If React build doesn't exist, show error message instead of demo page
        return HTMLResponse(content="""
        <html>
        <head><title>FlowState - Error</title></head>
        <body>
        <h1>React Build Not Found</h1>
        <p>The React application build is missing. Try the <a href="/demo">demo page</a> instead.</p>
        </body>
        </html>
        """, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
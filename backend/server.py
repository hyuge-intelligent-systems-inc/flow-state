"""
FlowState FastAPI Backend Server
Exposes the FlowState productivity system through REST API
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import uuid

# Import FlowState modules
try:
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

# In-memory storage for demo (in production, use proper database)
users_db: Dict[str, Dict] = {}
engines_db: Dict[str, ProductivityEngine] = {}
profiles_db: Dict[str, UserProfile] = {}

# Pydantic models for API requests/responses
class StartSessionRequest(BaseModel):
    task_description: str = ""
    category: str = "work"
    estimated_minutes: Optional[int] = None
    energy_level: int = 3
    
class EndSessionRequest(BaseModel):
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
    """Start a productivity session"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    profile = get_or_create_user_profile(user_id)
    
    # Start session with context
    context = {"energy_level": request.energy_level}
    
    session_result = engine.start_productivity_session(
        task_description=request.task_description,
        category=request.category,
        estimated_minutes=request.estimated_minutes,
        context=context
    )
    
    # Track usage
    profile.track_usage("productivity_session")
    
    return session_result

@app.post("/api/users/{user_id}/sessions/end")
async def end_session(user_id: str, request: EndSessionRequest):
    """End current productivity session"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    
    session_result = engine.end_productivity_session(
        user_notes=request.user_notes,
        energy_level=request.energy_level,
        focus_quality=request.focus_quality,
        interruptions=request.interruptions,
        satisfaction=request.satisfaction
    )
    
    return session_result

@app.get("/api/users/{user_id}/sessions/current")
async def get_current_session(user_id: str):
    """Get current active session"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    engine = get_or_create_user_engine(user_id)
    current_session = engine.time_tracker.get_current_session()
    
    if not current_session:
        return {"active_session": False}
    
    return {
        "active_session": True,
        "session": current_session
    }

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
    
    if len(engine.time_tracker.entries) < 5:
        return {
            "message": "Not enough data for pattern analysis",
            "required_sessions": 5,
            "current_sessions": len(engine.time_tracker.entries)
        }
    
    patterns = engine.pattern_analyzer.analyze_time_patterns(
        engine.time_tracker.entries,
        timeframe_days=30
    )
    
    # Convert patterns to serializable format
    patterns_dict = {}
    for name, pattern in patterns.items():
        patterns_dict[name] = {
            "description": pattern.description,
            "confidence": pattern.confidence.value,
            "sample_size": pattern.sample_size,
            "limitations": pattern.limitations,
            "user_interpretation_needed": pattern.user_interpretation_needed,
            "supporting_data": pattern.supporting_data
        }
    
    return {"patterns": patterns_dict}

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
    """Create a sample user with demo data"""
    user_id = str(uuid.uuid4())
    username = f"demo_user_{user_id[:8]}"
    
    # Create user
    profile = UserProfile(user_id)
    engine = ProductivityEngine(user_id)
    
    # Add some sample data
    sample_sessions = [
        {"task": "Morning planning", "category": "planning", "duration": 15},
        {"task": "Deep work session", "category": "work", "duration": 90},
        {"task": "Email review", "category": "admin", "duration": 30},
        {"task": "Team meeting", "category": "meeting", "duration": 60},
        {"task": "Learning session", "category": "learning", "duration": 45}
    ]
    
    for i, session in enumerate(sample_sessions):
        start_time = datetime.now() - timedelta(hours=len(sample_sessions)-i)
        end_time = start_time + timedelta(minutes=session["duration"])
        
        entry = engine.time_tracker.add_manual_entry(
            start_time=start_time,
            duration_minutes=session["duration"],
            task_description=session["task"],
            category=session["category"],
            confidence=ConfidenceLevel.HIGH
        )
    
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
        "message": "Sample user created with demo data",
        "sample_sessions": len(sample_sessions)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
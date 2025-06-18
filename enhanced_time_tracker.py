"""
Enhanced FlowState Core Time Tracker with Multi-Session Support and Tagging System
Supports concurrent sessions and user-defined tag-based categorization
"""

import time
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class ConfidenceLevel(Enum):
    """Honest confidence levels for time tracking accuracy"""
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    UNCERTAIN = "uncertain"


class SessionStatus(Enum):
    """Status of a time tracking session"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class SessionTag:
    """User-defined tag with main tag and optional sub-tag"""
    main_tag: str  # Primary hashtag-like identifier (e.g., "work", "learning", "exercise")
    sub_tag: Optional[str] = None  # Additional description (e.g., "client-meeting", "react-tutorial", "cardio")
    
    def __str__(self) -> str:
        """String representation for display"""
        if self.sub_tag:
            return f"#{self.main_tag}/{self.sub_tag}"
        return f"#{self.main_tag}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            "main_tag": self.main_tag,
            "sub_tag": self.sub_tag
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SessionTag':
        """Create from dictionary"""
        return cls(
            main_tag=data["main_tag"],
            sub_tag=data.get("sub_tag")
        )


@dataclass
class TimeEntry:
    """Individual time tracking entry with enhanced tagging support"""
    session_id: str
    start_time: datetime
    tag: SessionTag
    task_description: str = ""
    end_time: Optional[datetime] = None
    status: SessionStatus = SessionStatus.ACTIVE
    confidence: ConfidenceLevel = ConfidenceLevel.MODERATE
    user_notes: str = ""
    interruptions: int = 0
    energy_level: int = 3  # 1-5 scale, user self-reported
    focus_quality: int = 3  # 1-5 scale, user self-reported
    estimated_minutes: Optional[int] = None
    
    def duration_minutes(self) -> Optional[int]:
        """Calculate duration with honest uncertainty handling"""
        if not self.end_time:
            return None
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)
    
    def current_duration_minutes(self) -> int:
        """Get current duration for active sessions"""
        end_time = self.end_time if self.end_time else datetime.now()
        delta = end_time - self.start_time
        return int(delta.total_seconds() / 60)
    
    def is_active(self) -> bool:
        """Check if session is currently active"""
        return self.status == SessionStatus.ACTIVE
    
    def is_complete(self) -> bool:
        """Check if time entry is complete"""
        return self.status == SessionStatus.COMPLETED and self.end_time is not None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        data = {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "tag": self.tag.to_dict(),
            "task_description": self.task_description,
            "status": self.status.value,
            "confidence": self.confidence.value,
            "user_notes": self.user_notes,
            "interruptions": self.interruptions,
            "energy_level": self.energy_level,
            "focus_quality": self.focus_quality,
            "estimated_minutes": self.estimated_minutes
        }
        
        if self.end_time:
            data["end_time"] = self.end_time.isoformat()
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TimeEntry':
        """Create from dictionary"""
        entry = cls(
            session_id=data["session_id"],
            start_time=datetime.fromisoformat(data["start_time"]),
            tag=SessionTag.from_dict(data["tag"]),
            task_description=data.get("task_description", ""),
            status=SessionStatus(data.get("status", "active")),
            confidence=ConfidenceLevel(data.get("confidence", "moderate")),
            user_notes=data.get("user_notes", ""),
            interruptions=data.get("interruptions", 0),
            energy_level=data.get("energy_level", 3),
            focus_quality=data.get("focus_quality", 3),
            estimated_minutes=data.get("estimated_minutes")
        )
        
        if "end_time" in data:
            entry.end_time = datetime.fromisoformat(data["end_time"])
            
        return entry


class MultiSessionTimeTracker:
    """
    Enhanced time tracker supporting multiple concurrent sessions with tagging
    
    Key features:
    - Multiple simultaneous active sessions
    - User-defined tagging system (main tag + sub tag)
    - Flexible categorization based on user preferences
    - Async session management
    """
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.entries: List[TimeEntry] = []
        self.active_sessions: Dict[str, TimeEntry] = {}  # session_id -> TimeEntry
        self.user_tags: Set[str] = set()  # Track all main tags user has used
        self.estimation_history: List[Tuple[int, int]] = []  # (estimated, actual) pairs
        
    def start_session(self, main_tag: str, sub_tag: Optional[str] = None, 
                     task_description: str = "", estimated_minutes: Optional[int] = None) -> TimeEntry:
        """
        Start a new tracking session with user-defined tags
        
        Args:
            main_tag: Primary hashtag-like identifier
            sub_tag: Optional additional description  
            task_description: What the user is working on
            estimated_minutes: User's time estimate (optional)
        
        Returns:
            TimeEntry: The created time entry
        """
        session_id = str(uuid.uuid4())
        tag = SessionTag(main_tag=main_tag.lower(), sub_tag=sub_tag)
        
        # Track user's tags for autocomplete/suggestions
        self.user_tags.add(main_tag.lower())
        
        entry = TimeEntry(
            session_id=session_id,
            start_time=datetime.now(),
            tag=tag,
            task_description=task_description,
            estimated_minutes=estimated_minutes,
            confidence=ConfidenceLevel.MODERATE
        )
        
        self.entries.append(entry)
        self.active_sessions[session_id] = entry
        
        return entry
    
    def end_session(self, session_id: str, user_notes: str = "", energy_level: int = 3,
                   focus_quality: int = 3, interruptions: int = 0) -> Optional[TimeEntry]:
        """
        End a specific session by ID
        
        Args:
            session_id: ID of the session to end
            user_notes: User's reflection on the work session
            energy_level: Self-reported energy (1-5)
            focus_quality: Self-reported focus quality (1-5)
            interruptions: Number of interruptions
        
        Returns:
            Optional[TimeEntry]: Completed entry or None if not found
        """
        if session_id not in self.active_sessions:
            return None
        
        entry = self.active_sessions[session_id]
        
        # Complete the entry
        entry.end_time = datetime.now()
        entry.status = SessionStatus.COMPLETED
        entry.user_notes = user_notes
        entry.energy_level = energy_level
        entry.focus_quality = focus_quality
        entry.interruptions = interruptions
        
        # Update estimation accuracy if user provided estimate
        duration = entry.duration_minutes()
        if duration and entry.estimated_minutes:
            self.estimation_history.append((entry.estimated_minutes, duration))
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return entry
    
    def pause_session(self, session_id: str) -> Optional[TimeEntry]:
        """Pause a session (for future enhancement)"""
        if session_id not in self.active_sessions:
            return None
        
        entry = self.active_sessions[session_id]
        entry.status = SessionStatus.PAUSED
        return entry
    
    def resume_session(self, session_id: str) -> Optional[TimeEntry]:
        """Resume a paused session (for future enhancement)"""
        if session_id not in self.active_sessions:
            return None
        
        entry = self.active_sessions[session_id]
        if entry.status == SessionStatus.PAUSED:
            entry.status = SessionStatus.ACTIVE
        return entry
    
    def cancel_session(self, session_id: str) -> Optional[TimeEntry]:
        """Cancel a session without recording completion"""
        if session_id not in self.active_sessions:
            return None
        
        entry = self.active_sessions[session_id]
        entry.status = SessionStatus.CANCELLED
        entry.end_time = datetime.now()
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        return entry
    
    def get_active_sessions(self) -> List[Dict]:
        """Get all currently active sessions"""
        active_sessions = []
        
        for session_id, entry in self.active_sessions.items():
            if entry.is_active():
                active_sessions.append({
                    "session_id": session_id,
                    "tag": str(entry.tag),
                    "main_tag": entry.tag.main_tag,
                    "sub_tag": entry.tag.sub_tag,
                    "task": entry.task_description,
                    "duration_minutes": entry.current_duration_minutes(),
                    "start_time": entry.start_time.isoformat(),
                    "energy_level": entry.energy_level,
                    "confidence": entry.confidence.value
                })
        
        return active_sessions
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get specific session details"""
        if session_id in self.active_sessions:
            entry = self.active_sessions[session_id]
            return {
                "session_id": session_id,
                "tag": str(entry.tag),
                "main_tag": entry.tag.main_tag,
                "sub_tag": entry.tag.sub_tag,
                "task": entry.task_description,
                "duration_minutes": entry.current_duration_minutes(),
                "start_time": entry.start_time.isoformat(),
                "status": entry.status.value,
                "confidence": entry.confidence.value
            }
        
        # Check completed sessions
        for entry in self.entries:
            if entry.session_id == session_id:
                return {
                    "session_id": session_id,
                    "tag": str(entry.tag),
                    "main_tag": entry.tag.main_tag,
                    "sub_tag": entry.tag.sub_tag,
                    "task": entry.task_description,
                    "duration_minutes": entry.duration_minutes(),
                    "start_time": entry.start_time.isoformat(),
                    "end_time": entry.end_time.isoformat() if entry.end_time else None,
                    "status": entry.status.value,
                    "confidence": entry.confidence.value
                }
        
        return None
    
    def get_daily_summary(self, date: Optional[datetime] = None) -> Dict:
        """
        Get daily summary with tag-based analytics
        """
        if date is None:
            date = datetime.now().date()
        
        # Filter entries for the day
        day_entries = [
            entry for entry in self.entries
            if entry.start_time.date() == date and entry.is_complete()
        ]
        
        if not day_entries:
            return {
                "date": date.isoformat(),
                "total_minutes": 0,
                "entries_count": 0,
                "active_sessions_count": len(self.active_sessions),
                "tags": {},
                "main_tags": {},
                "confidence": "no_data",
                "limitations": "No time tracking data available for this date"
            }
        
        # Calculate summary with tag-based grouping
        total_minutes = sum(entry.duration_minutes() or 0 for entry in day_entries)
        
        # Group by full tags (main + sub)
        tags = {}
        main_tags = {}
        
        for entry in day_entries:
            # Full tag grouping
            tag_str = str(entry.tag)
            if tag_str not in tags:
                tags[tag_str] = {"minutes": 0, "count": 0, "main_tag": entry.tag.main_tag, "sub_tag": entry.tag.sub_tag}
            tags[tag_str]["minutes"] += entry.duration_minutes() or 0
            tags[tag_str]["count"] += 1
            
            # Main tag grouping
            main_tag = entry.tag.main_tag
            if main_tag not in main_tags:
                main_tags[main_tag] = {"minutes": 0, "count": 0, "sub_tags": set()}
            main_tags[main_tag]["minutes"] += entry.duration_minutes() or 0
            main_tags[main_tag]["count"] += 1
            if entry.tag.sub_tag:
                main_tags[main_tag]["sub_tags"].add(entry.tag.sub_tag)
        
        # Convert sets to lists for JSON serialization
        for main_tag_data in main_tags.values():
            main_tag_data["sub_tags"] = list(main_tag_data["sub_tags"])
        
        # Assess overall confidence
        confidence_levels = [entry.confidence.value for entry in day_entries]
        high_confidence_count = confidence_levels.count(ConfidenceLevel.HIGH.value)
        overall_confidence = ConfidenceLevel.HIGH.value if high_confidence_count > len(confidence_levels) * 0.7 else ConfidenceLevel.MODERATE.value
        
        return {
            "date": date.isoformat(),
            "total_minutes": total_minutes,
            "entries_count": len(day_entries),
            "active_sessions_count": len(self.active_sessions),
            "tags": tags,
            "main_tags": main_tags,
            "confidence": overall_confidence,
            "limitations": "Data based on user input and may include estimation errors",
            "average_energy": sum(e.energy_level for e in day_entries) / len(day_entries),
            "average_focus": sum(e.focus_quality for e in day_entries) / len(day_entries),
            "total_interruptions": sum(e.interruptions for e in day_entries)
        }
    
    def get_tag_analytics(self, timeframe_days: int = 30) -> Dict:
        """
        Get analytics based on user's tagging patterns
        """
        cutoff_date = datetime.now() - timedelta(days=timeframe_days)
        recent_entries = [
            entry for entry in self.entries
            if entry.start_time >= cutoff_date and entry.is_complete()
        ]
        
        if not recent_entries:
            return {
                "timeframe_days": timeframe_days,
                "total_entries": 0,
                "message": "No data available for the specified timeframe"
            }
        
        # Analyze by main tags
        main_tag_analysis = {}
        for entry in recent_entries:
            main_tag = entry.tag.main_tag
            if main_tag not in main_tag_analysis:
                main_tag_analysis[main_tag] = {
                    "total_minutes": 0,
                    "session_count": 0,
                    "sub_tags": {},
                    "avg_energy": [],
                    "avg_focus": [],
                    "avg_duration": []
                }
            
            duration = entry.duration_minutes() or 0
            main_tag_analysis[main_tag]["total_minutes"] += duration
            main_tag_analysis[main_tag]["session_count"] += 1
            main_tag_analysis[main_tag]["avg_energy"].append(entry.energy_level)
            main_tag_analysis[main_tag]["avg_focus"].append(entry.focus_quality)
            main_tag_analysis[main_tag]["avg_duration"].append(duration)
            
            # Sub-tag analysis
            if entry.tag.sub_tag:
                sub_tag = entry.tag.sub_tag
                if sub_tag not in main_tag_analysis[main_tag]["sub_tags"]:
                    main_tag_analysis[main_tag]["sub_tags"][sub_tag] = {
                        "total_minutes": 0,
                        "session_count": 0,
                        "avg_energy": [],
                        "avg_focus": []
                    }
                
                main_tag_analysis[main_tag]["sub_tags"][sub_tag]["total_minutes"] += duration
                main_tag_analysis[main_tag]["sub_tags"][sub_tag]["session_count"] += 1
                main_tag_analysis[main_tag]["sub_tags"][sub_tag]["avg_energy"].append(entry.energy_level)
                main_tag_analysis[main_tag]["sub_tags"][sub_tag]["avg_focus"].append(entry.focus_quality)
        
        # Calculate averages
        for main_tag, data in main_tag_analysis.items():
            if data["avg_energy"]:
                data["avg_energy"] = sum(data["avg_energy"]) / len(data["avg_energy"])
                data["avg_focus"] = sum(data["avg_focus"]) / len(data["avg_focus"])
                data["avg_duration"] = sum(data["avg_duration"]) / len(data["avg_duration"])
            
            for sub_tag, sub_data in data["sub_tags"].items():
                if sub_data["avg_energy"]:
                    sub_data["avg_energy"] = sum(sub_data["avg_energy"]) / len(sub_data["avg_energy"])
                    sub_data["avg_focus"] = sum(sub_data["avg_focus"]) / len(sub_data["avg_focus"])
        
        return {
            "timeframe_days": timeframe_days,
            "total_entries": len(recent_entries),
            "total_time_minutes": sum(entry.duration_minutes() or 0 for entry in recent_entries),
            "main_tag_analysis": main_tag_analysis,
            "user_tags": list(self.user_tags),
            "insights": self._generate_tag_insights(main_tag_analysis)
        }
    
    def _generate_tag_insights(self, main_tag_analysis: Dict) -> List[str]:
        """Generate insights based on tagging patterns"""
        insights = []
        
        if not main_tag_analysis:
            return ["Not enough data to generate insights"]
        
        # Most productive tag
        most_productive_tag = max(main_tag_analysis.keys(), 
                                key=lambda k: main_tag_analysis[k]["total_minutes"])
        insights.append(f"Most time spent on #{most_productive_tag} activities")
        
        # Highest energy tag
        highest_energy_tag = max(main_tag_analysis.keys(),
                               key=lambda k: main_tag_analysis[k]["avg_energy"])
        if main_tag_analysis[highest_energy_tag]["avg_energy"] > 3.5:
            insights.append(f"#{highest_energy_tag} activities give you the most energy")
        
        # Best focus tag
        best_focus_tag = max(main_tag_analysis.keys(),
                           key=lambda k: main_tag_analysis[k]["avg_focus"])
        if main_tag_analysis[best_focus_tag]["avg_focus"] > 3.5:
            insights.append(f"You focus best during #{best_focus_tag} activities")
        
        # Tag diversity
        tag_count = len(main_tag_analysis)
        if tag_count >= 5:
            insights.append(f"You're tracking {tag_count} different types of activities - good diversity!")
        elif tag_count <= 2:
            insights.append("Consider using more specific tags to better understand your patterns")
        
        return insights
    
    def get_user_tags(self) -> List[str]:
        """Get all tags the user has used for autocomplete"""
        return sorted(list(self.user_tags))
    
    def get_estimation_accuracy(self) -> Dict:
        """Calculate user's time estimation accuracy"""
        if len(self.estimation_history) < 3:
            return {
                "accuracy": "insufficient_data",
                "sample_size": len(self.estimation_history),
                "message": "Need at least 3 estimated tasks to calculate accuracy",
                "confidence": ConfidenceLevel.UNCERTAIN.value
            }
        
        # Calculate accuracy metrics
        errors = []
        for estimated, actual in self.estimation_history:
            error_percent = abs(estimated - actual) / actual * 100
            errors.append(error_percent)
        
        avg_error = sum(errors) / len(errors)
        
        # Honest assessment
        if avg_error < 20:
            accuracy_level = "good"
        elif avg_error < 40:
            accuracy_level = "moderate"
        else:
            accuracy_level = "needs_improvement"
        
        return {
            "accuracy": accuracy_level,
            "average_error_percent": round(avg_error, 1),
            "sample_size": len(self.estimation_history),
            "confidence": ConfidenceLevel.MODERATE.value,
            "limitations": "Based on limited data and subject to recall bias"
        }
    
    def export_data(self) -> Dict:
        """Export all data with full user control"""
        return {
            "user_id": self.user_id,
            "export_date": datetime.now().isoformat(),
            "entries": [entry.to_dict() for entry in self.entries],
            "active_sessions": [entry.to_dict() for entry in self.active_sessions.values()],
            "user_tags": list(self.user_tags),
            "estimation_history": self.estimation_history,
            "data_integrity": {
                "total_entries": len(self.entries),
                "complete_entries": len([e for e in self.entries if e.is_complete()]),
                "active_sessions": len(self.active_sessions),
                "confidence_distribution": self._get_confidence_distribution()
            }
        }
    
    def _get_confidence_distribution(self) -> Dict[str, int]:
        """Internal method to analyze confidence levels"""
        distribution = {level.value: 0 for level in ConfidenceLevel}
        for entry in self.entries:
            distribution[entry.confidence.value] += 1
        return distribution
    
    def clear_data(self) -> bool:
        """Clear all data with user control (for privacy)"""
        self.entries.clear()
        self.active_sessions.clear()
        self.user_tags.clear()
        self.estimation_history.clear()
        return True


# Example usage and testing
if __name__ == "__main__":
    # Create tracker
    tracker = MultiSessionTimeTracker("user_123")
    
    # Start multiple concurrent sessions
    session1 = tracker.start_session("work", "client-project", "Building new feature", 60)
    session2 = tracker.start_session("learning", "react", "Learning React hooks", 30)
    session3 = tracker.start_session("exercise", "cardio", "Morning run", 45)
    
    print("Active sessions:", len(tracker.get_active_sessions()))
    
    # Simulate some work time
    time.sleep(2)
    
    # End sessions with feedback
    completed1 = tracker.end_session(
        session1.session_id,
        user_notes="Good progress on the authentication system",
        energy_level=4,
        focus_quality=4,
        interruptions=1
    )
    
    completed2 = tracker.end_session(
        session2.session_id,
        user_notes="Learned about useEffect and custom hooks",
        energy_level=3,
        focus_quality=5,
        interruptions=0
    )
    
    # Keep exercise session running
    print("Remaining active sessions:", len(tracker.get_active_sessions()))
    
    # Get summary
    summary = tracker.get_daily_summary()
    print("Daily Summary:", json.dumps(summary, indent=2))
    
    # Get tag analytics
    analytics = tracker.get_tag_analytics()
    print("Tag Analytics:", json.dumps(analytics, indent=2))
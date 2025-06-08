

"""
FlowState Core Time Tracker
Based on expert analysis: Reality-based productivity with human agency

Key principles implemented:
- User agency and control preservation
- Honest limitations and uncertainty acknowledgment
- Failure planning and resilience
- Individual differences accommodation
- Evidence-based methods over marketing claims
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ConfidenceLevel(Enum):
    """Honest confidence levels for time tracking accuracy"""
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    UNCERTAIN = "uncertain"


class TaskComplexity(Enum):
    """Task complexity levels for realistic estimation"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    UNKNOWN = "unknown"


@dataclass
class TimeEntry:
    """Individual time tracking entry with honest uncertainty"""
    start_time: datetime
    end_time: Optional[datetime] = None
    task_description: str = ""
    category: str = "uncategorized"
    complexity: TaskComplexity = TaskComplexity.UNKNOWN
    confidence: ConfidenceLevel = ConfidenceLevel.MODERATE
    user_notes: str = ""
    interruptions: int = 0
    energy_level: int = 3  # 1-5 scale, user self-reported
    focus_quality: int = 3  # 1-5 scale, user self-reported
    
    def duration_minutes(self) -> Optional[int]:
        """Calculate duration with honest uncertainty handling"""
        if not self.end_time:
            return None
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)
    
    def is_complete(self) -> bool:
        """Check if time entry is complete"""
        return self.end_time is not None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        data = asdict(self)
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        data['complexity'] = self.complexity.value
        data['confidence'] = self.confidence.value
        return data


class TimeTracker:
    """
    Realistic time tracker implementing expert analysis principles:
    - User agency preservation
    - Honest limitations
    - Failure recovery
    - Individual adaptation
    """
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.entries: List[TimeEntry] = []
        self.current_entry: Optional[TimeEntry] = None
        self.categories: List[str] = ["work", "learning", "planning", "break", "personal"]
        self.estimation_history: List[Tuple[int, int]] = []  # (estimated, actual) pairs
        
    def start_timer(self, task_description: str = "", category: str = "work", 
                   estimated_minutes: Optional[int] = None) -> TimeEntry:
        """
        Start tracking time with user agency preserved
        
        Args:
            task_description: User-provided task description
            category: User-selected category
            estimated_minutes: User's time estimate (optional)
        
        Returns:
            TimeEntry: The created time entry
        """
        # Stop current timer if running (graceful handling)
        if self.current_entry and not self.current_entry.is_complete():
            self.stop_timer()
        
        # Create new entry
        self.current_entry = TimeEntry(
            start_time=datetime.now(),
            task_description=task_description,
            category=category,
            confidence=ConfidenceLevel.MODERATE  # Honest about limitations
        )
        
        # Store estimation for learning (if provided)
        if estimated_minutes:
            self.current_entry.user_notes = f"Estimated: {estimated_minutes} minutes"
        
        self.entries.append(self.current_entry)
        return self.current_entry
    
    def stop_timer(self, user_notes: str = "", energy_level: int = 3, 
                  focus_quality: int = 3, interruptions: int = 0) -> Optional[TimeEntry]:
        """
        Stop current timer with user-provided context
        
        Args:
            user_notes: User's reflection on the work session
            energy_level: Self-reported energy (1-5)
            focus_quality: Self-reported focus quality (1-5)
            interruptions: Number of interruptions
        
        Returns:
            Optional[TimeEntry]: Completed entry or None if no timer running
        """
        if not self.current_entry or self.current_entry.is_complete():
            return None
        
        # Complete the entry
        self.current_entry.end_time = datetime.now()
        self.current_entry.user_notes = user_notes
        self.current_entry.energy_level = energy_level
        self.current_entry.focus_quality = focus_quality
        self.current_entry.interruptions = interruptions
        
        # Update estimation accuracy if user provided estimate
        duration = self.current_entry.duration_minutes()
        if duration and "Estimated:" in self.current_entry.user_notes:
            try:
                estimated = int(self.current_entry.user_notes.split("Estimated: ")[1].split(" ")[0])
                self.estimation_history.append((estimated, duration))
            except (ValueError, IndexError):
                pass  # Graceful failure handling
        
        completed_entry = self.current_entry
        self.current_entry = None
        return completed_entry
    
    def add_manual_entry(self, start_time: datetime, duration_minutes: int,
                        task_description: str, category: str = "work",
                        confidence: ConfidenceLevel = ConfidenceLevel.LOW) -> TimeEntry:
        """
        Add manual time entry with lower confidence (honest about limitations)
        
        Args:
            start_time: When the task started
            duration_minutes: How long it took
            task_description: What was done
            category: Task category
            confidence: Confidence level (default LOW for manual entries)
        
        Returns:
            TimeEntry: The created manual entry
        """
        entry = TimeEntry(
            start_time=start_time,
            end_time=start_time + timedelta(minutes=duration_minutes),
            task_description=task_description,
            category=category,
            confidence=confidence  # Honest about manual entry limitations
        )
        
        self.entries.append(entry)
        return entry
    
    def get_current_session(self) -> Optional[Dict]:
        """Get current active session with honest uncertainty"""
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
        """
        Get daily summary with honest limitations acknowledgment
        
        Args:
            date: Date to summarize (defaults to today)
        
        Returns:
            Dict: Summary with confidence indicators
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
                "categories": {},
                "confidence": "no_data",
                "limitations": "No time tracking data available for this date"
            }
        
        # Calculate summary
        total_minutes = sum(entry.duration_minutes() or 0 for entry in day_entries)
        categories = {}
        confidence_levels = []
        
        for entry in day_entries:
            if entry.category not in categories:
                categories[entry.category] = 0
            categories[entry.category] += entry.duration_minutes() or 0
            confidence_levels.append(entry.confidence.value)
        
        # Assess overall confidence
        high_confidence_count = confidence_levels.count(ConfidenceLevel.HIGH.value)
        overall_confidence = ConfidenceLevel.HIGH.value if high_confidence_count > len(confidence_levels) * 0.7 else ConfidenceLevel.MODERATE.value
        
        return {
            "date": date.isoformat(),
            "total_minutes": total_minutes,
            "entries_count": len(day_entries),
            "categories": categories,
            "confidence": overall_confidence,
            "limitations": "Data based on user input and may include estimation errors",
            "average_energy": sum(e.energy_level for e in day_entries) / len(day_entries),
            "average_focus": sum(e.focus_quality for e in day_entries) / len(day_entries),
            "total_interruptions": sum(e.interruptions for e in day_entries)
        }
    
    def get_estimation_accuracy(self) -> Dict:
        """
        Calculate user's time estimation accuracy with honest assessment
        
        Returns:
            Dict: Estimation accuracy with limitations noted
        """
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
    
    def add_category(self, category: str) -> bool:
        """Add custom category with user control"""
        if category not in self.categories:
            self.categories.append(category)
            return True
        return False
    
    def export_data(self) -> Dict:
        """
        Export all data with full user control
        
        Returns:
            Dict: Complete exportable data
        """
        return {
            "user_id": self.user_id,
            "export_date": datetime.now().isoformat(),
            "entries": [entry.to_dict() for entry in self.entries],
            "categories": self.categories,
            "estimation_history": self.estimation_history,
            "data_integrity": {
                "total_entries": len(self.entries),
                "complete_entries": len([e for e in self.entries if e.is_complete()]),
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
        """
        Clear all data with user control (for privacy)
        
        Returns:
            bool: True if successful
        """
        self.entries.clear()
        self.current_entry = None
        self.estimation_history.clear()
        return True


# Example usage and testing
if __name__ == "__main__":
    # Create tracker
    tracker = TimeTracker("user_123")
    
    # Start a work session
    tracker.start_timer("Writing FlowState documentation", "work", estimated_minutes=60)
    
    # Simulate some work time
    time.sleep(2)  # In real use, this would be actual work time
    
    # Stop with user feedback
    tracker.stop_timer(
        user_notes="Good focus session, completed task outline",
        energy_level=4,
        focus_quality=4,
        interruptions=1
    )
    
    # Get summary
    summary = tracker.get_daily_summary()
    print("Daily Summary:", json.dumps(summary, indent=2))
    
    # Check estimation accuracy
    accuracy = tracker.get_estimation_accuracy()
    print("Estimation Accuracy:", json.dumps(accuracy, indent=2))

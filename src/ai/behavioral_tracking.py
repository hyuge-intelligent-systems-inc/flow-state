
"""
FlowState Behavioral Tracking Module
Privacy-First Behavioral Analysis with User Agency

This module tracks user behavior patterns while maintaining strict privacy controls
and user agency. All tracking is transparent, user-controlled, and locally processed.

Core Principles:
- User agency preserved - users control what is tracked and how
- Privacy-first - all data processed locally with user consent
- Transparent tracking - users see exactly what is being monitored
- Honest limitations - clear about what can and cannot be inferred
- Professional boundaries - behavioral insights, not psychological diagnosis
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import sqlite3
from pathlib import Path


class TrackingLevel(Enum):
    """User-controlled tracking granularity levels"""
    MINIMAL = "minimal"      # Basic time tracking only
    STANDARD = "standard"    # Time + basic app usage patterns
    DETAILED = "detailed"    # Standard + environmental context
    COMPREHENSIVE = "comprehensive"  # All available data with user consent


class BehaviorCategory(Enum):
    """Categories of trackable behavior patterns"""
    WORK_SESSIONS = "work_sessions"
    BREAK_PATTERNS = "break_patterns"
    APP_USAGE = "app_usage"
    FOCUS_INDICATORS = "focus_indicators"
    ENVIRONMENT_CONTEXT = "environment_context"
    PRODUCTIVITY_RHYTHMS = "productivity_rhythms"


@dataclass
class BehaviorEvent:
    """Single behavioral observation with metadata"""
    timestamp: datetime
    event_type: str
    category: BehaviorCategory
    data: Dict[str, Any]
    confidence: float
    user_verified: Optional[bool] = None
    privacy_level: TrackingLevel = TrackingLevel.STANDARD
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'category': self.category.value,
            'data': self.data,
            'confidence': self.confidence,
            'user_verified': self.user_verified,
            'privacy_level': self.privacy_level.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BehaviorEvent':
        """Create from dictionary"""
        return cls(
            timestamp=datetime.fromisoformat(data['timestamp']),
            event_type=data['event_type'],
            category=BehaviorCategory(data['category']),
            data=data['data'],
            confidence=data['confidence'],
            user_verified=data.get('user_verified'),
            privacy_level=TrackingLevel(data.get('privacy_level', 'standard'))
        )


@dataclass
class BehaviorPattern:
    """Identified pattern in user behavior"""
    pattern_id: str
    name: str
    description: str
    confidence: float
    evidence_events: List[str]  # Event IDs supporting this pattern
    created_at: datetime
    last_updated: datetime
    user_feedback: Optional[str] = None
    accuracy_rating: Optional[float] = None


class BehaviorTracker:
    """
    Privacy-first behavioral tracking with user agency
    
    Tracks user behavior patterns while maintaining complete user control
    over what is tracked, how it's processed, and who can access insights.
    """
    
    def __init__(self, data_dir: str, user_preferences: Dict[str, Any]):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # User-controlled preferences
        self.tracking_level = TrackingLevel(
            user_preferences.get('tracking_level', 'standard')
        )
        self.enabled_categories = set(
            BehaviorCategory(cat) for cat in 
            user_preferences.get('enabled_categories', ['work_sessions', 'break_patterns'])
        )
        self.data_retention_days = user_preferences.get('data_retention_days', 90)
        self.require_user_verification = user_preferences.get('require_verification', True)
        
        # Initialize storage
        self.db_path = self.data_dir / 'behavior_tracking.db'
        self._initialize_database()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Privacy controls
        self.anonymization_enabled = user_preferences.get('anonymization', True)
        self.local_processing_only = user_preferences.get('local_only', True)
        
    def _initialize_database(self):
        """Initialize SQLite database for behavior storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS behavior_events (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                category TEXT NOT NULL,
                data TEXT NOT NULL,
                confidence REAL NOT NULL,
                user_verified INTEGER,
                privacy_level TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS behavior_patterns (
                pattern_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                confidence REAL NOT NULL,
                evidence_events TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                user_feedback TEXT,
                accuracy_rating REAL
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracking_preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_work_session(self, session_data: Dict[str, Any]) -> Optional[str]:
        """
        Track a work session with user agency
        
        Args:
            session_data: Dict containing session information
            
        Returns:
            Event ID if tracked, None if user declined or not enabled
        """
        if BehaviorCategory.WORK_SESSIONS not in self.enabled_categories:
            return None
        
        # Ask for user consent if required
        if self.require_user_verification:
            consent = self._get_user_consent(
                "Track this work session for productivity insights?",
                session_data
            )
            if not consent:
                return None
        
        # Create anonymized session data based on privacy level
        tracked_data = self._anonymize_session_data(session_data)
        
        event = BehaviorEvent(
            timestamp=datetime.now(),
            event_type="work_session_completed",
            category=BehaviorCategory.WORK_SESSIONS,
            data=tracked_data,
            confidence=0.9,  # High confidence for explicit user actions
            privacy_level=self.tracking_level
        )
        
        return self._store_event(event)
    
    def track_app_usage(self, app_data: Dict[str, Any]) -> Optional[str]:
        """
        Track application usage patterns with privacy protection
        
        Args:
            app_data: Application usage information
            
        Returns:
            Event ID if tracked, None if disabled
        """
        if BehaviorCategory.APP_USAGE not in self.enabled_categories:
            return None
        
        # Hash application names for privacy
        if self.anonymization_enabled:
            app_data = self._anonymize_app_data(app_data)
        
        event = BehaviorEvent(
            timestamp=datetime.now(),
            event_type="app_usage_detected",
            category=BehaviorCategory.APP_USAGE,
            data=app_data,
            confidence=0.8,  # Good confidence for automated detection
            privacy_level=self.tracking_level
        )
        
        return self._store_event(event)
    
    def track_break_pattern(self, break_data: Dict[str, Any]) -> Optional[str]:
        """
        Track break patterns for productivity insights
        
        Args:
            break_data: Break timing and context information
            
        Returns:
            Event ID if tracked
        """
        if BehaviorCategory.BREAK_PATTERNS not in self.enabled_categories:
            return None
        
        event = BehaviorEvent(
            timestamp=datetime.now(),
            event_type="break_detected",
            category=BehaviorCategory.BREAK_PATTERNS,
            data=break_data,
            confidence=0.7,  # Moderate confidence for inferred breaks
            privacy_level=self.tracking_level
        )
        
        return self._store_event(event)
    
    def track_focus_indicator(self, focus_data: Dict[str, Any]) -> Optional[str]:
        """
        Track focus state indicators with uncertainty disclosure
        
        Args:
            focus_data: Focus state indicators and confidence
            
        Returns:
            Event ID if tracked
        """
        if BehaviorCategory.FOCUS_INDICATORS not in self.enabled_categories:
            return None
        
        # Focus detection has inherent uncertainty - be honest about it
        confidence = min(focus_data.get('confidence', 0.5), 0.6)  # Cap at 60%
        
        event = BehaviorEvent(
            timestamp=datetime.now(),
            event_type="focus_state_inferred",
            category=BehaviorCategory.FOCUS_INDICATORS,
            data={
                **focus_data,
                'uncertainty_note': 'Focus detection is approximate and may not reflect actual mental state'
            },
            confidence=confidence,
            privacy_level=self.tracking_level
        )
        
        return self._store_event(event)
    
    def _anonymize_session_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize session data based on privacy level"""
        if self.tracking_level == TrackingLevel.MINIMAL:
            return {
                'duration_minutes': session_data.get('duration_minutes'),
                'session_type': 'work'  # Generic type only
            }
        
        elif self.tracking_level == TrackingLevel.STANDARD:
            return {
                'duration_minutes': session_data.get('duration_minutes'),
                'category_hash': self._hash_sensitive_data(
                    session_data.get('category', 'unknown')
                ),
                'productivity_rating': session_data.get('productivity_rating')
            }
        
        else:  # DETAILED or COMPREHENSIVE
            anonymized = session_data.copy()
            
            # Hash sensitive text data
            if 'description' in anonymized:
                anonymized['description_hash'] = self._hash_sensitive_data(
                    anonymized.pop('description')
                )
            
            if 'project_name' in anonymized:
                anonymized['project_hash'] = self._hash_sensitive_data(
                    anonymized.pop('project_name')
                )
            
            return anonymized
    
    def _anonymize_app_data(self, app_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize application data for privacy"""
        anonymized = app_data.copy()
        
        # Hash application names
        if 'app_name' in anonymized:
            anonymized['app_hash'] = self._hash_sensitive_data(
                anonymized.pop('app_name')
            )
        
        # Remove window titles and file paths
        anonymized.pop('window_title', None)
        anonymized.pop('file_path', None)
        
        # Keep only usage duration and category
        return {
            'app_hash': anonymized.get('app_hash'),
            'usage_duration': anonymized.get('usage_duration'),
            'app_category': anonymized.get('app_category', 'unknown')
        }
    
    def _hash_sensitive_data(self, data: str) -> str:
        """Create privacy-preserving hash of sensitive data"""
        if not data:
            return "empty"
        
        # Use SHA-256 with salt for privacy
        salt = "flowstate_privacy_salt_2024"
        return hashlib.sha256(f"{salt}{data}".encode()).hexdigest()[:16]
    
    def _get_user_consent(self, message: str, data: Dict[str, Any]) -> bool:
        """
        Get user consent for tracking (placeholder for UI integration)
        
        In production, this would integrate with the UI system to show
        a consent dialog with details about what will be tracked.
        """
        # For now, respect user preferences
        return not self.require_user_verification
    
    def _store_event(self, event: BehaviorEvent) -> str:
        """Store behavior event in local database"""
        event_id = hashlib.sha256(
            f"{event.timestamp.isoformat()}{event.event_type}".encode()
        ).hexdigest()[:16]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO behavior_events 
            (id, timestamp, event_type, category, data, confidence, 
             user_verified, privacy_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_id,
            event.timestamp.isoformat(),
            event.event_type,
            event.category.value,
            json.dumps(event.data),
            event.confidence,
            event.user_verified,
            event.privacy_level.value
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Stored behavior event: {event.event_type} ({event_id})")
        return event_id
    
    def get_behavior_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Get behavior summary with user-controlled privacy
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Privacy-respecting behavior summary
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count, AVG(confidence) as avg_confidence
            FROM behavior_events 
            WHERE timestamp > ?
            GROUP BY category
        ''', (cutoff_date.isoformat(),))
        
        results = cursor.fetchall()
        conn.close()
        
        summary = {
            'period_days': days,
            'categories': {
                category: {
                    'event_count': count,
                    'average_confidence': round(avg_confidence, 2),
                    'data_quality': self._assess_data_quality(avg_confidence)
                }
                for category, count, avg_confidence in results
            },
            'privacy_level': self.tracking_level.value,
            'user_control_note': 'All tracking is user-controlled and can be disabled at any time'
        }
        
        return summary
    
    def _assess_data_quality(self, confidence: float) -> str:
        """Assess and communicate data quality honestly"""
        if confidence >= 0.8:
            return "High confidence - reliable patterns"
        elif confidence >= 0.6:
            return "Moderate confidence - likely patterns"
        elif confidence >= 0.4:
            return "Low confidence - uncertain patterns"
        else:
            return "Very low confidence - patterns may not be meaningful"
    
    def get_user_verification_requests(self) -> List[Dict[str, Any]]:
        """Get events that need user verification"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, event_type, data, confidence
            FROM behavior_events 
            WHERE user_verified IS NULL
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'event_id': event_id,
                'timestamp': timestamp,
                'event_type': event_type,
                'summary': self._create_event_summary(json.loads(data)),
                'confidence': confidence,
                'verification_note': 'Help improve pattern accuracy by confirming this observation'
            }
            for event_id, timestamp, event_type, data, confidence in results
        ]
    
    def _create_event_summary(self, data: Dict[str, Any]) -> str:
        """Create privacy-respecting event summary for user verification"""
        if 'duration_minutes' in data:
            return f"Work session: {data['duration_minutes']} minutes"
        elif 'app_category' in data:
            return f"App usage: {data['app_category']} category"
        elif 'break_duration' in data:
            return f"Break detected: {data['break_duration']} minutes"
        else:
            return "Activity detected"
    
    def verify_event(self, event_id: str, is_accurate: bool, feedback: str = "") -> bool:
        """Allow user to verify or correct event detection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE behavior_events 
            SET user_verified = ?, 
                data = json_set(data, '$.user_feedback', ?)
            WHERE id = ?
        ''', (is_accurate, feedback, event_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            self.logger.info(f"Event {event_id} verified by user: {is_accurate}")
        
        return success
    
    def update_tracking_preferences(self, new_preferences: Dict[str, Any]) -> bool:
        """Update user tracking preferences with validation"""
        try:
            # Validate new preferences
            if 'tracking_level' in new_preferences:
                self.tracking_level = TrackingLevel(new_preferences['tracking_level'])
            
            if 'enabled_categories' in new_preferences:
                self.enabled_categories = set(
                    BehaviorCategory(cat) for cat in new_preferences['enabled_categories']
                )
            
            if 'data_retention_days' in new_preferences:
                retention = new_preferences['data_retention_days']
                if 1 <= retention <= 365:  # Reasonable bounds
                    self.data_retention_days = retention
            
            # Store preferences
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for key, value in new_preferences.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO tracking_preferences (key, value)
                    VALUES (?, ?)
                ''', (key, json.dumps(value)))
            
            conn.commit()
            conn.close()
            
            self.logger.info("Tracking preferences updated by user")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update preferences: {e}")
            return False
    
    def export_behavior_data(self) -> Dict[str, Any]:
        """Export all behavior data for user portability"""
        conn = sqlite3.connect(self.db_path)
        
        # Export events
        events_df = conn.execute('''
            SELECT * FROM behavior_events 
            ORDER BY timestamp DESC
        ''').fetchall()
        
        # Export patterns
        patterns_df = conn.execute('''
            SELECT * FROM behavior_patterns 
            ORDER BY created_at DESC
        ''').fetchall()
        
        # Export preferences
        preferences_df = conn.execute('''
            SELECT * FROM tracking_preferences
        ''').fetchall()
        
        conn.close()
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'export_type': 'complete_behavior_data',
            'privacy_level': self.tracking_level.value,
            'data_ownership_statement': 'This data belongs to you. You can delete it at any time.',
            'events': [dict(zip(['id', 'timestamp', 'event_type', 'category', 'data', 
                                'confidence', 'user_verified', 'privacy_level', 'created_at'], 
                               row)) for row in events_df],
            'patterns': [dict(zip(['pattern_id', 'name', 'description', 'confidence',
                                  'evidence_events', 'created_at', 'last_updated',
                                  'user_feedback', 'accuracy_rating'], 
                                 row)) for row in patterns_df],
            'preferences': [dict(zip(['key', 'value', 'updated_at'], row)) 
                           for row in preferences_df],
            'usage_instructions': {
                'data_format': 'JSON with SQLite schema',
                'privacy_notes': 'Sensitive data has been hashed for privacy',
                'deletion_instructions': 'Delete the behavior_tracking.db file to remove all data'
            }
        }
        
        return export_data
    
    def delete_all_data(self, confirmation_phrase: str) -> bool:
        """
        Delete all behavior tracking data (requires confirmation)
        
        Args:
            confirmation_phrase: Must match exactly for safety
            
        Returns:
            True if data deleted successfully
        """
        expected_phrase = "DELETE ALL MY BEHAVIOR DATA"
        
        if confirmation_phrase != expected_phrase:
            self.logger.warning("Data deletion attempted with incorrect confirmation phrase")
            return False
        
        try:
            # Delete database file
            if self.db_path.exists():
                self.db_path.unlink()
            
            # Clear in-memory state
            self.enabled_categories.clear()
            
            self.logger.info("All behavior tracking data deleted by user request")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete behavior data: {e}")
            return False
    
    def cleanup_old_data(self):
        """Clean up data older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.data_retention_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM behavior_events 
            WHERE timestamp < ?
        ''', (cutoff_date.isoformat(),))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            self.logger.info(f"Cleaned up {deleted_count} old behavior events")
        
        return deleted_count


# Example usage and testing
if __name__ == "__main__":
    # Example usage with privacy-first configuration
    user_prefs = {
        'tracking_level': 'standard',
        'enabled_categories': ['work_sessions', 'break_patterns'],
        'data_retention_days': 90,
        'require_verification': True,
        'anonymization': True,
        'local_only': True
    }
    
    tracker = BehaviorTracker('./data', user_prefs)
    
    # Track a work session
    session_data = {
        'duration_minutes': 45,
        'category': 'coding',
        'productivity_rating': 4
    }
    event_id = tracker.track_work_session(session_data)
    print(f"Tracked work session: {event_id}")
    
    # Get behavior summary
    summary = tracker.get_behavior_summary(days=7)
    print(f"Behavior summary: {summary}")
    
    # Export data for user
    export = tracker.export_behavior_data()
    print(f"Data export contains {len(export['events'])} events")


"""
FlowState Calendar Sync Integration
Privacy-first calendar integration with user-controlled data sharing

Key principles implemented:
- User controls all calendar data access and interpretation
- Privacy-preserving integration with explicit permissions
- Honest limitations about what calendar data can/cannot reveal
- Individual agency over calendar-productivity correlations
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
from abc import ABC, abstractmethod


class CalendarProvider(Enum):
    """Supported calendar providers"""
    GOOGLE = "google"
    OUTLOOK = "outlook"
    APPLE = "apple"
    CALDAV = "caldav"
    MANUAL = "manual"  # User manually adds events


class EventType(Enum):
    """Calendar event types for productivity analysis"""
    FOCUS_WORK = "focus_work"
    MEETING = "meeting"
    BREAK = "break"
    PERSONAL = "personal"
    COMMUTE = "commute"
    BUFFER = "buffer"
    UNKNOWN = "unknown"


class IntegrationPermission(Enum):
    """Granular calendar integration permissions"""
    READ_EVENTS = "read_events"
    READ_AVAILABILITY = "read_availability"
    CREATE_FOCUS_BLOCKS = "create_focus_blocks"
    UPDATE_EVENT_STATUS = "update_event_status"
    ANALYZE_PATTERNS = "analyze_patterns"


@dataclass
class CalendarEvent:
    """Privacy-preserving calendar event representation"""
    event_id: str
    start_time: datetime
    end_time: datetime
    event_type: EventType
    title_hash: Optional[str] = None  # Hashed for privacy
    is_focus_time: bool = False
    is_user_controlled: bool = True
    attendee_count: Optional[int] = None  # Number only, no names
    location_type: Optional[str] = None  # "office", "home", "remote", etc.
    user_energy_before: Optional[int] = None  # 1-5 scale, user-reported
    user_energy_after: Optional[int] = None   # 1-5 scale, user-reported
    productivity_rating: Optional[int] = None  # 1-5 scale, user-reported
    user_notes: Optional[str] = None


@dataclass
class CalendarIntegrationSettings:
    """User-controlled calendar integration preferences"""
    # Provider settings
    enabled_providers: List[CalendarProvider]
    primary_provider: Optional[CalendarProvider]
    
    # Permission controls
    granted_permissions: List[IntegrationPermission]
    
    # Privacy controls
    hash_event_titles: bool = True
    exclude_personal_events: bool = True
    share_meeting_patterns: bool = False
    share_focus_patterns: bool = False
    
    # Analysis preferences
    enable_productivity_correlation: bool = False
    enable_energy_tracking: bool = False
    enable_pattern_suggestions: bool = False
    
    # Sync preferences
    sync_frequency_hours: int = 1
    look_ahead_days: int = 7
    look_back_days: int = 30
    
    # Focus time management
    auto_create_focus_blocks: bool = False
    protect_existing_focus_time: bool = True
    min_focus_block_minutes: int = 25
    max_daily_focus_blocks: int = 4


class CalendarProvider_Interface(ABC):
    """Abstract interface for calendar providers"""
    
    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with calendar provider"""
        pass
    
    @abstractmethod
    def get_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Retrieve events from calendar provider"""
        pass
    
    @abstractmethod
    def create_event(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Create event in calendar provider"""
        pass
    
    @abstractmethod
    def update_event(self, event_id: str, event_data: Dict[str, Any]) -> bool:
        """Update existing event in calendar provider"""
        pass


class PrivacyPreservingCalendarSync:
    """
    Privacy-first calendar integration that respects user agency
    """
    
    def __init__(self, user_profile, integration_settings: CalendarIntegrationSettings):
        self.user_profile = user_profile
        self.settings = integration_settings
        self.providers: Dict[CalendarProvider, CalendarProvider_Interface] = {}
        self.cached_events: List[CalendarEvent] = []
        self.last_sync: Optional[datetime] = None
        self.sync_history: List[Dict[str, Any]] = []
        
        # Privacy-preserving storage
        self.user_event_annotations = {}  # User-added context
        self.productivity_correlations = {}  # User-discovered patterns
        
    def add_provider(self, provider_type: CalendarProvider, provider_instance: CalendarProvider_Interface) -> None:
        """Add calendar provider with user consent"""
        if provider_type in self.settings.enabled_providers:
            self.providers[provider_type] = provider_instance
    
    def sync_calendar_data(self, force_sync: bool = False) -> Dict[str, Any]:
        """
        Sync calendar data with full user control and transparency
        """
        if not self._should_sync() and not force_sync:
            return {
                'status': 'skipped',
                'reason': 'sync_not_needed',
                'last_sync': self.last_sync.isoformat() if self.last_sync else None
            }
        
        if not self.settings.granted_permissions:
            return {
                'status': 'error',
                'reason': 'no_permissions_granted',
                'message': 'User has not granted calendar access permissions'
            }
        
        sync_results = {
            'status': 'success',
            'events_processed': 0,
            'privacy_preserving': True,
            'user_control_maintained': True,
            'sync_timestamp': datetime.now().isoformat(),
            'provider_results': {}
        }
        
        # Sync from each enabled provider
        for provider_type in self.settings.enabled_providers:
            if provider_type in self.providers:
                try:
                    provider_result = self._sync_from_provider(provider_type)
                    sync_results['provider_results'][provider_type.value] = provider_result
                    sync_results['events_processed'] += provider_result.get('events_count', 0)
                except Exception as e:
                    sync_results['provider_results'][provider_type.value] = {
                        'status': 'error',
                        'error': str(e),
                        'events_count': 0
                    }
        
        self.last_sync = datetime.now()
        self._log_sync_history(sync_results)
        
        return sync_results
    
    def _sync_from_provider(self, provider_type: CalendarProvider) -> Dict[str, Any]:
        """Sync events from specific provider with privacy preservation"""
        provider = self.providers[provider_type]
        
        # Calculate sync window
        end_date = datetime.now() + timedelta(days=self.settings.look_ahead_days)
        start_date = datetime.now() - timedelta(days=self.settings.look_back_days)
        
        # Get raw events
        raw_events = provider.get_events(start_date, end_date)
        
        # Process events with privacy preservation
        processed_events = []
        for raw_event in raw_events:
            processed_event = self._process_event_with_privacy(raw_event, provider_type)
            if processed_event:  # None if filtered out for privacy
                processed_events.append(processed_event)
        
        # Update cached events
        self._update_cached_events(processed_events, provider_type)
        
        return {
            'status': 'success',
            'provider': provider_type.value,
            'events_count': len(processed_events),
            'privacy_filters_applied': True,
            'user_controlled': True
        }
    
    def _process_event_with_privacy(self, raw_event: Dict[str, Any], provider: CalendarProvider) -> Optional[CalendarEvent]:
        """
        Process calendar event with privacy-preserving techniques
        """
        # Skip personal events if user preference set
        if self.settings.exclude_personal_events and self._is_personal_event(raw_event):
            return None
        
        # Create privacy-preserving event representation
        event = CalendarEvent(
            event_id=raw_event.get('id', str(uuid.uuid4())),
            start_time=self._parse_datetime(raw_event.get('start')),
            end_time=self._parse_datetime(raw_event.get('end')),
            event_type=self._classify_event_type(raw_event),
            title_hash=self._hash_title(raw_event.get('title', '')) if self.settings.hash_event_titles else None,
            attendee_count=len(raw_event.get('attendees', [])) if raw_event.get('attendees') else None,
            location_type=self._classify_location_type(raw_event.get('location', '')),
            is_user_controlled=True  # User can always modify classification
        )
        
        return event
    
    def get_focus_time_suggestions(self) -> List[Dict[str, Any]]:
        """
        Suggest focus time blocks based on calendar gaps and user patterns
        """
        if IntegrationPermission.ANALYZE_PATTERNS not in self.settings.granted_permissions:
            return []
        
        suggestions = []
        now = datetime.now()
        
        # Look for gaps in calendar over next week
        for day_offset in range(7):
            day = now.date() + timedelta(days=day_offset)
            day_suggestions = self._find_focus_opportunities(day)
            suggestions.extend(day_suggestions)
        
        # Limit and prioritize suggestions
        suggestions = sorted(suggestions, key=lambda x: x['confidence_score'], reverse=True)
        return suggestions[:self.settings.max_daily_focus_blocks]
    
    def _find_focus_opportunities(self, target_date) -> List[Dict[str, Any]]:
        """Find potential focus time opportunities for a specific day"""
        day_start = datetime.combine(target_date, datetime.min.time().replace(hour=8))
        day_end = datetime.combine(target_date, datetime.min.time().replace(hour=18))
        
        # Get events for the day
        day_events = [e for e in self.cached_events 
                     if day_start <= e.start_time <= day_end]
        
        # Sort events by start time
        day_events.sort(key=lambda x: x.start_time)
        
        # Find gaps between events
        opportunities = []
        current_time = day_start
        
        for event in day_events:
            gap_duration = (event.start_time - current_time).total_seconds() / 60
            
            if gap_duration >= self.settings.min_focus_block_minutes:
                # Calculate confidence based on historical patterns
                confidence = self._calculate_focus_confidence(current_time, gap_duration)
                
                opportunities.append({
                    'start_time': current_time.isoformat(),
                    'duration_minutes': int(gap_duration),
                    'confidence_score': confidence,
                    'reasoning': self._generate_focus_reasoning(current_time, gap_duration),
                    'user_customizable': True,
                    'automatically_created': False  # Requires user approval
                })
            
            current_time = event.end_time
        
        return opportunities
    
    def create_focus_block(self, start_time: datetime, duration_minutes: int, user_approved: bool = True) -> Dict[str, Any]:
        """
        Create focus time block with user approval
        """
        if not user_approved:
            return {
                'status': 'error',
                'message': 'Focus blocks require explicit user approval'
            }
        
        if IntegrationPermission.CREATE_FOCUS_BLOCKS not in self.settings.granted_permissions:
            return {
                'status': 'error',
                'message': 'User has not granted permission to create calendar events'
            }
        
        # Create focus event
        focus_event = {
            'title': 'Focus Time (FlowState)',
            'start': start_time.isoformat(),
            'end': (start_time + timedelta(minutes=duration_minutes)).isoformat(),
            'description': 'Protected focus time created by FlowState',
            'busy': True,
            'private': True
        }
        
        # Try to create in primary calendar provider
        if self.settings.primary_provider in self.providers:
            provider = self.providers[self.settings.primary_provider]
            event_id = provider.create_event(focus_event)
            
            if event_id:
                return {
                    'status': 'success',
                    'event_id': event_id,
                    'provider': self.settings.primary_provider.value,
                    'user_approved': True
                }
        
        return {
            'status': 'error',
            'message': 'Failed to create focus block in calendar'
        }
    
    def add_user_event_annotation(self, event_id: str, annotation: Dict[str, Any]) -> None:
        """
        Allow user to add context and insights to calendar events
        """
        if event_id not in self.user_event_annotations:
            self.user_event_annotations[event_id] = []
        
        annotation_entry = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'annotation': annotation,
            'user_controlled': True
        }
        
        self.user_event_annotations[event_id].append(annotation_entry)
    
    def discover_productivity_pattern(self, pattern_description: str, supporting_events: List[str]) -> None:
        """
        User-discovered productivity patterns related to calendar events
        """
        pattern_id = str(uuid.uuid4())
        self.productivity_correlations[pattern_id] = {
            'pattern': pattern_description,
            'supporting_events': supporting_events,
            'discovered_by_user': True,
            'discovery_date': datetime.now().isoformat(),
            'confidence': 'user_determined',  # User decides confidence level
            'actionable_insights': []  # User adds their own insights
        }
    
    def get_calendar_productivity_insights(self) -> Dict[str, Any]:
        """
        Provide calendar-productivity insights with honest limitations
        """
        if not self.settings.enable_productivity_correlation:
            return {
                'status': 'disabled',
                'message': 'Calendar-productivity correlation analysis is disabled by user preference'
            }
        
        insights = {
            'data_source': 'user_calendar_events',
            'analysis_limitations': [
                'Correlation does not imply causation',
                'Calendar events may not reflect actual productivity',
                'Personal and emotional factors not captured',
                'Sample size may be insufficient for reliable patterns'
            ],
            'user_interpretation_required': True,
            'privacy_preserving': True,
            'insights': []
        }
        
        # Basic pattern observations (not conclusions)
        if len(self.cached_events) >= 30:  # Minimum sample size
            insights['insights'].extend([
                self._analyze_meeting_density_patterns(),
                self._analyze_focus_time_effectiveness(),
                self._analyze_energy_calendar_correlations()
            ])
        else:
            insights['insufficient_data'] = {
                'current_events': len(self.cached_events),
                'minimum_needed': 30,
                'message': 'More calendar data needed for pattern analysis'
            }
        
        return insights
    
    def _analyze_meeting_density_patterns(self) -> Dict[str, Any]:
        """Analyze meeting density patterns with user interpretation required"""
        meeting_events = [e for e in self.cached_events if e.event_type == EventType.MEETING]
        
        # Calculate basic statistics
        daily_meeting_counts = {}
        for event in meeting_events:
            day = event.start_time.date()
            daily_meeting_counts[day] = daily_meeting_counts.get(day, 0) + 1
        
        avg_meetings_per_day = sum(daily_meeting_counts.values()) / len(daily_meeting_counts) if daily_meeting_counts else 0
        
        return {
            'observation_type': 'meeting_density',
            'data': {
                'average_meetings_per_day': round(avg_meetings_per_day, 1),
                'total_meeting_days': len(daily_meeting_counts),
                'highest_meeting_day_count': max(daily_meeting_counts.values()) if daily_meeting_counts else 0
            },
            'user_interpretation_needed': True,
            'questions_for_reflection': [
                'Do you feel more or less productive on high-meeting days?',
                'What is your ideal number of meetings per day?',
                'How do meetings affect your energy levels?'
            ],
            'limitations': 'This only shows meeting frequency, not meeting quality or necessity'
        }
    
    def _analyze_focus_time_effectiveness(self) -> Dict[str, Any]:
        """Analyze focus time patterns with user context required"""
        focus_events = [e for e in self.cached_events if e.event_type == EventType.FOCUS_WORK]
        
        if not focus_events:
            return {
                'observation_type': 'focus_time',
                'message': 'No dedicated focus time blocks found in calendar',
                'suggestion': 'Consider scheduling explicit focus time blocks'
            }
        
        # Basic focus time statistics
        total_focus_hours = sum((e.end_time - e.start_time).total_seconds() / 3600 for e in focus_events)
        avg_focus_block_duration = total_focus_hours / len(focus_events) * 60  # in minutes
        
        return {
            'observation_type': 'focus_time_patterns',
            'data': {
                'total_focus_blocks': len(focus_events),
                'total_focus_hours': round(total_focus_hours, 1),
                'average_block_duration_minutes': round(avg_focus_block_duration, 0)
            },
            'user_interpretation_needed': True,
            'questions_for_reflection': [
                'Which focus blocks were most productive for you?',
                'What duration works best for your focus sessions?',
                'What time of day do you focus best?'
            ],
            'limitations': 'Calendar blocks do not measure actual focus quality or output'
        }
    
    def _analyze_energy_calendar_correlations(self) -> Dict[str, Any]:
        """Analyze energy-calendar correlations if user tracks energy"""
        energy_tracked_events = [e for e in self.cached_events 
                               if e.user_energy_before is not None or e.user_energy_after is not None]
        
        if len(energy_tracked_events) < 10:
            return {
                'observation_type': 'energy_calendar_correlation',
                'message': 'Insufficient energy tracking data for correlation analysis',
                'suggestion': 'Consider tracking energy before/after calendar events'
            }
        
        # This would contain energy correlation analysis
        return {
            'observation_type': 'energy_calendar_correlation',
            'data': 'Energy correlation analysis would go here',
            'user_interpretation_needed': True,
            'limitations': 'Energy levels affected by many factors beyond calendar events'
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Provide transparent status of calendar integration"""
        return {
            'integration_status': {
                'enabled_providers': [p.value for p in self.settings.enabled_providers],
                'granted_permissions': [p.value for p in self.settings.granted_permissions],
                'last_sync': self.last_sync.isoformat() if self.last_sync else None,
                'cached_events_count': len(self.cached_events)
            },
            'privacy_settings': {
                'hash_event_titles': self.settings.hash_event_titles,
                'exclude_personal_events': self.settings.exclude_personal_events,
                'share_meeting_patterns': self.settings.share_meeting_patterns,
                'enable_productivity_correlation': self.settings.enable_productivity_correlation
            },
            'user_control': {
                'can_disable_integration': True,
                'can_modify_permissions': True,
                'can_export_all_data': True,
                'can_delete_all_data': True
            },
            'data_ownership': 'You own all calendar integration data and can control it completely'
        }
    
    def export_calendar_integration_data(self) -> Dict[str, Any]:
        """Export all calendar integration data for user"""
        return {
            'calendar_integration_data': {
                'settings': {
                    'enabled_providers': [p.value for p in self.settings.enabled_providers],
                    'granted_permissions': [p.value for p in self.settings.granted_permissions],
                    'privacy_controls': {
                        'hash_event_titles': self.settings.hash_event_titles,
                        'exclude_personal_events': self.settings.exclude_personal_events,
                        'share_meeting_patterns': self.settings.share_meeting_patterns,
                        'enable_productivity_correlation': self.settings.enable_productivity_correlation
                    }
                },
                'cached_events': [
                    {
                        'event_id': e.event_id,
                        'start_time': e.start_time.isoformat(),
                        'end_time': e.end_time.isoformat(),
                        'event_type': e.event_type.value,
                        'user_annotations': self.user_event_annotations.get(e.event_id, [])
                    }
                    for e in self.cached_events
                ],
                'user_discoveries': self.productivity_correlations,
                'sync_history': self.sync_history
            },
            'export_metadata': {
                'export_date': datetime.now().isoformat(),
                'privacy_preserved': True,
                'user_owned': True
            }
        }
    
    # Helper methods
    def _should_sync(self) -> bool:
        """Determine if sync is needed based on user preferences"""
        if not self.last_sync:
            return True
        
        hours_since_sync = (datetime.now() - self.last_sync).total_seconds() / 3600
        return hours_since_sync >= self.settings.sync_frequency_hours
    
    def _is_personal_event(self, raw_event: Dict[str, Any]) -> bool:
        """Classify if event is personal (basic heuristics)"""
        title = raw_event.get('title', '').lower()
        personal_keywords = ['personal', 'family', 'doctor', 'dentist', 'vacation', 'holiday']
        return any(keyword in title for keyword in personal_keywords)
    
    def _classify_event_type(self, raw_event: Dict[str, Any]) -> EventType:
        """Classify event type based on basic heuristics"""
        title = raw_event.get('title', '').lower()
        attendee_count = len(raw_event.get('attendees', []))
        
        if 'focus' in title or 'deep work' in title:
            return EventType.FOCUS_WORK
        elif attendee_count > 1:
            return EventType.MEETING
        elif 'break' in title or 'lunch' in title:
            return EventType.BREAK
        elif 'commute' in title or 'travel' in title:
            return EventType.COMMUTE
        else:
            return EventType.UNKNOWN
    
    def _classify_location_type(self, location: str) -> Optional[str]:
        """Classify location type for privacy-preserving analysis"""
        location_lower = location.lower()
        
        if 'office' in location_lower or 'conference' in location_lower:
            return 'office'
        elif 'home' in location_lower:
            return 'home'
        elif 'zoom' in location_lower or 'teams' in location_lower or 'meet' in location_lower:
            return 'remote'
        else:
            return 'other'
    
    def _hash_title(self, title: str) -> str:
        """Create privacy-preserving hash of event title"""
        import hashlib
        return hashlib.sha256(title.encode()).hexdigest()[:16]
    
    def _parse_datetime(self, datetime_data: Any) -> datetime:
        """Parse datetime from various calendar provider formats"""
        if isinstance(datetime_data, str):
            return datetime.fromisoformat(datetime_data.replace('Z', '+00:00'))
        elif isinstance(datetime_data, dict):
            return datetime.fromisoformat(datetime_data.get('dateTime', datetime_data.get('date')))
        return datetime_data
    
    def _calculate_focus_confidence(self, start_time: datetime, duration_minutes: float) -> float:
        """Calculate confidence score for focus time suggestion"""
        # This would use historical patterns and user preferences
        # For now, simple heuristic based on time of day and duration
        hour = start_time.hour
        
        confidence = 0.5  # Base confidence
        
        # Time of day adjustments (user could customize these)
        if 9 <= hour <= 11:  # Morning focus time
            confidence += 0.3
        elif 14 <= hour <= 16:  # Afternoon focus time
            confidence += 0.2
        
        # Duration adjustments
        if 25 <= duration_minutes <= 90:  # Optimal focus duration
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _generate_focus_reasoning(self, start_time: datetime, duration_minutes: float) -> str:
        """Generate human-readable reasoning for focus suggestion"""
        hour = start_time.hour
        
        reasoning = f"{duration_minutes:.0f}-minute gap available"
        
        if 9 <= hour <= 11:
            reasoning += " during morning peak focus hours"
        elif 14 <= hour <= 16:
            reasoning += " during afternoon focus window"
        
        reasoning += ". User can customize or decline this suggestion."
        
        return reasoning
    
    def _update_cached_events(self, new_events: List[CalendarEvent], provider: CalendarProvider) -> None:
        """Update cached events with new data"""
        # Remove old events from this provider
        self.cached_events = [e for e in self.cached_events 
                            if not e.event_id.startswith(provider.value)]
        
        # Add new events
        self.cached_events.extend(new_events)
        
        # Sort by start time
        self.cached_events.sort(key=lambda x: x.start_time)
    
    def _log_sync_history(self, sync_result: Dict[str, Any]) -> None:
        """Log sync history for user transparency"""
        self.sync_history.append({
            'timestamp': datetime.now().isoformat(),
            'result': sync_result,
            'user_controlled': True
        })
        
        # Keep only last 100 sync records
        self.sync_history = self.sync_history[-100:]


# Example concrete provider implementation
class GoogleCalendarProvider(CalendarProvider_Interface):
    """Example Google Calendar provider implementation"""
    
    def __init__(self):
        self.authenticated = False
        self.credentials = None
    
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with Google Calendar API"""
        # In real implementation, this would handle OAuth flow
        self.authenticated = True
        self.credentials = credentials
        return True
    
    def get_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get events from Google Calendar"""
        if not self.authenticated:
            raise Exception("Not authenticated with Google Calendar")
        
        # In real implementation, this would call Google Calendar API
        # Returning mock data for example
        return [
            {
                'id': 'example_event_1',
                'title': 'Team Meeting',
                'start': start_date.isoformat(),
                'end': (start_date + timedelta(hours=1)).isoformat(),
                'attendees': [{'email': 'user1@example.com'}, {'email': 'user2@example.com'}]
            }
        ]
    
    def create_event(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Create event in Google Calendar"""
        if not self.authenticated:
            return None
        
        # In real implementation, this would call Google Calendar API
        return f"created_event_{uuid.uuid4()}"
    
    def update_event(self, event_id: str, event_data: Dict[str, Any]) -> bool:
        """Update event in Google Calendar"""
        if not self.authenticated:
            return False
        
        # In real implementation, this would call Google Calendar API
        return True


# Helper function to create calendar integration with user preferences
def create_calendar_integration(user_profile, enable_basic_sync: bool = True) -> PrivacyPreservingCalendarSync:
    """
    Create calendar integration configured for user preferences
    """
    # Default conservative settings
    settings = CalendarIntegrationSettings(
        enabled_providers=[CalendarProvider.MANUAL],  # Start with manual only
        primary_provider=CalendarProvider.MANUAL,
        granted_permissions=[IntegrationPermission.READ_EVENTS] if enable_basic_sync else [],
        hash_event_titles=True,  # Privacy first
        exclude_personal_events=True,  # Privacy first
        share_meeting_patterns=False,  # Privacy first
        enable_productivity_correlation=False,  # User must explicitly enable
        auto_create_focus_blocks=False,  # User must explicitly enable
        sync_frequency_hours=24,  # Conservative sync frequency
        min_focus_block_minutes=25,  # Standard pomodoro
        max_daily_focus_blocks=3   # Conservative limit
    )
    
    return PrivacyPreservingCalendarSync(user_profile, settings)

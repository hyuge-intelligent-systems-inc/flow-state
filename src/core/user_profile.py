

"""
FlowState User Profile Manager
Centralized user preferences and settings management

Key principles implemented:
- User data ownership and control
- Granular privacy settings
- Individual differences accommodation
- Cross-module preference coordination
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class ProductivityMode(Enum):
    """User's current productivity mode based on life circumstances"""
    SURVIVAL = "survival"      # High constraints, focus on essentials only
    MAINTENANCE = "maintenance"  # Moderate constraints, sustainable routines
    GROWTH = "growth"          # Lower constraints, room for optimization
    MASTERY = "mastery"        # Low constraints, advanced development


class PrivacyLevel(Enum):
    """Data sharing privacy levels"""
    PRIVATE = "private"              # No sharing
    ANONYMOUS = "anonymous"          # Anonymous aggregation only
    AGGREGATED = "aggregated"        # Team aggregated insights
    TEAM_VISIBLE = "team_visible"    # Team can see patterns
    FULL_COLLABORATION = "full"      # Full collaboration features


@dataclass
class AccessibilityPreferences:
    """Accessibility and neurodiversity accommodations"""
    # Visual preferences
    high_contrast: bool = False
    reduced_motion: bool = False
    simplified_interface: bool = False
    custom_color_scheme: Optional[str] = None
    
    # Cognitive preferences
    extended_processing_time: bool = False
    reduced_decision_points: bool = False
    predictable_interface: bool = False
    
    # Attention preferences
    minimal_notifications: bool = False
    focus_protection_strict: bool = False
    break_reminders_gentle: bool = False
    
    # Sensory preferences
    audio_cues_enabled: bool = False
    haptic_feedback_enabled: bool = True
    visual_noise_reduction: bool = False


@dataclass
class ProductivityPreferences:
    """Individual productivity approach preferences"""
    # Time management style
    preferred_session_length: int = 25  # minutes
    natural_break_frequency: int = 90   # minutes
    deep_work_preference: str = "morning"  # morning, afternoon, evening
    
    # Methodology preferences
    likes_time_blocking: bool = True
    likes_pomodoro: bool = False
    likes_gtd_approach: bool = False
    prefers_flexible_planning: bool = True
    
    # Motivation preferences
    responds_to_deadlines: bool = True
    prefers_collaborative_work: bool = False
    needs_autonomy_high: bool = True
    values_progress_tracking: bool = True
    
    # Energy management
    energy_peak_time: str = "morning"
    energy_low_time: str = "afternoon"
    prefers_task_variety: bool = True
    handles_interruptions_well: bool = False


@dataclass
class PrivacySettings:
    """Granular privacy and data sharing controls"""
    # Module-specific privacy levels
    time_tracking_privacy: PrivacyLevel = PrivacyLevel.PRIVATE
    pattern_analysis_privacy: PrivacyLevel = PrivacyLevel.PRIVATE
    ai_insights_privacy: PrivacyLevel = PrivacyLevel.PRIVATE
    psychology_insights_privacy: PrivacyLevel = PrivacyLevel.PRIVATE
    team_collaboration_privacy: PrivacyLevel = PrivacyLevel.PRIVATE
    
    # Specific data type controls
    share_productivity_patterns: bool = False
    share_energy_levels: bool = False
    share_focus_quality: bool = False
    share_goal_progress: bool = False
    share_challenge_areas: bool = False
    
    # External integration permissions
    calendar_integration_enabled: bool = False
    external_app_data_sharing: bool = False
    research_participation: bool = False
    
    # Data retention preferences
    auto_delete_old_data: bool = False
    data_retention_months: int = 24


class UserProfile:
    """
    Centralized user profile management with privacy-first design
    """
    
    def __init__(self, user_id: Optional[str] = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        
        # Core profile data
        self.accessibility_prefs = AccessibilityPreferences()
        self.productivity_prefs = ProductivityPreferences()
        self.privacy_settings = PrivacySettings()
        
        # Current state
        self.current_productivity_mode = ProductivityMode.MAINTENANCE
        self.ui_complexity_level = 1  # 1-5, controlled by ProgressiveComplexity
        
        # Usage and engagement tracking
        self.days_active = 0
        self.total_sessions = 0
        self.feature_exploration_count = 0
        self.last_active_date = None
        
        # Module-specific preferences
        self.module_preferences = {
            'time_tracker': {},
            'pattern_analyzer': {},
            'ai_tracker': {},
            'self_discovery': {},
            'team_optimizer': {},
            'ui_complexity': {}
        }
        
        # User insights and discoveries (user-controlled)
        self.personal_insights = []
        self.productivity_goals = []
        self.discovered_patterns = []
    
    def update_accessibility_preferences(self, **kwargs) -> None:
        """Update accessibility preferences with user control"""
        for key, value in kwargs.items():
            if hasattr(self.accessibility_prefs, key):
                setattr(self.accessibility_prefs, key, value)
        self._mark_updated()
        self._log_preference_change('accessibility', kwargs)
    
    def update_productivity_preferences(self, **kwargs) -> None:
        """Update productivity preferences based on user discovery"""
        for key, value in kwargs.items():
            if hasattr(self.productivity_prefs, key):
                setattr(self.productivity_prefs, key, value)
        self._mark_updated()
        self._log_preference_change('productivity', kwargs)
    
    def update_privacy_settings(self, **kwargs) -> None:
        """Update privacy settings with explicit confirmation"""
        changes_made = {}
        
        for key, value in kwargs.items():
            if hasattr(self.privacy_settings, key):
                old_value = getattr(self.privacy_settings, key)
                setattr(self.privacy_settings, key, value)
                changes_made[key] = {'old': old_value, 'new': value}
        
        self._mark_updated()
        self._log_privacy_change(changes_made)
    
    def set_productivity_mode(self, mode: ProductivityMode, reason: str = "") -> None:
        """
        Set current productivity mode based on life circumstances
        """
        old_mode = self.current_productivity_mode
        self.current_productivity_mode = mode
        
        # Adjust default preferences based on mode
        if mode == ProductivityMode.SURVIVAL:
            # Simplify everything for survival mode
            self.accessibility_prefs.simplified_interface = True
            self.accessibility_prefs.reduced_decision_points = True
            self.productivity_prefs.prefers_flexible_planning = True
        
        elif mode == ProductivityMode.MAINTENANCE:
            # Sustainable defaults for maintenance mode
            self.productivity_prefs.prefers_flexible_planning = True
            self.accessibility_prefs.predictable_interface = True
        
        elif mode == ProductivityMode.GROWTH:
            # Enable more features for growth mode
            self.accessibility_prefs.simplified_interface = False
            self.productivity_prefs.values_progress_tracking = True
        
        elif mode == ProductivityMode.MASTERY:
            # Advanced features available for mastery mode
            self.accessibility_prefs.reduced_decision_points = False
        
        self._mark_updated()
        self._log_mode_change(old_mode, mode, reason)
    
    def get_module_preferences(self, module_name: str) -> Dict[str, Any]:
        """Get preferences for a specific module"""
        return self.module_preferences.get(module_name, {})
    
    def update_module_preferences(self, module_name: str, preferences: Dict[str, Any]) -> None:
        """Update preferences for a specific module"""
        if module_name not in self.module_preferences:
            self.module_preferences[module_name] = {}
        
        self.module_preferences[module_name].update(preferences)
        self._mark_updated()
    
    def add_personal_insight(self, insight: str, category: str, confidence: str) -> None:
        """
        Add user-discovered personal insight (user controls all insights)
        """
        insight_entry = {
            'id': str(uuid.uuid4()),
            'insight': insight,
            'category': category,
            'confidence': confidence,
            'discovered_date': datetime.now().isoformat(),
            'user_noted': True  # Always user-generated
        }
        
        self.personal_insights.append(insight_entry)
        self._mark_updated()
    
    def add_productivity_goal(self, goal: str, target_date: Optional[datetime] = None) -> None:
        """Add user-defined productivity goal"""
        goal_entry = {
            'id': str(uuid.uuid4()),
            'goal': goal,
            'created_date': datetime.now().isoformat(),
            'target_date': target_date.isoformat() if target_date else None,
            'status': 'active',
            'progress_notes': []
        }
        
        self.productivity_goals.append(goal_entry)
        self._mark_updated()
    
    def track_usage(self, session_type: str = "general") -> None:
        """Track usage for progression and engagement measurement"""
        today = datetime.now().date()
        
        # Update activity tracking
        if self.last_active_date != today:
            self.days_active += 1
            self.last_active_date = today
        
        self.total_sessions += 1
        self._mark_updated()
    
    def get_privacy_summary(self) -> Dict[str, Any]:
        """
        Provide transparent summary of current privacy settings
        """
        return {
            'data_sharing_summary': {
                'time_tracking': self.privacy_settings.time_tracking_privacy.value,
                'pattern_analysis': self.privacy_settings.pattern_analysis_privacy.value,
                'ai_insights': self.privacy_settings.ai_insights_privacy.value,
                'psychology_insights': self.privacy_settings.psychology_insights_privacy.value,
                'team_collaboration': self.privacy_settings.team_collaboration_privacy.value
            },
            'external_integrations': {
                'calendar_integration': self.privacy_settings.calendar_integration_enabled,
                'external_apps': self.privacy_settings.external_app_data_sharing,
                'research_participation': self.privacy_settings.research_participation
            },
            'data_retention': {
                'auto_delete_enabled': self.privacy_settings.auto_delete_old_data,
                'retention_period_months': self.privacy_settings.data_retention_months
            },
            'data_ownership': 'You own all your data and can export or delete it at any time'
        }
    
    def export_all_data(self) -> Dict[str, Any]:
        """
        Export all user data for portability and transparency
        """
        return {
            'user_profile': {
                'user_id': self.user_id,
                'created_at': self.created_at.isoformat(),
                'last_updated': self.last_updated.isoformat(),
                'current_productivity_mode': self.current_productivity_mode.value,
                'ui_complexity_level': self.ui_complexity_level,
                'usage_stats': {
                    'days_active': self.days_active,
                    'total_sessions': self.total_sessions,
                    'feature_exploration_count': self.feature_exploration_count
                }
            },
            'preferences': {
                'accessibility': asdict(self.accessibility_prefs),
                'productivity': asdict(self.productivity_prefs),
                'privacy': asdict(self.privacy_settings),
                'module_specific': self.module_preferences
            },
            'user_insights': {
                'personal_insights': self.personal_insights,
                'productivity_goals': self.productivity_goals,
                'discovered_patterns': self.discovered_patterns
            },
            'export_metadata': {
                'export_date': datetime.now().isoformat(),
                'export_version': '1.0',
                'data_ownership': 'This data belongs entirely to the user'
            }
        }
    
    def reset_all_data(self, confirmation_id: str) -> Dict[str, str]:
        """
        Reset all user data with explicit confirmation
        """
        if confirmation_id != f"RESET-{self.user_id[:8]}":
            return {
                'status': 'error',
                'message': 'Invalid confirmation ID. Data not reset.',
                'required_confirmation': f"RESET-{self.user_id[:8]}"
            }
        
        # Reset to defaults
        self.accessibility_prefs = AccessibilityPreferences()
        self.productivity_prefs = ProductivityPreferences()
        self.privacy_settings = PrivacySettings()
        self.current_productivity_mode = ProductivityMode.MAINTENANCE
        self.ui_complexity_level = 1
        self.days_active = 0
        self.total_sessions = 0
        self.feature_exploration_count = 0
        self.module_preferences = {'time_tracker': {}, 'pattern_analyzer': {}, 'ai_tracker': {}, 'self_discovery': {}, 'team_optimizer': {}, 'ui_complexity': {}}
        self.personal_insights = []
        self.productivity_goals = []
        self.discovered_patterns = []
        
        self._mark_updated()
        
        return {
            'status': 'success',
            'message': 'All user data has been reset to defaults',
            'reset_date': datetime.now().isoformat()
        }
    
    def _mark_updated(self) -> None:
        """Mark profile as updated"""
        self.last_updated = datetime.now()
    
    def _log_preference_change(self, category: str, changes: Dict[str, Any]) -> None:
        """Log preference changes for transparency"""
        # In a real implementation, this might log to a user-accessible change log
        pass
    
    def _log_privacy_change(self, changes: Dict[str, Any]) -> None:
        """Log privacy setting changes for user transparency"""
        # In a real implementation, this would provide detailed privacy change logging
        pass
    
    def _log_mode_change(self, old_mode: ProductivityMode, new_mode: ProductivityMode, reason: str) -> None:
        """Log productivity mode changes"""
        # In a real implementation, this helps users understand their productivity journey
        pass
    
    def get_configuration_for_module(self, module_name: str) -> Dict[str, Any]:
        """
        Get comprehensive configuration for a specific module
        """
        base_config = {
            'accessibility': asdict(self.accessibility_prefs),
            'productivity_mode': self.current_productivity_mode.value,
            'ui_complexity_level': self.ui_complexity_level,
            'privacy_level': getattr(self.privacy_settings, f"{module_name}_privacy", PrivacyLevel.PRIVATE).value,
            'module_preferences': self.get_module_preferences(module_name)
        }
        
        # Add module-specific configurations
        if module_name == 'time_tracker':
            base_config.update({
                'preferred_session_length': self.productivity_prefs.preferred_session_length,
                'break_frequency': self.productivity_prefs.natural_break_frequency,
                'enable_ai_suggestions': self.privacy_settings.ai_insights_privacy != PrivacyLevel.PRIVATE
            })
        
        elif module_name == 'pattern_analyzer':
            base_config.update({
                'require_user_interpretation': True,  # Always true
                'show_confidence_levels': True,       # Always true
                'minimum_sample_size': 7              # Conservative approach
            })
        
        elif module_name == 'ai_tracker':
            base_config.update({
                'max_daily_predictions': 5,           # Conservative limit
                'confidence_threshold': 0.7,         # High confidence required
                'enable_track_record_display': True  # Transparency
            })
        
        elif module_name == 'team_optimizer':
            base_config.update({
                'collaboration_level': self.privacy_settings.team_collaboration_privacy.value,
                'share_patterns': self.privacy_settings.share_productivity_patterns,
                'require_explicit_consent': True     # Always true
            })
        
        return base_config


# Example usage and configuration helper
def create_user_profile_for_individual_needs(
    productivity_mode: ProductivityMode = ProductivityMode.MAINTENANCE,
    accessibility_needs: Optional[Dict[str, bool]] = None,
    privacy_preference: PrivacyLevel = PrivacyLevel.PRIVATE
) -> UserProfile:
    """
    Helper function to create user profile configured for individual needs
    """
    profile = UserProfile()
    profile.set_productivity_mode(productivity_mode)
    
    if accessibility_needs:
        profile.update_accessibility_preferences(**accessibility_needs)
    
    # Set consistent privacy level across modules
    privacy_settings = {
        'time_tracking_privacy': privacy_preference,
        'pattern_analysis_privacy': privacy_preference,
        'ai_insights_privacy': privacy_preference,
        'psychology_insights_privacy': privacy_preference,
        'team_collaboration_privacy': privacy_preference
    }
    profile.update_privacy_settings(**privacy_settings)
    
    return profile

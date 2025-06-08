

"""
FlowState Progressive Complexity UI Module
Based on expert analysis: Earned sophistication and user-controlled interface evolution

Key principles implemented:
- Start with boring, reliable functionality
- Users earn visual sophistication through demonstrated engagement
- Complete user control over complexity level
- Graceful degradation when features fail
- Performance over polish, with polish as reward
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ComplexityLevel(Enum):
    """Progressive UI complexity levels users can earn or choose"""
    MINIMAL = "minimal"           # Just the essentials, maximum reliability
    STANDARD = "standard"         # Clean, functional interface
    ENHANCED = "enhanced"         # Polish and convenience features
    SOPHISTICATED = "sophisticated"  # Advanced visualizations and interactions
    BEAUTIFUL = "beautiful"       # Full visual sophistication


class FeatureCategory(Enum):
    """Categories of features that unlock progressively"""
    CORE_FUNCTIONALITY = "core_functionality"
    VISUAL_POLISH = "visual_polish"
    CONVENIENCE_FEATURES = "convenience_features"
    ADVANCED_INSIGHTS = "advanced_insights"
    CUSTOMIZATION = "customization"
    COLLABORATION = "collaboration"


@dataclass
class UIFeature:
    """Individual UI feature with unlock requirements"""
    feature_id: str
    name: str
    description: str
    category: FeatureCategory
    required_level: ComplexityLevel
    unlock_criteria: Dict[str, Any]
    enabled: bool = False
    user_override: bool = False  # User can always enable/disable


@dataclass
class UsageMetrics:
    """Metrics for determining UI progression eligibility"""
    days_active: int
    sessions_completed: int
    features_used_count: int
    data_entries: int
    user_satisfaction_rating: Optional[float]
    engagement_consistency: float  # How regularly user engages
    feature_exploration_rate: float  # How much user explores available features


class ProgressiveComplexityManager:
    """
    Manages UI complexity progression based on user engagement and choice
    """
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.current_level = ComplexityLevel.MINIMAL
        self.user_forced_level: Optional[ComplexityLevel] = None  # User override
        self.features = self._initialize_features()
        self.usage_history: List[Dict] = []
        self.user_preferences = self._initialize_preferences()
        
    def _initialize_features(self) -> Dict[str, UIFeature]:
        """Initialize all UI features with their unlock requirements"""
        return {
            # Core functionality - always available
            "basic_timer": UIFeature(
                feature_id="basic_timer",
                name="Basic Timer",
                description="Simple start/stop timer",
                category=FeatureCategory.CORE_FUNCTIONALITY,
                required_level=ComplexityLevel.MINIMAL,
                unlock_criteria={},
                enabled=True
            ),
            
            "time_logging": UIFeature(
                feature_id="time_logging",
                name="Time Logging",
                description="Log completed time entries",
                category=FeatureCategory.CORE_FUNCTIONALITY,
                required_level=ComplexityLevel.MINIMAL,
                unlock_criteria={},
                enabled=True
            ),
            
            "daily_summary": UIFeature(
                feature_id="daily_summary",
                name="Daily Summary",
                description="Basic daily time summary",
                category=FeatureCategory.CORE_FUNCTIONALITY,
                required_level=ComplexityLevel.MINIMAL,
                unlock_criteria={},
                enabled=True
            ),
            
            # Standard level features
            "categories": UIFeature(
                feature_id="categories",
                name="Task Categories",
                description="Organize tasks by category",
                category=FeatureCategory.CONVENIENCE_FEATURES,
                required_level=ComplexityLevel.STANDARD,
                unlock_criteria={"days_active": 3, "sessions_completed": 5},
                enabled=False
            ),
            
            "weekly_view": UIFeature(
                feature_id="weekly_view",
                name="Weekly Overview",
                description="Week-level time analysis",
                category=FeatureCategory.CONVENIENCE_FEATURES,
                required_level=ComplexityLevel.STANDARD,
                unlock_criteria={"days_active": 5, "data_entries": 10},
                enabled=False
            ),
            
            # Enhanced level features
            "visual_themes": UIFeature(
                feature_id="visual_themes",
                name="Visual Themes",
                description="Color themes and visual polish",
                category=FeatureCategory.VISUAL_POLISH,
                required_level=ComplexityLevel.ENHANCED,
                unlock_criteria={"days_active": 7, "engagement_consistency": 0.6},
                enabled=False
            ),
            
            "pattern_insights": UIFeature(
                feature_id="pattern_insights",
                name="Pattern Insights",
                description="Visual pattern recognition",
                category=FeatureCategory.ADVANCED_INSIGHTS,
                required_level=ComplexityLevel.ENHANCED,
                unlock_criteria={"days_active": 10, "data_entries": 25, "features_used_count": 4},
                enabled=False
            ),
            
            "custom_notifications": UIFeature(
                feature_id="custom_notifications",
                name="Smart Notifications",
                description="Customizable notification system",
                category=FeatureCategory.CONVENIENCE_FEATURES,
                required_level=ComplexityLevel.ENHANCED,
                unlock_criteria={"days_active": 14, "user_satisfaction_rating": 4.0},
                enabled=False
            ),
            
            # Sophisticated level features
            "advanced_analytics": UIFeature(
                feature_id="advanced_analytics",
                name="Advanced Analytics",
                description="Detailed productivity analytics",
                category=FeatureCategory.ADVANCED_INSIGHTS,
                required_level=ComplexityLevel.SOPHISTICATED,
                unlock_criteria={"days_active": 21, "data_entries": 50, "feature_exploration_rate": 0.7},
                enabled=False
            ),
            
            "ai_suggestions": UIFeature(
                feature_id="ai_suggestions",
                name="AI Suggestions",
                description="Intelligent productivity suggestions",
                category=FeatureCategory.ADVANCED_INSIGHTS,
                required_level=ComplexityLevel.SOPHISTICATED,
                unlock_criteria={"days_active": 28, "engagement_consistency": 0.8},
                enabled=False
            ),
            
            "custom_dashboard": UIFeature(
                feature_id="custom_dashboard",
                name="Custom Dashboard",
                description="Personalized dashboard layout",
                category=FeatureCategory.CUSTOMIZATION,
                required_level=ComplexityLevel.SOPHISTICATED,
                unlock_criteria={"days_active": 30, "features_used_count": 8},
                enabled=False
            ),
            
            # Beautiful level features
            "animated_transitions": UIFeature(
                feature_id="animated_transitions",
                name="Smooth Animations",
                description="Beautiful UI transitions",
                category=FeatureCategory.VISUAL_POLISH,
                required_level=ComplexityLevel.BEAUTIFUL,
                unlock_criteria={"days_active": 45, "user_satisfaction_rating": 4.5, "engagement_consistency": 0.9},
                enabled=False
            ),
            
            "data_visualizations": UIFeature(
                feature_id="data_visualizations",
                name="Rich Visualizations",
                description="Beautiful charts and graphs",
                category=FeatureCategory.VISUAL_POLISH,
                required_level=ComplexityLevel.BEAUTIFUL,
                unlock_criteria={"days_active": 60, "data_entries": 100},
                enabled=False
            ),
            
            "collaboration_tools": UIFeature(
                feature_id="collaboration_tools",
                name="Team Collaboration",
                description="Share insights with team",
                category=FeatureCategory.COLLABORATION,
                required_level=ComplexityLevel.BEAUTIFUL,
                unlock_criteria={"days_active": 90, "user_satisfaction_rating": 4.8},
                enabled=False
            )
        }
    
    def _initialize_preferences(self) -> Dict[str, Any]:
        """Initialize user UI preferences"""
        return {
            "auto_progression": True,  # Automatically unlock features when criteria met
            "visual_density": "comfortable",  # minimal, comfortable, dense
            "animation_speed": "normal",  # slow, normal, fast, off
            "notification_frequency": "moderate",  # minimal, moderate, frequent
            "color_scheme": "auto",  # light, dark, auto
            "complexity_preference": "earned",  # minimal, earned, maximum
            "performance_priority": True  # Prioritize performance over beauty
        }
    
    def calculate_usage_metrics(self, usage_data: Dict[str, Any]) -> UsageMetrics:
        """
        Calculate usage metrics for complexity progression
        
        Args:
            usage_data: Raw usage data from the application
            
        Returns:
            UsageMetrics: Calculated metrics for progression decisions
        """
        # Calculate days active
        if usage_data.get("first_use_date"):
            first_use = datetime.fromisoformat(usage_data["first_use_date"])
            days_active = (datetime.now() - first_use).days + 1
        else:
            days_active = 0
        
        # Calculate engagement consistency (how regularly user engages)
        recent_sessions = usage_data.get("sessions_last_14_days", [])
        if len(recent_sessions) >= 14:
            engagement_consistency = len([d for d in recent_sessions if d > 0]) / 14
        else:
            engagement_consistency = 0.0
        
        # Calculate feature exploration rate
        total_features = len([f for f in self.features.values() if f.enabled])
        used_features = len(usage_data.get("features_used", []))
        feature_exploration_rate = used_features / max(total_features, 1)
        
        return UsageMetrics(
            days_active=days_active,
            sessions_completed=usage_data.get("total_sessions", 0),
            features_used_count=used_features,
            data_entries=usage_data.get("total_time_entries", 0),
            user_satisfaction_rating=usage_data.get("satisfaction_rating"),
            engagement_consistency=engagement_consistency,
            feature_exploration_rate=feature_exploration_rate
        )
    
    def check_unlock_eligibility(self, metrics: UsageMetrics) -> List[str]:
        """
        Check which features are eligible for unlock
        
        Args:
            metrics: Current usage metrics
            
        Returns:
            List of feature IDs eligible for unlock
        """
        eligible_features = []
        
        for feature_id, feature in self.features.items():
            if feature.enabled or feature.user_override:
                continue  # Already enabled or user controlled
            
            # Check unlock criteria
            criteria_met = True
            for criterion, required_value in feature.unlock_criteria.items():
                actual_value = getattr(metrics, criterion, 0)
                
                if isinstance(required_value, (int, float)):
                    if actual_value < required_value:
                        criteria_met = False
                        break
                elif isinstance(required_value, bool):
                    if actual_value != required_value:
                        criteria_met = False
                        break
            
            if criteria_met:
                eligible_features.append(feature_id)
        
        return eligible_features
    
    def unlock_features(self, feature_ids: List[str], user_initiated: bool = False) -> List[str]:
        """
        Unlock specified features
        
        Args:
            feature_ids: Features to unlock
            user_initiated: Whether user explicitly requested unlock
            
        Returns:
            List of successfully unlocked feature IDs
        """
        unlocked = []
        
        for feature_id in feature_ids:
            if feature_id in self.features:
                feature = self.features[feature_id]
                
                # Always allow user-initiated unlocks
                if user_initiated or self.user_preferences.get("auto_progression", True):
                    feature.enabled = True
                    feature.user_override = user_initiated
                    unlocked.append(feature_id)
                    
                    # Log unlock event
                    self.usage_history.append({
                        "event": "feature_unlocked",
                        "feature_id": feature_id,
                        "timestamp": datetime.now().isoformat(),
                        "user_initiated": user_initiated
                    })
        
        # Update complexity level if needed
        self._update_complexity_level()
        
        return unlocked
    
    def _update_complexity_level(self):
        """Update current complexity level based on enabled features"""
        if self.user_forced_level:
            self.current_level = self.user_forced_level
            return
        
        # Count enabled features by level
        level_counts = {level: 0 for level in ComplexityLevel}
        
        for feature in self.features.values():
            if feature.enabled:
                level_counts[feature.required_level] += 1
        
        # Determine current level based on enabled features
        if level_counts[ComplexityLevel.BEAUTIFUL] > 0:
            self.current_level = ComplexityLevel.BEAUTIFUL
        elif level_counts[ComplexityLevel.SOPHISTICATED] > 0:
            self.current_level = ComplexityLevel.SOPHISTICATED
        elif level_counts[ComplexityLevel.ENHANCED] > 0:
            self.current_level = ComplexityLevel.ENHANCED
        elif level_counts[ComplexityLevel.STANDARD] > 0:
            self.current_level = ComplexityLevel.STANDARD
        else:
            self.current_level = ComplexityLevel.MINIMAL
    
    def set_user_complexity_level(self, level: ComplexityLevel, override: bool = False) -> bool:
        """
        Allow user to manually set complexity level
        
        Args:
            level: Desired complexity level
            override: Whether to override automatic progression
            
        Returns:
            bool: Success status
        """
        if override:
            self.user_forced_level = level
        else:
            self.user_forced_level = None
        
        # Enable/disable features based on level
        for feature in self.features.values():
            if not feature.user_override:  # Don't touch user-controlled features
                if feature.required_level.value <= level.value:
                    feature.enabled = True
                else:
                    feature.enabled = False
        
        self.current_level = level
        
        # Log level change
        self.usage_history.append({
            "event": "complexity_level_changed",
            "new_level": level.value,
            "user_override": override,
            "timestamp": datetime.now().isoformat()
        })
        
        return True
    
    def get_current_ui_config(self) -> Dict[str, Any]:
        """
        Get current UI configuration based on complexity level and enabled features
        
        Returns:
            Dict: UI configuration for frontend rendering
        """
        enabled_features = {
            feature_id: feature 
            for feature_id, feature in self.features.items() 
            if feature.enabled
        }
        
        config = {
            "complexity_level": self.current_level.value,
            "enabled_features": {
                feature_id: {
                    "name": feature.name,
                    "description": feature.description,
                    "category": feature.category.value,
                    "user_controlled": feature.user_override
                }
                for feature_id, feature in enabled_features.items()
            },
            "ui_preferences": self.user_preferences,
            "performance_mode": self.user_preferences.get("performance_priority", True),
            "available_upgrades": self._get_available_upgrades(),
            "progression_status": self._get_progression_status()
        }
        
        return config
    
    def _get_available_upgrades(self) -> List[Dict[str, Any]]:
        """Get features available for unlock"""
        available = []
        
        for feature_id, feature in self.features.items():
            if not feature.enabled and not feature.user_override:
                available.append({
                    "feature_id": feature_id,
                    "name": feature.name,
                    "description": feature.description,
                    "category": feature.category.value,
                    "required_level": feature.required_level.value,
                    "unlock_criteria": feature.unlock_criteria
                })
        
        return available
    
    def _get_progression_status(self) -> Dict[str, Any]:
        """Get user's progression status"""
        total_features = len(self.features)
        enabled_features = len([f for f in self.features.values() if f.enabled])
        
        return {
            "features_unlocked": enabled_features,
            "total_features": total_features,
            "progression_percent": round((enabled_features / total_features) * 100, 1),
            "current_level": self.current_level.value,
            "can_progress": self.user_forced_level is None,
            "next_unlock_suggestions": self._get_next_unlock_suggestions()
        }
    
    def _get_next_unlock_suggestions(self) -> List[Dict[str, Any]]:
        """Suggest how user can unlock next features"""
        suggestions = []
        
        # Find the next 2-3 features closest to unlock
        disabled_features = [
            (feature_id, feature) 
            for feature_id, feature in self.features.items() 
            if not feature.enabled and not feature.user_override
        ]
        
        # Sort by complexity level and criteria difficulty
        disabled_features.sort(key=lambda x: (
            list(ComplexityLevel).index(x[1].required_level),
            sum(x[1].unlock_criteria.values()) if x[1].unlock_criteria else 0
        ))
        
        for feature_id, feature in disabled_features[:3]:
            suggestion = {
                "feature_name": feature.name,
                "description": feature.description,
                "requirements": []
            }
            
            for criterion, required_value in feature.unlock_criteria.items():
                suggestion["requirements"].append({
                    "criterion": criterion.replace("_", " ").title(),
                    "required": required_value,
                    "description": self._get_criterion_description(criterion, required_value)
                })
            
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_criterion_description(self, criterion: str, required_value: Any) -> str:
        """Get user-friendly description of unlock criteria"""
        descriptions = {
            "days_active": f"Use FlowState for {required_value} days",
            "sessions_completed": f"Complete {required_value} work sessions",
            "data_entries": f"Log {required_value} time entries",
            "features_used_count": f"Try {required_value} different features",
            "engagement_consistency": f"Use FlowState regularly ({required_value*100:.0f}% of days)",
            "feature_exploration_rate": f"Explore {required_value*100:.0f}% of available features",
            "user_satisfaction_rating": f"Rate your experience {required_value}/5 or higher"
        }
        
        return descriptions.get(criterion, f"{criterion}: {required_value}")
    
    def record_feature_usage(self, feature_id: str, usage_type: str = "used") -> bool:
        """
        Record feature usage for analytics
        
        Args:
            feature_id: Feature that was used
            usage_type: Type of usage (used, enabled, disabled)
            
        Returns:
            bool: Success status
        """
        if feature_id not in self.features:
            return False
        
        self.usage_history.append({
            "event": "feature_usage",
            "feature_id": feature_id,
            "usage_type": usage_type,
            "timestamp": datetime.now().isoformat(),
            "complexity_level": self.current_level.value
        })
        
        return True
    
    def disable_feature(self, feature_id: str, user_initiated: bool = True) -> bool:
        """
        Allow users to disable features they don't want
        
        Args:
            feature_id: Feature to disable
            user_initiated: Whether user requested this
            
        Returns:
            bool: Success status
        """
        if feature_id not in self.features:
            return False
        
        feature = self.features[feature_id]
        
        # Don't disable core functionality unless user insists
        if (feature.category == FeatureCategory.CORE_FUNCTIONALITY and 
            not user_initiated):
            return False
        
        feature.enabled = False
        if user_initiated:
            feature.user_override = True
        
        # Log disable event
        self.usage_history.append({
            "event": "feature_disabled",
            "feature_id": feature_id,
            "timestamp": datetime.now().isoformat(),
            "user_initiated": user_initiated
        })
        
        return True
    
    def get_performance_mode_config(self) -> Dict[str, Any]:
        """
        Get configuration for performance-optimized UI
        
        Returns:
            Dict: Performance-focused UI settings
        """
        return {
            "animations_enabled": False,
            "visual_effects": "minimal",
            "update_frequency": "reduced",
            "background_processing": "minimal",
            "visual_density": "compact",
            "image_quality": "optimized",
            "transition_speed": "instant",
            "polling_interval": "extended"
        }
    
    def export_progression_data(self) -> Dict[str, Any]:
        """
        Export user's UI progression data
        
        Returns:
            Dict: Complete progression history and current state
        """
        return {
            "user_id": self.user_id,
            "export_date": datetime.now().isoformat(),
            "current_complexity_level": self.current_level.value,
            "user_forced_level": self.user_forced_level.value if self.user_forced_level else None,
            "enabled_features": {
                feature_id: {
                    "name": feature.name,
                    "category": feature.category.value,
                    "level": feature.required_level.value,
                    "user_override": feature.user_override
                }
                for feature_id, feature in self.features.items()
                if feature.enabled
            },
            "user_preferences": self.user_preferences,
            "progression_history": self.usage_history,
            "progression_status": self._get_progression_status(),
            "notes": {
                "data_ownership": "User controls all UI preferences and progression",
                "reset_available": "User can reset to minimal complexity at any time",
                "customization": "All features can be individually enabled/disabled"
            }
        }
    
    def reset_to_minimal(self, user_confirmation: bool = False) -> bool:
        """
        Reset UI to minimal complexity
        
        Args:
            user_confirmation: Explicit user confirmation required
            
        Returns:
            bool: Success status
        """
        if not user_confirmation:
            return False
        
        # Reset to minimal level
        self.current_level = ComplexityLevel.MINIMAL
        self.user_forced_level = None
        
        # Disable all non-core features
        for feature in self.features.values():
            if feature.category != FeatureCategory.CORE_FUNCTIONALITY:
                feature.enabled = False
                feature.user_override = False
        
        # Log reset
        self.usage_history.append({
            "event": "reset_to_minimal",
            "timestamp": datetime.now().isoformat(),
            "user_initiated": True
        })
        
        return True


# Example usage and testing
if __name__ == "__main__":
    # Create complexity manager
    ui_manager = ProgressiveComplexityManager("user_123")
    
    # Simulate usage data
    usage_data = {
        "first_use_date": (datetime.now() - timedelta(days=15)).isoformat(),
        "total_sessions": 25,
        "total_time_entries": 30,
        "features_used": ["basic_timer", "time_logging", "daily_summary", "categories"],
        "sessions_last_14_days": [1, 1, 0, 1, 1, 2, 1, 0, 1, 1, 1, 0, 2, 1],
        "satisfaction_rating": 4.2
    }
    
    # Calculate metrics and check unlocks
    metrics = ui_manager.calculate_usage_metrics(usage_data)
    eligible = ui_manager.check_unlock_eligibility(metrics)
    
    print(f"Usage metrics: {asdict(metrics)}")
    print(f"Eligible for unlock: {eligible}")
    
    # Unlock eligible features
    unlocked = ui_manager.unlock_features(eligible)
    print(f"Unlocked features: {unlocked}")
    
    # Get current UI config
    config = ui_manager.get_current_ui_config()
    print("Current UI Config:")
    print(json.dumps(config, indent=2))
    
    # Export progression data
    progression_data = ui_manager.export_progression_data()
    print("\nProgression Data:")
    print(json.dumps(progression_data, indent=2))


"""
FlowState Configuration Settings
Based on expert analysis: User-controlled configuration with privacy-first defaults

Key principles implemented:
- Privacy-first default settings
- User agency preserved through extensive customization options
- Honest limitations and transparent system behavior
- Individual differences accommodation
- Professional boundaries and ethical guidelines
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class Environment(Enum):
    """Application environments"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class LogLevel(Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class PrivacyConfig:
    """Privacy-first configuration defaults"""
    default_data_privacy_level: str = "private"
    anonymize_error_reports: bool = True
    local_processing_preferred: bool = True
    telemetry_enabled: bool = False
    crash_reporting_opt_in: bool = False
    usage_analytics_opt_in: bool = False
    data_retention_days: int = 365
    auto_delete_old_data: bool = False  # User must explicitly enable
    export_includes_system_data: bool = False


@dataclass
class UserAgencyConfig:
    """Configuration preserving user agency and control"""
    require_explicit_consent: bool = True
    allow_ai_overrides: bool = True
    user_controls_complexity: bool = True
    default_to_manual_mode: bool = True
    confirmation_required_for_data_changes: bool = True
    user_interpretation_required: bool = True
    professional_boundaries_enforced: bool = True


@dataclass
class AIConfig:
    """AI configuration with honest limitations"""
    max_predictions_per_day: int = 5
    minimum_confidence_threshold: float = 0.6
    require_supporting_evidence: bool = True
    track_prediction_accuracy: bool = True
    expire_predictions_after_days: int = 7
    local_processing_only: bool = True
    conservative_uncertainty_handling: bool = True
    user_feedback_required: bool = True


@dataclass
class UIConfig:
    """Progressive complexity UI configuration"""
    start_with_minimal_ui: bool = True
    earned_complexity_enabled: bool = True
    manual_complexity_override: bool = True
    performance_over_beauty: bool = True
    accessibility_first: bool = True
    dark_mode_default: bool = False
    animation_reduced_motion: bool = False
    font_size_scalable: bool = True


@dataclass
class PsychologyConfig:
    """Ethical psychology feature configuration"""
    professional_boundaries_strict: bool = True
    self_discovery_only: bool = True
    no_ai_diagnosis: bool = True
    crisis_detection_enabled: bool = True
    professional_referral_resources: bool = True
    user_insight_ownership: bool = True
    reflection_prompts_only: bool = True


@dataclass
class SecurityConfig:
    """Security and data protection configuration"""
    encryption_at_rest: bool = True
    local_data_storage: bool = True
    secure_data_transmission: bool = True
    session_timeout_minutes: int = 60
    auto_logout_enabled: bool = True
    password_requirements_strict: bool = True
    two_factor_auth_available: bool = True
    audit_log_enabled: bool = True


@dataclass
class IntegrationConfig:
    """External integration configuration"""
    calendar_sync_opt_in: bool = False
    task_manager_sync_opt_in: bool = False
    cloud_sync_opt_in: bool = False
    team_features_opt_in: bool = False
    third_party_integrations_disabled: bool = True
    api_rate_limiting_enabled: bool = True
    webhook_validation_strict: bool = True


class FlowStateConfig:
    """
    Main configuration manager for FlowState application
    Based on expert analysis emphasizing user agency and privacy protection
    """
    
    def __init__(self, environment: Environment = Environment.DEVELOPMENT):
        self.environment = environment
        self.config_dir = Path.home() / ".flowstate"
        self.config_dir.mkdir(exist_ok=True)
        
        # Initialize configuration with privacy-first defaults
        self.privacy = PrivacyConfig()
        self.user_agency = UserAgencyConfig()
        self.ai = AIConfig()
        self.ui = UIConfig()
        self.psychology = PsychologyConfig()
        self.security = SecurityConfig()
        self.integration = IntegrationConfig()
        
        # Load user customizations
        self._load_user_config()
        
        # Environment-specific overrides
        self._apply_environment_config()
    
    def _load_user_config(self):
        """Load user customizations from config file"""
        user_config_file = self.config_dir / "user_config.json"
        
        if user_config_file.exists():
            try:
                with open(user_config_file, 'r') as f:
                    user_config = json.load(f)
                    self._apply_user_overrides(user_config)
            except Exception as e:
                print(f"Warning: Could not load user config: {e}")
                print("Using default configuration")
    
    def _apply_user_overrides(self, user_config: Dict[str, Any]):
        """Apply user configuration overrides safely"""
        # Only apply overrides for known configuration sections
        safe_sections = {
            'privacy': self.privacy,
            'ui': self.ui,
            'integration': self.integration
        }
        
        for section_name, section_obj in safe_sections.items():
            if section_name in user_config:
                section_config = user_config[section_name]
                for key, value in section_config.items():
                    if hasattr(section_obj, key):
                        setattr(section_obj, key, value)
    
    def _apply_environment_config(self):
        """Apply environment-specific configuration"""
        if self.environment == Environment.DEVELOPMENT:
            self.ai.local_processing_only = True
            self.privacy.telemetry_enabled = False
            self.security.session_timeout_minutes = 120
            
        elif self.environment == Environment.TESTING:
            self.privacy.data_retention_days = 30
            self.ai.max_predictions_per_day = 10
            self.security.session_timeout_minutes = 30
            
        elif self.environment == Environment.PRODUCTION:
            self.security.password_requirements_strict = True
            self.security.two_factor_auth_available = True
            self.privacy.anonymize_error_reports = True
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration based on environment"""
        base_config = {
            "type": "sqlite",
            "local_storage": True,
            "encryption_enabled": self.security.encryption_at_rest,
            "backup_enabled": True,
            "data_directory": str(self.config_dir / "data")
        }
        
        if self.environment == Environment.DEVELOPMENT:
            base_config.update({
                "database_file": "flowstate_dev.db",
                "enable_sql_logging": True,
                "connection_pool_size": 5
            })
        elif self.environment == Environment.TESTING:
            base_config.update({
                "database_file": ":memory:",
                "enable_sql_logging": False,
                "connection_pool_size": 1
            })
        else:  # Production
            base_config.update({
                "database_file": "flowstate.db",
                "enable_sql_logging": False,
                "connection_pool_size": 10,
                "backup_frequency_hours": 24
            })
        
        return base_config
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        log_level = LogLevel.DEBUG if self.environment == Environment.DEVELOPMENT else LogLevel.INFO
        
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                },
                "simple": {
                    "format": "%(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level.value,
                    "formatter": "simple"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": str(self.config_dir / "flowstate.log"),
                    "level": log_level.value,
                    "formatter": "detailed"
                }
            },
            "loggers": {
                "flowstate": {
                    "level": log_level.value,
                    "handlers": ["console", "file"],
                    "propagate": False
                }
            },
            "root": {
                "level": log_level.value,
                "handlers": ["console"]
            }
        }
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration with honest limitations"""
        return {
            "max_predictions_per_day": self.ai.max_predictions_per_day,
            "confidence_threshold": self.ai.minimum_confidence_threshold,
            "local_processing": self.ai.local_processing_only,
            "prediction_expiry_days": self.ai.expire_predictions_after_days,
            "require_evidence": self.ai.require_supporting_evidence,
            "track_accuracy": self.ai.track_prediction_accuracy,
            "user_feedback_required": self.ai.user_feedback_required,
            "conservative_mode": self.ai.conservative_uncertainty_handling,
            "honest_limitations": {
                "individual_variation_high": True,
                "sample_size_requirements": "minimum_10_data_points",
                "correlation_not_causation": True,
                "context_dependency_significant": True
            }
        }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get progressive complexity UI configuration"""
        return {
            "progressive_complexity": {
                "start_minimal": self.ui.start_with_minimal_ui,
                "earned_sophistication": self.ui.earned_complexity_enabled,
                "user_override": self.ui.manual_complexity_override,
                "performance_priority": self.ui.performance_over_beauty
            },
            "accessibility": {
                "high_contrast_available": True,
                "font_scaling": self.ui.font_size_scalable,
                "reduced_motion": self.ui.animation_reduced_motion,
                "screen_reader_support": True,
                "keyboard_navigation": True
            },
            "appearance": {
                "dark_mode_default": self.ui.dark_mode_default,
                "theme_customizable": True,
                "color_blind_friendly": True
            }
        }
    
    def get_privacy_config(self) -> Dict[str, Any]:
        """Get privacy configuration"""
        return {
            "data_protection": {
                "default_privacy_level": self.privacy.default_data_privacy_level,
                "local_processing_preferred": self.privacy.local_processing_preferred,
                "anonymize_errors": self.privacy.anonymize_error_reports,
                "data_retention_days": self.privacy.data_retention_days
            },
            "user_control": {
                "explicit_consent_required": self.user_agency.require_explicit_consent,
                "granular_privacy_controls": True,
                "data_export_available": True,
                "data_deletion_available": True,
                "privacy_dashboard": True
            },
            "telemetry": {
                "enabled": self.privacy.telemetry_enabled,
                "opt_in_required": True,
                "anonymized": True,
                "user_controlled": True
            }
        }
    
    def get_psychology_config(self) -> Dict[str, Any]:
        """Get ethical psychology configuration"""
        return {
            "professional_boundaries": {
                "no_diagnosis": self.psychology.no_ai_diagnosis,
                "self_discovery_only": self.psychology.self_discovery_only,
                "professional_referral": self.psychology.professional_referral_resources,
                "crisis_detection": self.psychology.crisis_detection_enabled
            },
            "user_agency": {
                "interpretation_required": self.user_agency.user_interpretation_required,
                "insight_ownership": self.psychology.user_insight_ownership,
                "reflection_prompts": self.psychology.reflection_prompts_only
            },
            "ethical_guidelines": {
                "no_manipulation": True,
                "transparent_methods": True,
                "voluntary_participation": True,
                "easy_withdrawal": True
            }
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return {
            "data_protection": {
                "encryption_at_rest": self.security.encryption_at_rest,
                "local_storage": self.security.local_data_storage,
                "secure_transmission": self.security.secure_data_transmission
            },
            "session_management": {
                "timeout_minutes": self.security.session_timeout_minutes,
                "auto_logout": self.security.auto_logout_enabled
            },
            "authentication": {
                "password_requirements": self.security.password_requirements_strict,
                "two_factor_available": self.security.two_factor_auth_available
            },
            "audit": {
                "logging_enabled": self.security.audit_log_enabled,
                "user_controlled": True
            }
        }
    
    def get_integration_config(self) -> Dict[str, Any]:
        """Get external integration configuration"""
        return {
            "calendar": {
                "sync_enabled": self.integration.calendar_sync_opt_in,
                "privacy_preserving": True,
                "user_permission_required": True
            },
            "task_managers": {
                "sync_enabled": self.integration.task_manager_sync_opt_in,
                "supported_providers": ["todoist", "asana", "trello"],
                "oauth_only": True
            },
            "cloud_sync": {
                "enabled": self.integration.cloud_sync_opt_in,
                "encryption_required": True,
                "user_controlled": True
            },
            "team_features": {
                "enabled": self.integration.team_features_opt_in,
                "privacy_preserving": True,
                "opt_out_available": True
            },
            "api": {
                "rate_limiting": self.integration.api_rate_limiting_enabled,
                "webhook_validation": self.integration.webhook_validation_strict,
                "third_party_disabled": self.integration.third_party_integrations_disabled
            }
        }
    
    def save_user_config(self, user_overrides: Dict[str, Any], 
                        user_confirmation: bool = False) -> bool:
        """Save user configuration overrides with confirmation"""
        if not user_confirmation:
            return False, "Configuration changes require explicit user confirmation"
        
        user_config_file = self.config_dir / "user_config.json"
        
        try:
            # Load existing config
            existing_config = {}
            if user_config_file.exists():
                with open(user_config_file, 'r') as f:
                    existing_config = json.load(f)
            
            # Merge with overrides
            existing_config.update(user_overrides)
            
            # Save updated config
            with open(user_config_file, 'w') as f:
                json.dump(existing_config, f, indent=2)
            
            # Apply to current instance
            self._apply_user_overrides(existing_config)
            
            return True, "User configuration saved successfully"
            
        except Exception as e:
            return False, f"Error saving user configuration: {e}"
    
    def reset_to_defaults(self, confirmation_phrase: str) -> bool:
        """Reset configuration to privacy-first defaults"""
        expected_phrase = "RESET CONFIG TO DEFAULTS"
        if confirmation_phrase != expected_phrase:
            return False, f"Reset requires exact phrase: '{expected_phrase}'"
        
        # Reset to defaults
        self.privacy = PrivacyConfig()
        self.user_agency = UserAgencyConfig()
        self.ai = AIConfig()
        self.ui = UIConfig()
        self.psychology = PsychologyConfig()
        self.security = SecurityConfig()
        self.integration = IntegrationConfig()
        
        # Remove user config file
        user_config_file = self.config_dir / "user_config.json"
        if user_config_file.exists():
            user_config_file.unlink()
        
        return True, "Configuration reset to privacy-first defaults"
    
    def export_config(self) -> Dict[str, Any]:
        """Export all configuration for user review"""
        return {
            "environment": self.environment.value,
            "privacy": asdict(self.privacy),
            "user_agency": asdict(self.user_agency),
            "ai": asdict(self.ai),
            "ui": asdict(self.ui),
            "psychology": asdict(self.psychology),
            "security": asdict(self.security),
            "integration": asdict(self.integration),
            "export_metadata": {
                "export_timestamp": "2024-01-15T10:00:00",  # Would use actual timestamp
                "config_version": "1.0",
                "privacy_statement": "This configuration belongs to the user and controls FlowState behavior"
            }
        }
    
    def validate_config(self) -> List[str]:
        """Validate configuration for security and privacy compliance"""
        issues = []
        
        # Privacy validation
        if self.privacy.telemetry_enabled and not self.privacy.anonymize_error_reports:
            issues.append("Telemetry enabled without anonymization")
        
        # Security validation
        if not self.security.encryption_at_rest:
            issues.append("Data encryption disabled")
        
        if self.security.session_timeout_minutes > 240:  # 4 hours
            issues.append("Session timeout too long for security")
        
        # AI validation
        if self.ai.minimum_confidence_threshold < 0.5:
            issues.append("AI confidence threshold too low")
        
        if self.ai.max_predictions_per_day > 20:
            issues.append("Too many AI predictions per day")
        
        # Psychology validation
        if not self.psychology.professional_boundaries_strict:
            issues.append("Professional boundaries not enforced")
        
        return issues
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get feature flags based on configuration"""
        return {
            # Core features (always enabled)
            "time_tracking": True,
            "pattern_analysis": True,
            
            # Privacy-controlled features
            "ai_suggestions": self.ai.local_processing_only,
            "team_collaboration": self.integration.team_features_opt_in,
            "calendar_sync": self.integration.calendar_sync_opt_in,
            
            # UI features
            "progressive_complexity": self.ui.earned_complexity_enabled,
            "accessibility_mode": self.ui.accessibility_first,
            
            # Psychology features
            "self_discovery": self.psychology.self_discovery_only,
            "crisis_detection": self.psychology.crisis_detection_enabled,
            
            # Security features
            "audit_logging": self.security.audit_log_enabled,
            "two_factor_auth": self.security.two_factor_auth_available,
            
            # Integration features
            "cloud_sync": self.integration.cloud_sync_opt_in,
            "third_party_apis": not self.integration.third_party_integrations_disabled
        }


# Environment-specific configuration instances
def get_config(environment: str = None) -> FlowStateConfig:
    """Get FlowState configuration for specified environment"""
    env = Environment(environment) if environment else Environment.DEVELOPMENT
    return FlowStateConfig(env)


# Default configurations for different environments
DEVELOPMENT_CONFIG = FlowStateConfig(Environment.DEVELOPMENT)
TESTING_CONFIG = FlowStateConfig(Environment.TESTING)
PRODUCTION_CONFIG = FlowStateConfig(Environment.PRODUCTION)


# Configuration validation and utility functions
def validate_environment_config(config: FlowStateConfig) -> bool:
    """Validate configuration meets security and privacy requirements"""
    issues = config.validate_config()
    if issues:
        print(f"Configuration issues found: {issues}")
        return False
    return True


def create_user_config_template() -> Dict[str, Any]:
    """Create template for user configuration customization"""
    return {
        "privacy": {
            "telemetry_enabled": False,
            "usage_analytics_opt_in": False,
            "data_retention_days": 365
        },
        "ui": {
            "dark_mode_default": True,
            "animation_reduced_motion": False,
            "font_size_scalable": True
        },
        "integration": {
            "calendar_sync_opt_in": False,
            "team_features_opt_in": False,
            "cloud_sync_opt_in": False
        }
    }


# Example usage and testing
if __name__ == "__main__":
    # Example of privacy-first configuration
    config = FlowStateConfig(Environment.DEVELOPMENT)
    
    # Validate configuration
    is_valid = validate_environment_config(config)
    print(f"Configuration valid: {is_valid}")
    
    # Export configuration for review
    config_export = config.export_config()
    print("Configuration export:", json.dumps(config_export, indent=2))
    
    # Check feature flags
    features = config.get_feature_flags()
    print("Enabled features:", [name for name, enabled in features.items() if enabled])
    
    # Example user customization
    user_overrides = {
        "ui": {"dark_mode_default": True},
        "integration": {"calendar_sync_opt_in": True}
    }
    
    success, message = config.save_user_config(user_overrides, user_confirmation=True)
    print(f"User config update: {message}")

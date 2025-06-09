
# FlowState Testing Configuration
# config/testing.py

import os
import tempfile
from datetime import timedelta
from unittest.mock import Mock

class TestingConfig:
    """
    Testing configuration for FlowState app.
    Enables comprehensive testing of human-centered pragmatic design principles
    while providing fast, reliable, and isolated test execution.
    """
    
    # Basic Flask Configuration
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test-secret-key-not-for-production'
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier testing
    
    # Database Configuration - In-memory SQLite for speed
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Disable SQL logging in tests for cleaner output
    
    # Test Data Isolation
    TEST_DATA_ISOLATION = True
    CLEANUP_AFTER_TESTS = True
    RESET_BETWEEN_TESTS = True
    
    # Privacy-First Data Storage (Test implementation)
    LOCAL_DATA_STORAGE = True
    USER_DATA_ENCRYPTION = False  # Disabled for test performance
    ENCRYPTION_KEY = 'test-encryption-key-32-chars-long'
    NO_CLOUD_BACKUP_DEFAULT = True
    DATA_EXPORT_ENABLED = True
    DATA_DELETION_IMMEDIATE = True
    
    # Progressive Complexity Testing
    DEFAULT_INTERFACE_MODE = 'boring'
    VISUAL_COMPLEXITY_LEVELS = {
        'boring': {
            'animations': False,
            'particles': False,
            'color_scheme': 'minimal',
            'ai_suggestions': False
        },
        'polished': {
            'animations': True,
            'particles': False,
            'color_scheme': 'enhanced',
            'ai_suggestions': 'basic'
        },
        'beautiful': {
            'animations': True,
            'particles': True,
            'color_scheme': 'full',
            'ai_suggestions': 'advanced'
        }
    }
    
    # User Agency & Control (Testing enforcement)
    USER_CONTROLS_ALL_FEATURES = True
    AI_OVERRIDE_ALWAYS_AVAILABLE = True
    FEATURE_FLAGS_USER_CONTROLLED = True
    NO_FORCED_FEATURES = True
    
    # AI/ML Configuration (Test mocks)
    AI_PROCESSING_MODE = 'mock'
    AI_CONFIDENCE_THRESHOLD = 0.7
    AI_FALLBACK_TO_RULES = True
    AI_UNCERTAINTY_DISPLAY = True
    
    # Mock AI responses for consistent testing
    MOCK_AI_RESPONSES = True
    MOCK_AI_CONFIDENCE_LEVELS = [0.3, 0.5, 0.7, 0.9]
    MOCK_PROCRASTINATION_PATTERNS = True
    MOCK_FLOW_STATE_DETECTION = True
    
    # Honest Limitations Testing
    SHOW_CONFIDENCE_LEVELS = True
    ACKNOWLEDGE_UNCERTAINTY = True
    CLEAR_SCOPE_LIMITATIONS = True
    TEST_TRANSPARENCY_FEATURES = True
    
    # Performance Configuration (Fast for tests)
    MAX_RESPONSE_TIME_MS = 100  # Faster for unit tests
    PERFORMANCE_MONITORING = False  # Disabled for test speed
    AUTO_DOWNGRADE_ON_ISSUES = False
    BATTERY_OPTIMIZATION = False
    
    # Cache Configuration (Disabled for isolation)
    CACHE_TYPE = 'null'
    CACHE_DEFAULT_TIMEOUT = 0
    
    # Session Configuration (Short for tests)
    SESSION_LIFETIME = timedelta(minutes=5)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API Configuration (Testing)
    API_RATE_LIMITING = False  # Disabled for test performance
    API_VERSIONING = 'v1'
    CORS_ENABLED = True
    
    # Feature Toggles (Test scenarios)
    FEATURES = {
        # Core Features (Always Available)
        'basic_time_tracking': True,
        'simple_reporting': True,
        'data_export': True,
        
        # Progressive Features (Configurable for testing)
        'visual_enhancements': True,  # Enabled for testing
        'ai_suggestions': True,       # Enabled with mocks
        'advanced_analytics': True,   # Enabled for testing
        'team_features': True,        # Enabled for testing
        
        # Experimental Features (Test controlled)
        'biometric_integration': False,
        'smart_home_integration': False,
        'environmental_adaptation': False,
        
        # Professional Features (Mock implementations)
        'psychology_assessment': False,
        'therapeutic_referral': True,
        'professional_coaching': True,
    }
    
    # Test User Scenarios
    TEST_USER_SCENARIOS = {
        'new_user': {
            'interface_mode': 'boring',
            'features_unlocked': ['basic_time_tracking'],
            'ai_enabled': False,
            'usage_days': 0
        },
        'consistent_user': {
            'interface_mode': 'polished',
            'features_unlocked': ['basic_time_tracking', 'visual_enhancements'],
            'ai_enabled': True,
            'usage_days': 21
        },
        'power_user': {
            'interface_mode': 'beautiful',
            'features_unlocked': ['all'],
            'ai_enabled': True,
            'usage_days': 90,
            'subscription': 'pro'
        },
        'enterprise_user': {
            'interface_mode': 'boring',  # Enterprise prefers functional
            'features_unlocked': ['all_enterprise'],
            'ai_enabled': True,
            'subscription': 'enterprise',
            'team_features': True
        }
    }
    
    # Neurodiversity Testing Scenarios
    NEURODIVERSITY_TEST_SCENARIOS = {
        'adhd_user': {
            'attention_style': 'hyperfocus_prone',
            'stimulation_needs': 'high',
            'interface_preferences': 'reduced_clutter',
            'notification_sensitivity': 'low'
        },
        'autism_user': {
            'sensory_processing': 'sensitive',
            'routine_needs': 'high_predictability',
            'change_tolerance': 'low',
            'communication_style': 'direct'
        },
        'dyslexia_user': {
            'reading_preferences': 'large_fonts',
            'color_needs': 'high_contrast',
            'processing_time': 'extended',
            'format_preferences': 'visual_aids'
        }
    }
    
    # Cultural Testing Scenarios
    CULTURAL_TEST_SCENARIOS = {
        'western_linear': {
            'time_orientation': 'linear',
            'communication_style': 'direct',
            'achievement_style': 'individual',
            'feedback_preference': 'explicit'
        },
        'eastern_cyclical': {
            'time_orientation': 'cyclical',
            'communication_style': 'indirect',
            'achievement_style': 'collective',
            'feedback_preference': 'contextual'
        },
        'polychronic': {
            'time_orientation': 'flexible',
            'multitasking_preference': 'high',
            'relationship_priority': 'high',
            'schedule_flexibility': 'preferred'
        }
    }
    
    # Mock External Services
    MOCK_EXTERNAL_SERVICES = True
    MOCK_PROFESSIONAL_REFERRALS = True
    MOCK_SMART_HOME_INTEGRATIONS = True
    MOCK_CALENDAR_INTEGRATIONS = True
    MOCK_BIOMETRIC_DATA = True
    
    # Professional Boundaries Testing
    PROFESSIONAL_REFERRAL_ENABLED = True
    CLEAR_SCOPE_BOUNDARIES = True
    LICENSED_PARTNERSHIPS = True
    CRISIS_DETECTION = True
    TEST_REFERRAL_TRIGGERS = True
    
    # Anti-Surveillance Testing
    NO_COVERT_TRACKING = True
    TRANSPARENT_DATA_COLLECTION = True
    USER_AUDIT_TRAIL = True
    SURVEILLANCE_PREVENTION = True
    TEST_PRIVACY_CONTROLS = True
    
    # Test-Specific Settings
    LOG_LEVEL = 'WARNING'  # Reduce log noise in tests
    MAIL_SUPPRESS_SEND = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    
    # Test Database Utilities
    TEST_DB_CLEANUP = True
    TEST_DATA_FIXTURES = True
    FACTORY_BOY_RANDOM_SEED = 12345  # Consistent test data
    
    # Mock Data Generators
    MOCK_PRODUCTIVITY_DATA = {
        'daily_patterns': True,
        'weekly_trends': True,
        'procrastination_episodes': True,
        'flow_state_sessions': True,
        'energy_levels': True,
        'task_completion_rates': True
    }
    
    # Test Validation Rules
    TEST_VALIDATION = {
        'user_agency_preserved': True,
        'privacy_controls_functional': True,
        'accessibility_features_working': True,
        'progressive_complexity_enforced': True,
        'professional_boundaries_respected': True,
        'transparency_features_active': True
    }

class TestingUtils:
    """Utilities for testing FlowState functionality"""
    
    @staticmethod
    def create_test_user(scenario='new_user'):
        """Create a test user with specific scenario characteristics"""
        scenario_config = TestingConfig.TEST_USER_SCENARIOS.get(scenario, {})
        return {
            'id': f'test_user_{scenario}',
            'interface_mode': scenario_config.get('interface_mode', 'boring'),
            'features_unlocked': scenario_config.get('features_unlocked', []),
            'ai_enabled': scenario_config.get('ai_enabled', False),
            'usage_days': scenario_config.get('usage_days', 0),
            'subscription': scenario_config.get('subscription', 'free'),
            'created_for_test': True
        }
    
    @staticmethod
    def create_neurodivergent_user(neurodiversity_type='adhd_user'):
        """Create a test user with specific neurodiversity characteristics"""
        base_user = TestingUtils.create_test_user('consistent_user')
        neurodiversity_config = TestingConfig.NEURODIVERSITY_TEST_SCENARIOS.get(neurodiversity_type, {})
        base_user.update({
            'neurodiversity_profile': neurodiversity_config,
            'accessibility_features_enabled': True,
            'custom_interface_settings': neurodiversity_config
        })
        return base_user
    
    @staticmethod
    def create_cultural_context_user(cultural_type='western_linear'):
        """Create a test user with specific cultural context"""
        base_user = TestingUtils.create_test_user('consistent_user')
        cultural_config = TestingConfig.CULTURAL_TEST_SCENARIOS.get(cultural_type, {})
        base_user.update({
            'cultural_profile': cultural_config,
            'localization_preferences': cultural_config,
            'communication_adaptations': cultural_config
        })
        return base_user
    
    @staticmethod
    def mock_ai_response(confidence_level=0.7, suggestion_type='time_blocking'):
        """Generate mock AI response for testing"""
        return {
            'suggestion': f'Mock {suggestion_type} suggestion',
            'confidence': confidence_level,
            'reasoning': f'Based on mock data analysis for {suggestion_type}',
            'uncertainty_acknowledged': confidence_level < 0.8,
            'user_override_available': True,
            'explanation_available': True
        }
    
    @staticmethod
    def mock_procrastination_analysis(severity='moderate'):
        """Generate mock procrastination analysis"""
        severity_configs = {
            'low': {'confidence': 0.9, 'intervention': 'gentle_nudge'},
            'moderate': {'confidence': 0.7, 'intervention': 'break_down_task'},
            'high': {'confidence': 0.8, 'intervention': 'professional_referral'}
        }
        config = severity_configs.get(severity, severity_configs['moderate'])
        
        return {
            'severity': severity,
            'confidence': config['confidence'],
            'suggested_intervention': config['intervention'],
            'root_cause_analysis': f'Mock analysis for {severity} procrastination',
            'professional_referral_needed': severity == 'high',
            'user_agency_preserved': True
        }
    
    @staticmethod
    def mock_flow_state_session(duration_minutes=45, quality='high'):
        """Generate mock flow state session data"""
        return {
            'duration_minutes': duration_minutes,
            'quality': quality,
            'interruptions': 0 if quality == 'high' else 2,
            'task_completion': 0.9 if quality == 'high' else 0.6,
            'user_satisfaction': 0.8 if quality == 'high' else 0.5,
            'conditions': {
                'environment': 'quiet',
                'energy_level': 'high',
                'task_type': 'creative'
            }
        }
    
    @staticmethod
    def assert_user_agency_preserved(user_interaction):
        """Assert that user agency principles are maintained"""
        assert user_interaction.get('user_override_available', False), "User override must be available"
        assert user_interaction.get('user_controls_enabled', False), "User controls must be enabled"
        assert not user_interaction.get('forced_features', False), "No features should be forced"
        assert user_interaction.get('transparency_provided', False), "Transparency must be provided"
    
    @staticmethod
    def assert_privacy_protected(data_interaction):
        """Assert that privacy principles are maintained"""
        assert data_interaction.get('local_processing', False), "Data should be processed locally"
        assert data_interaction.get('user_consent_obtained', False), "User consent must be obtained"
        assert data_interaction.get('deletion_available', False), "Data deletion must be available"
        assert not data_interaction.get('covert_tracking', False), "No covert tracking allowed"
    
    @staticmethod
    def assert_accessibility_supported(interface_interaction):
        """Assert that accessibility principles are maintained"""
        assert interface_interaction.get('screen_reader_compatible', False), "Must be screen reader compatible"
        assert interface_interaction.get('keyboard_navigation', False), "Must support keyboard navigation"
        assert interface_interaction.get('customization_available', False), "Customization must be available"
        assert interface_interaction.get('multiple_interaction_modes', False), "Multiple interaction modes required"
    
    @staticmethod
    def reset_test_environment():
        """Reset testing environment to clean state"""
        # Clear mock data
        # Reset feature flags
        # Clear user sessions
        # Reset AI mock responses
        pass
    
    @staticmethod
    def validate_expert_consensus_principles(app_state):
        """Validate that expert consensus principles are maintained"""
        validations = []
        
        # Progressive Complexity (UX Expert)
        if app_state.get('default_mode') != 'boring':
            validations.append("Must start with boring mode")
        
        # User Agency (All Experts)
        if not app_state.get('user_controls_all_features'):
            validations.append("User must control all features")
        
        # Privacy First (All Experts)
        if not app_state.get('local_data_storage'):
            validations.append("Must use local data storage")
        
        # Honest Limitations (All Experts)
        if not app_state.get('show_confidence_levels'):
            validations.append("Must show AI confidence levels")
        
        # Professional Boundaries (Psychology Expert)
        if not app_state.get('professional_referral_available'):
            validations.append("Professional referral must be available")
        
        # Anti-Surveillance (Workplace Expert)
        if not app_state.get('transparent_data_collection'):
            validations.append("Data collection must be transparent")
        
        if validations:
            raise AssertionError(f"Expert consensus validation failed: {'; '.join(validations)}")
        
        return True

# Test Environment Setup
class TestEnvironment:
    """Test environment management"""
    
    @classmethod
    def setup(cls):
        """Set up test environment"""
        # Create temporary directories
        cls.temp_dir = tempfile.mkdtemp()
        
        # Initialize mock services
        cls.mock_ai_service = Mock()
        cls.mock_professional_service = Mock()
        cls.mock_external_integrations = Mock()
        
        # Set up test database
        cls.setup_test_database()
        
        # Configure logging for tests
        cls.setup_test_logging()
    
    @classmethod
    def teardown(cls):
        """Clean up test environment"""
        # Clean up temporary files
        import shutil
        if hasattr(cls, 'temp_dir'):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)
        
        # Reset mocks
        if hasattr(cls, 'mock_ai_service'):
            cls.mock_ai_service.reset_mock()
        
        # Clear test data
        cls.cleanup_test_database()
    
    @classmethod
    def setup_test_database(cls):
        """Set up isolated test database"""
        # Create in-memory database
        # Run migrations
        # Seed with test data
        pass
    
    @classmethod
    def cleanup_test_database(cls):
        """Clean up test database"""
        # Drop all tables
        # Clear connections
        pass
    
    @classmethod
    def setup_test_logging(cls):
        """Configure logging for tests"""
        import logging
        logging.getLogger().setLevel(logging.WARNING)  # Reduce noise
        
        # Disable third-party loggers
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)

# Pytest fixtures and test configuration
TEST_FIXTURES = {
    'new_user': lambda: TestingUtils.create_test_user('new_user'),
    'power_user': lambda: TestingUtils.create_test_user('power_user'),
    'adhd_user': lambda: TestingUtils.create_neurodivergent_user('adhd_user'),
    'autism_user': lambda: TestingUtils.create_neurodivergent_user('autism_user'),
    'enterprise_user': lambda: TestingUtils.create_test_user('enterprise_user'),
    'western_user': lambda: TestingUtils.create_cultural_context_user('western_linear'),
    'eastern_user': lambda: TestingUtils.create_cultural_context_user('eastern_cyclical')
}

# Validation on import
if __name__ == '__main__':
    print("✅ Testing configuration loaded successfully")
    print("🧪 FlowState testing environment configured with:")
    print("   - Comprehensive user scenario testing")
    print("   - Neurodiversity and cultural adaptation testing")
    print("   - Mock AI and external service integration")
    print("   - Privacy and user agency validation")
    print("   - Professional boundary testing")
    print("   - Expert consensus principle validation")
    print("   - Performance and accessibility testing")
    
    # Validate test scenarios
    for scenario_name in TestingConfig.TEST_USER_SCENARIOS:
        user = TestingUtils.create_test_user(scenario_name)
        print(f"   - {scenario_name}: {user['interface_mode']} mode, {len(user['features_unlocked'])} features")

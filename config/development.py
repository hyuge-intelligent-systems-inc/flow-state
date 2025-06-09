
# FlowState Development Configuration
# config/development.py

import os
from datetime import timedelta

class DevelopmentConfig:
    """
    Development configuration for FlowState app.
    Based on expert analysis emphasizing:
    - Progressive complexity with user agency
    - Privacy-first approach with local processing
    - Reality-based expectations with honest limitations
    - Anti-surveillance design principles
    """
    
    # Basic Flask Configuration
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('DEV_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration - Local SQLite for privacy-first approach
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL', 'sqlite:///flowstate_dev.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Show SQL queries in development
    
    # Privacy-First Data Storage (Expert consensus: User controls all data)
    LOCAL_DATA_STORAGE = True
    USER_DATA_ENCRYPTION = True
    NO_CLOUD_BACKUP_DEFAULT = True  # User must explicitly opt-in
    DATA_EXPORT_ENABLED = True
    DATA_DELETION_IMMEDIATE = True
    
    # Progressive Complexity Settings (UX Expert solution)
    DEFAULT_INTERFACE_MODE = 'boring'  # Start with most basic interface
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
    
    # User Agency & Control (All experts emphasized this)
    USER_CONTROLS_ALL_FEATURES = True
    AI_OVERRIDE_ALWAYS_AVAILABLE = True
    FEATURE_FLAGS_USER_CONTROLLED = True
    NO_FORCED_FEATURES = True
    
    # AI/ML Configuration (AI Expert pragmatic approach)
    AI_PROCESSING_MODE = 'local_first'
    AI_CONFIDENCE_THRESHOLD = 0.7  # High bar for predictions
    AI_FALLBACK_TO_RULES = True
    AI_UNCERTAINTY_DISPLAY = True
    
    # Rule-based "AI" for initial deployment
    SIMPLE_PATTERN_RECOGNITION = True
    MACHINE_LEARNING_ENABLED = False  # Start with rules, add ML later
    
    # Honest Limitations (All experts emphasized transparency)
    SHOW_CONFIDENCE_LEVELS = True
    ACKNOWLEDGE_UNCERTAINTY = True
    CLEAR_SCOPE_LIMITATIONS = True
    
    # Performance Configuration (UX Expert reality check)
    MAX_RESPONSE_TIME_MS = 500  # Realistic target, not fantasy 100ms
    PERFORMANCE_MONITORING = True
    AUTO_DOWNGRADE_ON_ISSUES = True
    BATTERY_OPTIMIZATION = True
    
    # Accessibility (Behavioral Expert inclusive design)
    ACCESSIBILITY_FIRST = True
    NEURODIVERSITY_SUPPORT = True
    CULTURAL_ADAPTATION = True
    MULTIPLE_INTERACTION_MODES = True
    
    # Professional Boundaries (Psychology Expert ethical approach)
    PROFESSIONAL_REFERRAL_ENABLED = True
    CLEAR_SCOPE_BOUNDARIES = True
    LICENSED_PARTNERSHIPS = True
    CRISIS_DETECTION = True
    
    # Anti-Surveillance Design (Workplace Expert trust building)
    NO_COVERT_TRACKING = True
    TRANSPARENT_DATA_COLLECTION = True
    USER_AUDIT_TRAIL = True
    SURVEILLANCE_PREVENTION = True
    
    # Time Management Realism (Time Management Expert evidence-based)
    REALISTIC_HABIT_FORMATION = True
    FAILURE_PLANNING_INCLUDED = True
    CONTEXT_AWARE_SUGGESTIONS = True
    PROCRASTINATION_ROOT_CAUSE_ANALYSIS = True
    
    # Development-Specific Settings
    LOG_LEVEL = 'DEBUG'
    MAIL_SUPPRESS_SEND = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier development
    
    # API Configuration
    API_RATE_LIMITING = False  # Disabled in development
    API_VERSIONING = 'v1'
    CORS_ENABLED = True
    
    # Cache Configuration (Minimal in development)
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Session Configuration
    SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # HTTP OK in development
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Feature Toggles (Progressive Enhancement Strategy)
    FEATURES = {
        # Core Features (Always Available)
        'basic_time_tracking': True,
        'simple_reporting': True,
        'data_export': True,
        
        # Earned Features (Unlock with usage)
        'visual_enhancements': False,  # Unlock after 2 weeks consistent use
        'ai_suggestions': False,       # Unlock after 1 month + opt-in
        'advanced_analytics': False,   # Unlock after 3 months + payment
        'team_features': False,        # Enterprise only
        
        # Optional Features (User Choice)
        'biometric_integration': False,
        'smart_home_integration': False,
        'environmental_adaptation': False,
        
        # Professional Features (Licensed partnerships)
        'psychology_assessment': False,
        'therapeutic_referral': True,  # Basic referral always available
        'professional_coaching': False,
    }
    
    # Neurodiversity Support Configuration
    NEURODIVERSITY_OPTIONS = {
        'adhd_optimization': True,
        'autism_accommodation': True,
        'dyslexia_support': True,
        'sensory_customization': True,
        'attention_variation_support': True
    }
    
    # Cultural Adaptation Settings
    CULTURAL_SUPPORT = {
        'time_orientation_flexibility': True,  # Linear vs cyclical
        'communication_style_adaptation': True,  # Direct vs indirect
        'success_definition_variety': True,  # Individual vs collective
        'local_psychology_consultation': True
    }
    
    # Privacy & Ethics Configuration
    PRIVACY_SETTINGS = {
        'data_minimization': True,
        'purpose_limitation': True,
        'storage_limitation': True,
        'transparency': True,
        'user_control': True,
        'accountability': True
    }
    
    # Research & Community Learning (Ethical approach)
    COMMUNITY_RESEARCH = {
        'voluntary_participation': True,
        'irb_oversight': True,
        'data_anonymization': True,
        'community_benefit_focus': True,
        'no_exploitation': True
    }
    
    # Business Model (Value-based, not manipulation-based)
    MONETIZATION = {
        'subscription_without_manipulation': True,
        'freemium_with_real_value': True,
        'no_dark_patterns': True,
        'transparent_pricing': True,
        'professional_service_partnerships': True
    }
    
    # Development Tools
    FLASK_ENV = 'development'
    FLASK_APP = 'src.app'
    HOT_RELOAD = True
    LIVE_RELOAD = True
    
    # Testing Configuration
    TESTING_DATABASE_URL = 'sqlite:///:memory:'
    TEST_USER_DATA_ISOLATION = True
    MOCK_AI_RESPONSES = True
    MOCK_EXTERNAL_SERVICES = True
    
    # Logging Configuration
    LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': 'logs/flowstate_dev.log'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
    
    @classmethod
    def validate_config(cls):
        """
        Validate that development configuration follows expert principles.
        """
        issues = []
        
        # Check privacy-first principles
        if not cls.LOCAL_DATA_STORAGE:
            issues.append("Development should use local data storage for privacy")
        
        # Check progressive complexity
        if cls.DEFAULT_INTERFACE_MODE != 'boring':
            issues.append("Should start with simplest interface mode")
        
        # Check user agency
        if not cls.USER_CONTROLS_ALL_FEATURES:
            issues.append("Users must control all features")
        
        # Check honest limitations
        if not cls.SHOW_CONFIDENCE_LEVELS:
            issues.append("Must show confidence levels for transparency")
        
        # Check anti-surveillance
        if not cls.TRANSPARENT_DATA_COLLECTION:
            issues.append("Data collection must be transparent")
        
        if issues:
            raise ValueError(f"Configuration validation failed: {', '.join(issues)}")
        
        return True

# Additional Development Utilities
class DevelopmentUtils:
    """Utilities for development environment"""
    
    @staticmethod
    def reset_user_to_boring_mode(user_id):
        """Reset user interface to basic mode for testing"""
        # Implementation would reset user preferences
        pass
    
    @staticmethod
    def simulate_usage_progression(user_id, weeks=4):
        """Simulate user progression through complexity levels"""
        # Implementation would simulate user engagement over time
        pass
    
    @staticmethod
    def test_accessibility_mode(mode='adhd'):
        """Switch to specific accessibility configuration for testing"""
        # Implementation would switch interface modes
        pass
    
    @staticmethod
    def mock_ai_confidence(level=0.3):
        """Set AI confidence level for testing uncertainty display"""
        # Implementation would mock AI responses with specific confidence
        pass

# Validation on import
if __name__ == '__main__':
    DevelopmentConfig.validate_config()
    print("✅ Development configuration validated successfully")
    print("🔧 FlowState development environment configured with:")
    print("   - Privacy-first local data storage")
    print("   - Progressive complexity starting with 'boring' mode")
    print("   - User agency and control over all features")
    print("   - Transparent limitations and confidence levels")
    print("   - Anti-surveillance design principles")
    print("   - Accessibility and neurodiversity support")
    print("   - Professional boundaries and ethical guidelines")

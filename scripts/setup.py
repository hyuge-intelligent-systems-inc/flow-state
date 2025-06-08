
#!/usr/bin/env python3
"""
FlowState Setup Script
Privacy-First Productivity Application

This setup script follows FlowState's core principles:
- User agency preserved throughout setup
- Privacy-first with explicit consent
- Honest limitations communicated upfront
- Professional boundaries maintained
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class FlowStateSetup:
    """
    Privacy-first setup with user agency preservation
    """
    
    def __init__(self):
        self.setup_log = []
        self.user_choices = {}
        self.system_info = self._get_system_info()
        self.requirements_met = True
        
    def _get_system_info(self) -> Dict:
        """Get system information for compatibility checking"""
        return {
            'platform': platform.system(),
            'python_version': platform.python_version(),
            'architecture': platform.machine(),
            'os_version': platform.version()
        }
    
    def _log(self, message: str, level: str = "INFO"):
        """Log setup progress with transparency"""
        log_entry = f"[{level}] {message}"
        self.setup_log.append(log_entry)
        print(log_entry)
    
    def _get_user_consent(self, question: str, default: bool = False) -> bool:
        """Get explicit user consent with clear defaults"""
        default_text = "Y/n" if default else "y/N"
        response = input(f"{question} [{default_text}]: ").strip().lower()
        
        if not response:
            return default
        return response in ['y', 'yes', 'true', '1']
    
    def welcome_message(self):
        """Display welcome with honest expectations"""
        print("\n" + "="*60)
        print("🌊 FlowState Setup - Privacy-First Productivity")
        print("="*60)
        print("\nWelcome to FlowState! This setup will:")
        print("• Install FlowState with privacy-first defaults")
        print("• Give you complete control over data and features")
        print("• Start simple - you earn complexity over time")
        print("• Respect your choices about data and AI")
        print("\nWhat FlowState WILL NOT do:")
        print("• Track you without explicit permission")
        print("• Share data without your consent")
        print("• Make decisions for you")
        print("• Promise impossible AI capabilities")
        print("\n" + "-"*60)
    
    def check_system_requirements(self) -> bool:
        """Check system compatibility with honest assessment"""
        self._log("Checking system compatibility...")
        
        # Check Python version
        if sys.version_info < (3.8, 0):
            self._log("❌ Python 3.8+ required for security features", "ERROR")
            self.requirements_met = False
        else:
            self._log(f"✅ Python {platform.python_version()} compatible")
        
        # Check available disk space
        try:
            free_space = self._get_free_space()
            if free_space < 100:  # 100MB minimum
                self._log(f"⚠️  Low disk space: {free_space}MB available", "WARNING")
            else:
                self._log(f"✅ Sufficient disk space: {free_space}MB available")
        except Exception as e:
            self._log(f"⚠️  Could not check disk space: {e}", "WARNING")
        
        # Check for required system libraries
        required_libs = ['sqlite3']
        for lib in required_libs:
            try:
                __import__(lib)
                self._log(f"✅ {lib} available")
            except ImportError:
                self._log(f"❌ {lib} not available", "ERROR")
                self.requirements_met = False
        
        return self.requirements_met
    
    def _get_free_space(self) -> int:
        """Get available disk space in MB"""
        if platform.system() == "Windows":
            import shutil
            free_bytes = shutil.disk_usage('.').free
        else:
            statvfs = os.statvfs('.')
            free_bytes = statvfs.f_frsize * statvfs.f_bavail
        
        return free_bytes // (1024 * 1024)  # Convert to MB
    
    def configure_privacy_settings(self):
        """Configure privacy with explicit user choices"""
        self._log("Setting up privacy controls...")
        print("\n📋 Privacy Configuration")
        print("-" * 30)
        
        privacy_choices = {}
        
        # Data storage location
        print("\n1. Data Storage Location:")
        print("   • LOCAL: All data stays on your device (most private)")
        print("   • CLOUD: Optional encrypted cloud backup (convenience)")
        
        use_cloud = self._get_user_consent(
            "Enable optional cloud backup for convenience?", 
            default=False
        )
        privacy_choices['cloud_backup'] = use_cloud
        
        if use_cloud:
            print("   ⚠️  Cloud backup uses encryption, but local-only is more private")
        
        # AI analysis level
        print("\n2. AI Analysis Level:")
        print("   • BASIC: Simple pattern recognition (privacy-focused)")
        print("   • ADVANCED: More insights, uses more data")
        
        advanced_ai = self._get_user_consent(
            "Enable advanced AI insights (uses more personal data)?", 
            default=False
        )
        privacy_choices['advanced_ai'] = advanced_ai
        
        # Calendar integration
        print("\n3. Calendar Integration:")
        print("   • Helps with focus time suggestions")
        print("   • Event titles are hashed for privacy")
        
        calendar_integration = self._get_user_consent(
            "Enable privacy-preserving calendar integration?", 
            default=False
        )
        privacy_choices['calendar_integration'] = calendar_integration
        
        # Team features
        print("\n4. Team Features:")
        print("   • Share insights with colleagues (anonymized)")
        print("   • Only aggregated patterns, never individual data")
        
        team_features = self._get_user_consent(
            "Enable team collaboration features?", 
            default=False
        )
        privacy_choices['team_features'] = team_features
        
        self.user_choices.update(privacy_choices)
        self._log("Privacy settings configured based on user choices")
    
    def install_dependencies(self) -> bool:
        """Install required packages with user consent"""
        self._log("Installing dependencies...")
        
        # Check if pip is available
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            self._log("❌ pip not available - cannot install dependencies", "ERROR")
            return False
        
        # Core dependencies
        core_deps = [
            'cryptography>=3.4.8',  # For data encryption
            'requests>=2.25.1',     # For API calls
            'python-dateutil>=2.8.1',  # For date handling
            'pydantic>=1.8.0',     # For data validation
        ]
        
        # Optional dependencies based on user choices
        optional_deps = []
        
        if self.user_choices.get('calendar_integration'):
            optional_deps.extend([
                'google-auth>=2.0.0',
                'google-auth-oauthlib>=0.4.0',
                'google-api-python-client>=2.0.0'
            ])
        
        if self.user_choices.get('advanced_ai'):
            optional_deps.extend([
                'scikit-learn>=1.0.0',
                'numpy>=1.21.0'
            ])
        
        # Install dependencies
        all_deps = core_deps + optional_deps
        
        print(f"\nInstalling {len(all_deps)} packages...")
        for dep in all_deps:
            try:
                self._log(f"Installing {dep}...")
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '--quiet', dep
                ], check=True)
                self._log(f"✅ {dep} installed")
            except subprocess.CalledProcessError:
                self._log(f"❌ Failed to install {dep}", "ERROR")
                return False
        
        return True
    
    def create_configuration(self):
        """Create user configuration file"""
        self._log("Creating configuration file...")
        
        config = {
            'version': '1.0.0',
            'setup_date': self._get_current_timestamp(),
            'system_info': self.system_info,
            'user_choices': self.user_choices,
            'privacy_settings': {
                'data_retention_days': 365,
                'anonymous_usage_stats': False,
                'crash_reporting': False,
                'feature_usage_tracking': False
            },
            'ui_settings': {
                'complexity_level': 'simple',  # Start simple
                'theme': 'auto',
                'accessibility_mode': 'standard'
            },
            'ai_settings': {
                'confidence_threshold': 0.7,
                'uncertainty_disclosure': True,
                'prediction_explanations': True,
                'fallback_to_simple': True
            }
        }
        
        # Create config directory
        config_dir = Path.home() / '.flowstate'
        config_dir.mkdir(exist_ok=True)
        
        # Write configuration
        config_file = config_dir / 'config.json'
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Set appropriate permissions (user only)
        if platform.system() != "Windows":
            os.chmod(config_file, 0o600)
        
        self._log(f"Configuration saved to {config_file}")
    
    def create_directory_structure(self):
        """Create necessary directories"""
        self._log("Creating directory structure...")
        
        base_dir = Path.home() / '.flowstate'
        directories = [
            base_dir / 'data',
            base_dir / 'exports',
            base_dir / 'logs',
            base_dir / 'backups'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self._log(f"Created directory: {directory}")
    
    def setup_database(self):
        """Initialize local database"""
        self._log("Setting up local database...")
        
        try:
            import sqlite3
            db_path = Path.home() / '.flowstate' / 'data' / 'flowstate.db'
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create basic tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS time_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    category TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Set database permissions (user only)
            if platform.system() != "Windows":
                os.chmod(db_path, 0o600)
            
            self._log("Database initialized successfully")
        
        except Exception as e:
            self._log(f"❌ Database setup failed: {e}", "ERROR")
            return False
        
        return True
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def create_launch_script(self):
        """Create platform-specific launch script"""
        self._log("Creating launch script...")
        
        flowstate_dir = Path.home() / '.flowstate'
        
        if platform.system() == "Windows":
            # Create Windows batch file
            script_content = f"""@echo off
cd /d "{Path.cwd()}"
python -m src.main
pause
"""
            script_path = flowstate_dir / 'launch_flowstate.bat'
        else:
            # Create Unix shell script
            script_content = f"""#!/bin/bash
cd "{Path.cwd()}"
python -m src.main
"""
            script_path = flowstate_dir / 'launch_flowstate.sh'
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable on Unix systems
        if platform.system() != "Windows":
            os.chmod(script_path, 0o755)
        
        self._log(f"Launch script created: {script_path}")
    
    def final_setup_summary(self):
        """Show setup completion summary"""
        print("\n" + "="*60)
        print("🎉 FlowState Setup Complete!")
        print("="*60)
        
        print("\n📊 Setup Summary:")
        print(f"• Privacy level: {'Privacy-focused' if not self.user_choices.get('advanced_ai') else 'Balanced'}")
        print(f"• Data storage: {'Local only' if not self.user_choices.get('cloud_backup') else 'Local + encrypted cloud'}")
        print(f"• Calendar integration: {'Enabled' if self.user_choices.get('calendar_integration') else 'Disabled'}")
        print(f"• Team features: {'Enabled' if self.user_choices.get('team_features') else 'Disabled'}")
        
        print("\n🚀 Next Steps:")
        print("1. Run FlowState:")
        if platform.system() == "Windows":
            print(f"   {Path.home() / '.flowstate' / 'launch_flowstate.bat'}")
        else:
            print(f"   {Path.home() / '.flowstate' / 'launch_flowstate.sh'}")
        
        print("\n2. Or run directly:")
        print("   python -m src.main")
        
        print("\n📖 Documentation:")
        print("   docs/user-guide.md - Complete user guide")
        print("   docs/privacy-policy.md - Privacy information")
        
        print("\n🔒 Your Privacy:")
        print("• Configuration stored in: ~/.flowstate/config.json")
        print("• Data stored locally in: ~/.flowstate/data/")
        print("• You can export or delete all data anytime")
        
        print("\n⚠️  Remember:")
        print("• FlowState starts simple - you earn complexity")
        print("• All features are optional and user-controlled")
        print("• AI has limitations and will tell you when uncertain")
        
        print("\n" + "="*60)
    
    def save_setup_log(self):
        """Save setup log for troubleshooting"""
        log_file = Path.home() / '.flowstate' / 'logs' / 'setup.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'w') as f:
            f.write("FlowState Setup Log\n")
            f.write(f"Setup Date: {self._get_current_timestamp()}\n")
            f.write(f"System: {self.system_info}\n")
            f.write(f"User Choices: {self.user_choices}\n")
            f.write("\nSetup Steps:\n")
            f.write("\n".join(self.setup_log))
        
        self._log(f"Setup log saved to {log_file}")
    
    def run_setup(self):
        """Run complete setup process"""
        try:
            self.welcome_message()
            
            # System checks
            if not self.check_system_requirements():
                print("\n❌ System requirements not met. Please resolve issues and try again.")
                return False
            
            # User configuration
            self.configure_privacy_settings()
            
            # Installation
            if not self.install_dependencies():
                print("\n❌ Dependency installation failed. Please check your internet connection and try again.")
                return False
            
            # Setup
            self.create_directory_structure()
            self.create_configuration()
            
            if not self.setup_database():
                print("\n❌ Database setup failed. Please check permissions and try again.")
                return False
            
            self.create_launch_script()
            self.save_setup_log()
            
            # Success
            self.final_setup_summary()
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Setup interrupted by user")
            return False
        except Exception as e:
            self._log(f"❌ Setup failed with error: {e}", "ERROR")
            print(f"\n❌ Setup failed: {e}")
            print("Please check the setup log for details.")
            return False


def main():
    """Main setup entry point"""
    setup = FlowStateSetup()
    success = setup.run_setup()
    
    if success:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Please resolve issues and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()

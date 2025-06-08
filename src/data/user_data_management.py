

"""
FlowState User Data Management
Based on expert analysis: Complete user data ownership with privacy-first design

Key principles implemented:
- Users own and control all their data
- Granular privacy controls with transparent data handling
- Complete data portability and deletion capabilities
- Privacy-preserving data processing and storage
- Honest limitations about data security and usage
"""

import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class PrivacyLevel(Enum):
    """Privacy levels for different types of data sharing"""
    PRIVATE = "private"  # Never shared, local only
    ANONYMOUS = "anonymous"  # Aggregated anonymously
    AGGREGATED = "aggregated"  # Combined with others
    TEAM_VISIBLE = "team_visible"  # Visible to team members
    FULL_COLLABORATION = "full_collaboration"  # Complete sharing


class DataCategory(Enum):
    """Categories of user data for granular privacy control"""
    TIME_ENTRIES = "time_entries"
    PRODUCTIVITY_PATTERNS = "productivity_patterns"
    ENERGY_LEVELS = "energy_levels"
    FOCUS_QUALITY = "focus_quality"
    SELF_DISCOVERY_INSIGHTS = "self_discovery_insights"
    AI_INTERACTIONS = "ai_interactions"
    TEAM_COLLABORATION = "team_collaboration"
    USER_PREFERENCES = "user_preferences"


@dataclass
class DataExportManifest:
    """Comprehensive manifest of all user data for export"""
    export_id: str
    user_id: str
    export_timestamp: datetime.datetime
    data_categories: List[str]
    total_records: int
    date_range: Tuple[datetime.date, datetime.date]
    privacy_settings: Dict[str, str]
    data_ownership_statement: str
    deletion_instructions: str


class UserDataManager:
    """
    Manages all user data with complete ownership and privacy controls
    Based on expert analysis emphasizing user data sovereignty
    """
    
    def __init__(self, user_id: str, data_directory: str = "user_data"):
        self.user_id = user_id
        self.data_dir = Path(data_directory) / user_id
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize privacy settings with conservative defaults
        self.privacy_settings = self._load_privacy_settings()
        self.data_categories = {category.value: [] for category in DataCategory}
        
        # Load existing data
        self._load_user_data()
        
    def _load_privacy_settings(self) -> Dict[str, PrivacyLevel]:
        """Load user privacy preferences with safe defaults"""
        privacy_file = self.data_dir / "privacy_settings.json"
        
        # Default to most private settings
        default_settings = {
            category.value: PrivacyLevel.PRIVATE.value 
            for category in DataCategory
        }
        
        if privacy_file.exists():
            try:
                with open(privacy_file, 'r') as f:
                    saved_settings = json.load(f)
                    # Merge with defaults to handle new categories
                    default_settings.update(saved_settings)
            except Exception as e:
                print(f"Warning: Could not load privacy settings: {e}")
                print("Using default private settings for all data")
        
        return {
            category: PrivacyLevel(level) 
            for category, level in default_settings.items()
        }
    
    def update_privacy_setting(self, category: DataCategory, level: PrivacyLevel, 
                             confirmation: bool = False) -> bool:
        """
        Update privacy setting for a data category with explicit confirmation
        """
        if not confirmation:
            return False, "Privacy setting changes require explicit confirmation"
        
        # Warn about implications of less private settings
        if level != PrivacyLevel.PRIVATE:
            privacy_implications = self._get_privacy_implications(level)
            print(f"Privacy Notice: {privacy_implications}")
        
        self.privacy_settings[category.value] = level
        self._save_privacy_settings()
        
        return True, f"Privacy level for {category.value} updated to {level.value}"
    
    def _get_privacy_implications(self, level: PrivacyLevel) -> str:
        """Provide clear explanation of privacy implications"""
        implications = {
            PrivacyLevel.ANONYMOUS: "Data will be anonymized and aggregated for insights",
            PrivacyLevel.AGGREGATED: "Data will be combined with others for team patterns",
            PrivacyLevel.TEAM_VISIBLE: "Team members can see your productivity patterns",
            PrivacyLevel.FULL_COLLABORATION: "Complete data sharing with team for collaboration"
        }
        return implications.get(level, "Data remains completely private")
    
    def store_data(self, category: DataCategory, data: Dict[str, Any], 
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store user data with timestamp and privacy respect
        """
        record_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        record = {
            "id": record_id,
            "timestamp": timestamp,
            "category": category.value,
            "data": data,
            "metadata": metadata or {},
            "privacy_level": self.privacy_settings[category.value].value
        }
        
        # Store in appropriate category
        self.data_categories[category.value].append(record)
        
        # Save to file
        self._save_category_data(category)
        
        return record_id
    
    def get_data(self, category: DataCategory, 
                 date_range: Optional[Tuple[datetime.date, datetime.date]] = None,
                 include_metadata: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve user data with optional filtering
        """
        data = self.data_categories[category.value].copy()
        
        # Filter by date range if provided
        if date_range:
            start_date, end_date = date_range
            filtered_data = []
            for record in data:
                record_date = datetime.datetime.fromisoformat(record["timestamp"]).date()
                if start_date <= record_date <= end_date:
                    filtered_data.append(record)
            data = filtered_data
        
        # Remove metadata if not requested
        if not include_metadata:
            for record in data:
                record.pop("metadata", None)
        
        return data
    
    def update_data(self, category: DataCategory, record_id: str, 
                    updated_data: Dict[str, Any], user_confirmation: bool = False) -> bool:
        """
        Update existing data record with user confirmation
        """
        if not user_confirmation:
            return False, "Data updates require explicit user confirmation"
        
        records = self.data_categories[category.value]
        for i, record in enumerate(records):
            if record["id"] == record_id:
                record["data"].update(updated_data)
                record["last_modified"] = datetime.datetime.now().isoformat()
                self._save_category_data(category)
                return True, "Data updated successfully"
        
        return False, f"Record {record_id} not found in {category.value}"
    
    def delete_data(self, category: DataCategory, record_id: Optional[str] = None,
                    confirmation_phrase: Optional[str] = None) -> bool:
        """
        Delete data with explicit confirmation for safety
        """
        expected_phrase = f"DELETE {category.value}"
        if confirmation_phrase != expected_phrase:
            return False, f"Deletion requires confirmation phrase: '{expected_phrase}'"
        
        if record_id:
            # Delete specific record
            records = self.data_categories[category.value]
            original_count = len(records)
            self.data_categories[category.value] = [
                r for r in records if r["id"] != record_id
            ]
            
            if len(self.data_categories[category.value]) < original_count:
                self._save_category_data(category)
                return True, f"Record {record_id} deleted from {category.value}"
            else:
                return False, f"Record {record_id} not found"
        else:
            # Delete entire category
            self.data_categories[category.value] = []
            self._save_category_data(category)
            return True, f"All {category.value} data deleted"
    
    def export_all_data(self, include_system_data: bool = False) -> Dict[str, Any]:
        """
        Export all user data in portable format
        """
        export_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now()
        
        # Calculate data range
        all_timestamps = []
        for category_data in self.data_categories.values():
            for record in category_data:
                all_timestamps.append(
                    datetime.datetime.fromisoformat(record["timestamp"]).date()
                )
        
        date_range = (min(all_timestamps), max(all_timestamps)) if all_timestamps else (None, None)
        total_records = sum(len(data) for data in self.data_categories.values())
        
        # Create export manifest
        manifest = DataExportManifest(
            export_id=export_id,
            user_id=self.user_id,
            export_timestamp=timestamp,
            data_categories=list(self.data_categories.keys()),
            total_records=total_records,
            date_range=date_range,
            privacy_settings={k: v.value for k, v in self.privacy_settings.items()},
            data_ownership_statement="This data belongs entirely to the user. FlowState claims no ownership or rights to this information.",
            deletion_instructions="To delete this data from FlowState systems, use the account deletion feature or contact support with this export ID."
        )
        
        export_data = {
            "manifest": asdict(manifest),
            "data": self.data_categories.copy(),
            "privacy_settings": {k: v.value for k, v in self.privacy_settings.items()}
        }
        
        # Include system data if requested (for debugging/transparency)
        if include_system_data:
            export_data["system_info"] = {
                "export_version": "1.0",
                "flowstate_version": "0.1.0",
                "data_format": "JSON",
                "encryption": "None (user responsibility)",
                "privacy_policy_version": "1.0"
            }
        
        return export_data
    
    def get_privacy_dashboard(self) -> Dict[str, Any]:
        """
        Provide complete transparency about user data and privacy
        """
        dashboard = {
            "user_id": self.user_id,
            "data_summary": {},
            "privacy_settings": {},
            "sharing_status": {},
            "data_rights": {
                "export": "You can export all your data at any time",
                "delete": "You can delete specific records or entire categories",
                "modify": "You can update any data record with confirmation",
                "privacy": "You control privacy levels for each data category",
                "ownership": "You own all your data completely"
            }
        }
        
        # Data summary
        for category, data in self.data_categories.items():
            dashboard["data_summary"][category] = {
                "record_count": len(data),
                "date_range": self._get_category_date_range(data),
                "storage_size_kb": self._estimate_storage_size(data)
            }
        
        # Privacy settings summary
        for category, level in self.privacy_settings.items():
            dashboard["privacy_settings"][category] = {
                "current_level": level.value,
                "implications": self._get_privacy_implications(level),
                "can_be_shared": level != PrivacyLevel.PRIVATE
            }
        
        # Current sharing status
        for category, level in self.privacy_settings.items():
            if level != PrivacyLevel.PRIVATE:
                dashboard["sharing_status"][category] = {
                    "currently_shared": True,
                    "sharing_type": level.value,
                    "can_revoke": True
                }
        
        return dashboard
    
    def reset_all_data(self, confirmation_phrase: str) -> bool:
        """
        Complete data reset with strong confirmation requirement
        """
        expected_phrase = f"RESET ALL DATA FOR {self.user_id}"
        if confirmation_phrase != expected_phrase:
            return False, f"Complete reset requires exact phrase: '{expected_phrase}'"
        
        # Reset all data categories
        for category in DataCategory:
            self.data_categories[category.value] = []
            self._save_category_data(category)
        
        # Reset privacy settings to defaults
        self.privacy_settings = {
            category.value: PrivacyLevel.PRIVATE 
            for category in DataCategory
        }
        self._save_privacy_settings()
        
        # Create reset log
        reset_log = {
            "reset_timestamp": datetime.datetime.now().isoformat(),
            "user_id": self.user_id,
            "action": "complete_data_reset",
            "confirmation_provided": True
        }
        
        with open(self.data_dir / "reset_log.json", "w") as f:
            json.dump(reset_log, f, indent=2)
        
        return True, "All user data has been reset successfully"
    
    def _load_user_data(self):
        """Load existing user data from files"""
        for category in DataCategory:
            category_file = self.data_dir / f"{category.value}.json"
            if category_file.exists():
                try:
                    with open(category_file, 'r') as f:
                        self.data_categories[category.value] = json.load(f)
                except Exception as e:
                    print(f"Warning: Could not load {category.value} data: {e}")
                    self.data_categories[category.value] = []
    
    def _save_category_data(self, category: DataCategory):
        """Save category data to file"""
        category_file = self.data_dir / f"{category.value}.json"
        try:
            with open(category_file, 'w') as f:
                json.dump(self.data_categories[category.value], f, indent=2)
        except Exception as e:
            print(f"Error saving {category.value} data: {e}")
    
    def _save_privacy_settings(self):
        """Save privacy settings to file"""
        privacy_file = self.data_dir / "privacy_settings.json"
        try:
            settings_to_save = {k: v.value for k, v in self.privacy_settings.items()}
            with open(privacy_file, 'w') as f:
                json.dump(settings_to_save, f, indent=2)
        except Exception as e:
            print(f"Error saving privacy settings: {e}")
    
    def _get_category_date_range(self, data: List[Dict]) -> Optional[Tuple[str, str]]:
        """Get date range for a category of data"""
        if not data:
            return None
        
        timestamps = [
            datetime.datetime.fromisoformat(record["timestamp"]).date()
            for record in data
        ]
        return (str(min(timestamps)), str(max(timestamps)))
    
    def _estimate_storage_size(self, data: List[Dict]) -> float:
        """Estimate storage size in KB"""
        try:
            data_str = json.dumps(data)
            return len(data_str.encode('utf-8')) / 1024
        except:
            return 0.0


# Example usage and testing
if __name__ == "__main__":
    # Example of ethical user data management
    user_data = UserDataManager("user_123")
    
    # Store some time tracking data
    time_entry = {
        "task": "Code review",
        "duration_minutes": 45,
        "energy_level": 8,
        "focus_quality": 9
    }
    
    record_id = user_data.store_data(
        DataCategory.TIME_ENTRIES, 
        time_entry,
        metadata={"source": "manual_entry", "device": "laptop"}
    )
    
    # Check privacy dashboard
    dashboard = user_data.get_privacy_dashboard()
    print("Privacy Dashboard:", json.dumps(dashboard, indent=2))
    
    # Export all data
    export = user_data.export_all_data(include_system_data=True)
    print(f"Export contains {export['manifest']['total_records']} records")
    
    # Example of privacy setting update
    success, message = user_data.update_privacy_setting(
        DataCategory.TIME_ENTRIES, 
        PrivacyLevel.AGGREGATED,
        confirmation=True
    )
    print(f"Privacy update: {message}")

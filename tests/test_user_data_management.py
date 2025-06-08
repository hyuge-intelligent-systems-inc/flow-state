
"""
FlowState User Data Management Tests
Comprehensive testing for user data ownership and privacy controls
Based on expert analysis emphasizing complete user sovereignty over data
"""

import unittest
import json
import tempfile
import os
import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the modules we're testing (adjust path as needed)
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.user_data_management import (
    UserDataManager, PrivacyLevel, DataCategory, 
    DataExportManifest
)


class TestUserDataOwnership(unittest.TestCase):
    """Test complete user ownership and control of data"""
    
    def setUp(self):
        """Set up test environment with temporary directory"""
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "test_user_123"
        self.data_manager = UserDataManager(self.user_id, self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_user_owns_all_data(self):
        """Test that user has complete ownership of their data"""
        # Store some test data
        test_data = {"task": "Test task", "duration": 60}
        record_id = self.data_manager.store_data(
            DataCategory.TIME_ENTRIES, 
            test_data
        )
        
        # User should be able to access their data
        retrieved_data = self.data_manager.get_data(DataCategory.TIME_ENTRIES)
        self.assertEqual(len(retrieved_data), 1)
        self.assertEqual(retrieved_data[0]["data"]["task"], "Test task")
        
        # User should be able to export all their data
        export = self.data_manager.export_all_data()
        self.assertIn("data_ownership_statement", export["manifest"])
        self.assertIn("belongs entirely to the user", export["manifest"]["data_ownership_statement"])
    
    def test_granular_data_control(self):
        """Test user can control each category of data independently"""
        # Test privacy level control for each category
        for category in DataCategory:
            success, message = self.data_manager.update_privacy_setting(
                category, 
                PrivacyLevel.AGGREGATED, 
                confirmation=True
            )
            self.assertTrue(success)
            self.assertEqual(
                self.data_manager.privacy_settings[category.value], 
                PrivacyLevel.AGGREGATED
            )
    
    def test_data_export_completeness(self):
        """Test that data export includes everything user owns"""
        # Add data to multiple categories
        categories_with_data = [
            DataCategory.TIME_ENTRIES,
            DataCategory.PRODUCTIVITY_PATTERNS,
            DataCategory.SELF_DISCOVERY_INSIGHTS
        ]
        
        for category in categories_with_data:
            self.data_manager.store_data(
                category, 
                {"test": f"data for {category.value}"}
            )
        
        # Export should include all categories
        export = self.data_manager.export_all_data()
        
        # Check manifest completeness
        manifest = export["manifest"]
        self.assertEqual(manifest["user_id"], self.user_id)
        self.assertGreater(manifest["total_records"], 0)
        self.assertIn("data_ownership_statement", manifest)
        
        # Check data completeness
        for category in categories_with_data:
            self.assertIn(category.value, export["data"])
            self.assertGreater(len(export["data"][category.value]), 0)
    
    def test_data_deletion_rights(self):
        """Test user can delete any or all of their data"""
        # Store test data
        record_id = self.data_manager.store_data(
            DataCategory.TIME_ENTRIES,
            {"task": "Test deletion", "duration": 30}
        )
        
        # User should be able to delete specific record
        success, message = self.data_manager.delete_data(
            DataCategory.TIME_ENTRIES,
            record_id,
            confirmation_phrase="DELETE time_entries"
        )
        self.assertTrue(success)
        
        # Data should be gone
        remaining_data = self.data_manager.get_data(DataCategory.TIME_ENTRIES)
        self.assertEqual(len(remaining_data), 0)
    
    def test_complete_data_reset(self):
        """Test user can reset all their data completely"""
        # Add data to multiple categories
        for category in [DataCategory.TIME_ENTRIES, DataCategory.AI_INTERACTIONS]:
            self.data_manager.store_data(category, {"test": "data"})
        
        # Verify data exists
        self.assertGreater(
            len(self.data_manager.get_data(DataCategory.TIME_ENTRIES)), 0
        )
        
        # Reset all data
        success, message = self.data_manager.reset_all_data(
            f"RESET ALL DATA FOR {self.user_id}"
        )
        self.assertTrue(success)
        
        # All data should be gone
        for category in DataCategory:
            data = self.data_manager.get_data(category)
            self.assertEqual(len(data), 0)
        
        # Privacy settings should be reset to private
        for category, level in self.data_manager.privacy_settings.items():
            self.assertEqual(level, PrivacyLevel.PRIVATE)


class TestPrivacyControls(unittest.TestCase):
    """Test granular privacy controls and transparency"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "privacy_test_user"
        self.data_manager = UserDataManager(self.user_id, self.test_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_default_privacy_settings(self):
        """Test that default privacy settings are maximally private"""
        for category in DataCategory:
            privacy_level = self.data_manager.privacy_settings[category.value]
            self.assertEqual(privacy_level, PrivacyLevel.PRIVATE)
    
    def test_privacy_setting_confirmation_required(self):
        """Test that privacy changes require explicit confirmation"""
        # Should fail without confirmation
        success, message = self.data_manager.update_privacy_setting(
            DataCategory.TIME_ENTRIES,
            PrivacyLevel.TEAM_VISIBLE,
            confirmation=False
        )
        self.assertFalse(success)
        self.assertIn("require explicit confirmation", message)
        
        # Should succeed with confirmation
        success, message = self.data_manager.update_privacy_setting(
            DataCategory.TIME_ENTRIES,
            PrivacyLevel.TEAM_VISIBLE,
            confirmation=True
        )
        self.assertTrue(success)
    
    def test_privacy_implications_transparency(self):
        """Test that privacy changes include clear implications"""
        with patch('builtins.print') as mock_print:
            self.data_manager.update_privacy_setting(
                DataCategory.PRODUCTIVITY_PATTERNS,
                PrivacyLevel.AGGREGATED,
                confirmation=True
            )
            
            # Should have printed privacy implications
            mock_print.assert_called()
            printed_text = str(mock_print.call_args)
            self.assertIn("Privacy Notice", printed_text)
    
    def test_privacy_dashboard_transparency(self):
        """Test privacy dashboard provides complete transparency"""
        # Set different privacy levels
        self.data_manager.update_privacy_setting(
            DataCategory.TIME_ENTRIES, PrivacyLevel.AGGREGATED, confirmation=True
        )
        self.data_manager.update_privacy_setting(
            DataCategory.ENERGY_LEVELS, PrivacyLevel.TEAM_VISIBLE, confirmation=True
        )
        
        dashboard = self.data_manager.get_privacy_dashboard()
        
        # Should include user rights
        self.assertIn("data_rights", dashboard)
        rights = dashboard["data_rights"]
        self.assertIn("export", rights)
        self.assertIn("delete", rights)
        self.assertIn("ownership", rights)
        
        # Should show current privacy settings
        self.assertIn("privacy_settings", dashboard)
        time_entries_privacy = dashboard["privacy_settings"]["time_entries"]
        self.assertEqual(time_entries_privacy["current_level"], "aggregated")
        
        # Should show sharing status
        self.assertIn("sharing_status", dashboard)
    
    def test_data_category_isolation(self):
        """Test that privacy settings are isolated between categories"""
        # Set different privacy levels
        self.data_manager.update_privacy_setting(
            DataCategory.TIME_ENTRIES, PrivacyLevel.TEAM_VISIBLE, confirmation=True
        )
        self.data_manager.update_privacy_setting(
            DataCategory.SELF_DISCOVERY_INSIGHTS, PrivacyLevel.PRIVATE, confirmation=True
        )
        
        # Categories should have independent privacy levels
        self.assertEqual(
            self.data_manager.privacy_settings[DataCategory.TIME_ENTRIES.value],
            PrivacyLevel.TEAM_VISIBLE
        )
        self.assertEqual(
            self.data_manager.privacy_settings[DataCategory.SELF_DISCOVERY_INSIGHTS.value],
            PrivacyLevel.PRIVATE
        )


class TestDataStorageAndRetrieval(unittest.TestCase):
    """Test reliable data storage and retrieval"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "storage_test_user"
        self.data_manager = UserDataManager(self.user_id, self.test_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_data_storage_with_metadata(self):
        """Test storing data with metadata preservation"""
        test_data = {"task": "Important work", "duration": 120}
        test_metadata = {"source": "manual_entry", "device": "laptop"}
        
        record_id = self.data_manager.store_data(
            DataCategory.TIME_ENTRIES,
            test_data,
            metadata=test_metadata
        )
        
        # Should return valid record ID
        self.assertIsInstance(record_id, str)
        self.assertTrue(len(record_id) > 0)
        
        # Data should be retrievable with metadata
        retrieved_data = self.data_manager.get_data(
            DataCategory.TIME_ENTRIES, 
            include_metadata=True
        )
        
        self.assertEqual(len(retrieved_data), 1)
        record = retrieved_data[0]
        self.assertEqual(record["data"]["task"], "Important work")
        self.assertEqual(record["metadata"]["source"], "manual_entry")
        self.assertIn("timestamp", record)
        self.assertIn("privacy_level", record)
    
    def test_data_retrieval_filtering(self):
        """Test data retrieval with date range filtering"""
        # Store data on different dates
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        
        # Mock datetime for consistent testing
        with patch('datetime.datetime') as mock_datetime:
            # Store data "yesterday"
            mock_datetime.now.return_value = datetime.datetime.combine(
                yesterday, datetime.time(10, 0)
            )
            mock_datetime.fromisoformat = datetime.datetime.fromisoformat
            
            yesterday_id = self.data_manager.store_data(
                DataCategory.TIME_ENTRIES,
                {"task": "Yesterday task", "duration": 60}
            )
            
            # Store data "today"
            mock_datetime.now.return_value = datetime.datetime.combine(
                today, datetime.time(10, 0)
            )
            
            today_id = self.data_manager.store_data(
                DataCategory.TIME_ENTRIES,
                {"task": "Today task", "duration": 90}
            )
        
        # Retrieve only today's data
        today_data = self.data_manager.get_data(
            DataCategory.TIME_ENTRIES,
            date_range=(today, today)
        )
        
        self.assertEqual(len(today_data), 1)
        self.assertEqual(today_data[0]["data"]["task"], "Today task")
    
    def test_data_update_with_confirmation(self):
        """Test data updates require user confirmation"""
        # Store initial data
        test_data = {"task": "Original task", "duration": 60}
        record_id = self.data_manager.store_data(
            DataCategory.TIME_ENTRIES,
            test_data
        )
        
        # Update should fail without confirmation
        success, message = self.data_manager.update_data(
            DataCategory.TIME_ENTRIES,
            record_id,
            {"duration": 90},
            user_confirmation=False
        )
        self.assertFalse(success)
        self.assertIn("require explicit user confirmation", message)
        
        # Update should succeed with confirmation
        success, message = self.data_manager.update_data(
            DataCategory.TIME_ENTRIES,
            record_id,
            {"duration": 90},
            user_confirmation=True
        )
        self.assertTrue(success)
        
        # Data should be updated
        updated_data = self.data_manager.get_data(DataCategory.TIME_ENTRIES)
        self.assertEqual(updated_data[0]["data"]["duration"], 90)
        self.assertIn("last_modified", updated_data[0])
    
    def test_data_persistence(self):
        """Test data persists across manager instances"""
        # Store data
        test_data = {"task": "Persistent task", "duration": 45}
        self.data_manager.store_data(DataCategory.TIME_ENTRIES, test_data)
        
        # Create new manager instance (simulates app restart)
        new_manager = UserDataManager(self.user_id, self.test_dir)
        
        # Data should still be available
        retrieved_data = new_manager.get_data(DataCategory.TIME_ENTRIES)
        self.assertEqual(len(retrieved_data), 1)
        self.assertEqual(retrieved_data[0]["data"]["task"], "Persistent task")


class TestDataSafety(unittest.TestCase):
    """Test data safety and error handling"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "safety_test_user"
        self.data_manager = UserDataManager(self.user_id, self.test_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_deletion_confirmation_required(self):
        """Test deletion requires exact confirmation phrases"""
        # Store test data
        record_id = self.data_manager.store_data(
            DataCategory.TIME_ENTRIES,
            {"task": "Test", "duration": 30}
        )
        
        # Should fail with wrong confirmation
        success, message = self.data_manager.delete_data(
            DataCategory.TIME_ENTRIES,
            record_id,
            confirmation_phrase="wrong phrase"
        )
        self.assertFalse(success)
        
        # Should succeed with correct confirmation
        success, message = self.data_manager.delete_data(
            DataCategory.TIME_ENTRIES,
            record_id,
            confirmation_phrase="DELETE time_entries"
        )
        self.assertTrue(success)
    
    def test_reset_confirmation_security(self):
        """Test complete reset requires precise confirmation"""
        # Should fail with wrong confirmation
        success, message = self.data_manager.reset_all_data("wrong phrase")
        self.assertFalse(success)
        
        # Should fail with almost correct confirmation
        success, message = self.data_manager.reset_all_data(
            f"RESET ALL DATA FOR wrong_user"
        )
        self.assertFalse(success)
        
        # Should succeed only with exact confirmation
        success, message = self.data_manager.reset_all_data(
            f"RESET ALL DATA FOR {self.user_id}"
        )
        self.assertTrue(success)
    
    def test_file_corruption_handling(self):
        """Test graceful handling of corrupted data files"""
        # Create corrupted file
        category_file = self.data_manager.data_dir / "time_entries.json"
        with open(category_file, 'w') as f:
            f.write("corrupted json content {")
        
        # Should handle corruption gracefully
        with patch('builtins.print') as mock_print:
            new_manager = UserDataManager(self.user_id, self.test_dir)
            
            # Should print warning about corruption
            mock_print.assert_called()
            printed_text = str(mock_print.call_args)
            self.assertIn("Warning", printed_text)
        
        # Should start with empty data for corrupted category
        data = new_manager.get_data(DataCategory.TIME_ENTRIES)
        self.assertEqual(len(data), 0)
    
    def test_privacy_settings_corruption_handling(self):
        """Test handling of corrupted privacy settings"""
        # Create corrupted privacy file
        privacy_file = self.data_manager.data_dir / "privacy_settings.json"
        with open(privacy_file, 'w') as f:
            f.write("corrupted privacy settings")
        
        # Should handle corruption gracefully and default to private
        with patch('builtins.print') as mock_print:
            new_manager = UserDataManager(self.user_id, self.test_dir)
            
            # Should default to most private settings
            for category in DataCategory:
                privacy_level = new_manager.privacy_settings[category.value]
                self.assertEqual(privacy_level, PrivacyLevel.PRIVATE)


class TestExportAndPortability(unittest.TestCase):
    """Test complete data export and portability"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "export_test_user"
        self.data_manager = UserDataManager(self.user_id, self.test_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_comprehensive_export(self):
        """Test export includes all user data and ownership info"""
        # Add data to multiple categories
        self.data_manager.store_data(
            DataCategory.TIME_ENTRIES,
            {"task": "Export test", "duration": 60}
        )
        self.data_manager.store_data(
            DataCategory.PRODUCTIVITY_PATTERNS,
            {"pattern": "Morning productivity", "confidence": 0.8}
        )
        
        # Update privacy setting
        self.data_manager.update_privacy_setting(
            DataCategory.TIME_ENTRIES, PrivacyLevel.AGGREGATED, confirmation=True
        )
        
        # Export all data
        export = self.data_manager.export_all_data(include_system_data=True)
        
        # Should include manifest with ownership statement
        manifest = export["manifest"]
        self.assertIn("data_ownership_statement", manifest)
        self.assertIn("belongs entirely to the user", manifest["data_ownership_statement"])
        self.assertIn("deletion_instructions", manifest)
        
        # Should include all data categories
        self.assertIn("data", export)
        self.assertIn("privacy_settings", export)
        
        # Should include system info when requested
        self.assertIn("system_info", export)
        self.assertIn("export_version", export["system_info"])
    
    def test_export_format_standards(self):
        """Test export uses standard, portable formats"""
        export = self.data_manager.export_all_data()
        
        # Should be JSON serializable
        json_export = json.dumps(export, default=str)
        self.assertIsInstance(json_export, str)
        
        # Should be deserializable
        reimported = json.loads(json_export)
        self.assertEqual(reimported["manifest"]["user_id"], self.user_id)
    
    def test_export_includes_privacy_context(self):
        """Test export includes full privacy context"""
        # Set various privacy levels
        self.data_manager.update_privacy_setting(
            DataCategory.TIME_ENTRIES, PrivacyLevel.TEAM_VISIBLE, confirmation=True
        )
        self.data_manager.update_privacy_setting(
            DataCategory.ENERGY_LEVELS, PrivacyLevel.PRIVATE, confirmation=True
        )
        
        export = self.data_manager.export_all_data()
        
        # Should include privacy settings
        privacy_settings = export["privacy_settings"]
        self.assertEqual(privacy_settings["time_entries"], "team_visible")
        self.assertEqual(privacy_settings["energy_levels"], "private")
        
        # Manifest should include privacy summary
        manifest_privacy = export["manifest"]["privacy_settings"]
        self.assertIn("time_entries", manifest_privacy)
        self.assertIn("energy_levels", manifest_privacy)


class TestUserDataIntegration(unittest.TestCase):
    """Test integration with other FlowState modules"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "integration_test_user"
        self.data_manager = UserDataManager(self.user_id, self.test_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_time_tracker_integration(self):
        """Test integration with time tracking data"""
        # Simulate time tracker storing data
        time_entry = {
            "task_name": "Code review",
            "start_time": "2024-01-15T09:00:00",
            "end_time": "2024-01-15T10:30:00",
            "duration_minutes": 90,
            "energy_level": 8,
            "focus_quality": 7
        }
        
        record_id = self.data_manager.store_data(
            DataCategory.TIME_ENTRIES,
            time_entry,
            metadata={"source": "time_tracker", "session_id": "session_123"}
        )
        
        # Should be retrievable by time tracker
        retrieved = self.data_manager.get_data(DataCategory.TIME_ENTRIES)
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0]["data"]["task_name"], "Code review")
    
    def test_self_discovery_integration(self):
        """Test integration with self-discovery insights"""
        # Simulate self-discovery storing user insights
        insight = {
            "insight_type": "productivity_pattern",
            "user_observation": "I'm most creative in the morning",
            "supporting_evidence": ["High energy 9am-11am", "Best ideas before lunch"],
            "confidence": "high",
            "date_discovered": "2024-01-15"
        }
        
        record_id = self.data_manager.store_data(
            DataCategory.SELF_DISCOVERY_INSIGHTS,
            insight,
            metadata={"discovery_session_id": "discovery_456"}
        )
        
        # Should maintain privacy (default private)
        privacy_level = self.data_manager.privacy_settings[DataCategory.SELF_DISCOVERY_INSIGHTS.value]
        self.assertEqual(privacy_level, PrivacyLevel.PRIVATE)
    
    def test_ai_interaction_tracking(self):
        """Test tracking AI interactions with transparency"""
        # Simulate AI tracker storing interactions
        ai_interaction = {
            "suggestion_type": "focus_time",
            "suggestion": "Try working on creative tasks between 9-11am",
            "confidence_score": 0.7,
            "supporting_evidence": ["Historical pattern analysis"],
            "user_response": "accepted",
            "outcome": "followed_suggestion"
        }
        
        record_id = self.data_manager.store_data(
            DataCategory.AI_INTERACTIONS,
            ai_interaction,
            metadata={"ai_model_version": "1.0", "session_context": "morning_planning"}
        )
        
        # Should be fully auditable by user
        interactions = self.data_manager.get_data(
            DataCategory.AI_INTERACTIONS, 
            include_metadata=True
        )
        self.assertEqual(len(interactions), 1)
        self.assertIn("suggestion_type", interactions[0]["data"])
        self.assertIn("confidence_score", interactions[0]["data"])


def run_all_tests():
    """Run all user data management tests with detailed reporting"""
    
    # Create test suite
    test_classes = [
        TestUserDataOwnership,
        TestPrivacyControls,
        TestDataStorageAndRetrieval,
        TestDataSafety,
        TestExportAndPortability,
        TestUserDataIntegration
    ]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    success_rate = ((total_tests - failures - errors) / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n" + "="*50)
    print(f"USER DATA MANAGEMENT TEST SUMMARY")
    print(f"="*50)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_tests - failures - errors}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if failures:
        print(f"\nFAILURES:")
        for test, failure in result.failures:
            print(f"- {test}: {failure}")
    
    if errors:
        print(f"\nERRORS:")
        for test, error in result.errors:
            print(f"- {test}: {error}")
    
    print(f"\nKey Areas Validated:")
    print(f"✅ Complete user data ownership and control")
    print(f"✅ Granular privacy controls with transparency")
    print(f"✅ Reliable data storage and retrieval")
    print(f"✅ Data safety with confirmation requirements")
    print(f"✅ Complete data export and portability")
    print(f"✅ Integration with other FlowState modules")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

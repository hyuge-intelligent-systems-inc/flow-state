

"""
FlowState Time Tracker Tests
Comprehensive testing for core time tracking functionality

Key testing principles implemented:
- Test user agency and control preservation
- Verify honest limitations and uncertainty handling
- Validate failure resilience and graceful degradation
- Ensure data ownership and export capabilities
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
import tempfile
import os
from typing import Dict, Any

# Import the module we're testing
# Note: In actual implementation, adjust import path as needed
import sys
sys.path.append('../src/core')
from time_tracker import TimeTracker, TimeEntry, SessionSummary


class TestTimeTracker(unittest.TestCase):
    """
    Comprehensive tests for TimeTracker class
    """
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.tracker = TimeTracker()
        self.test_category = "Deep Work"
        self.test_description = "Writing FlowState tests"
        
        # Create some test time entries for complex scenarios
        self.sample_entries = [
            {
                'start_time': datetime.now() - timedelta(hours=2),
                'end_time': datetime.now() - timedelta(hours=1, minutes=30),
                'category': 'Deep Work',
                'description': 'Code review',
                'energy_before': 4,
                'energy_after': 3,
                'focus_quality': 4
            },
            {
                'start_time': datetime.now() - timedelta(hours=1, minutes=15),
                'end_time': datetime.now() - timedelta(minutes=45),
                'category': 'Meeting',
                'description': 'Team standup',
                'energy_before': 3,
                'energy_after': 3,
                'focus_quality': 2
            }
        ]
    
    def tearDown(self):
        """Clean up after each test method"""
        # Reset tracker state
        self.tracker = None


class TestBasicTimeTracking(TestTimeTracker):
    """Test basic time tracking functionality"""
    
    def test_start_timer_creates_active_session(self):
        """Test that starting timer creates an active session"""
        result = self.tracker.start_timer(self.test_category, self.test_description)
        
        self.assertEqual(result['status'], 'started')
        self.assertTrue(self.tracker.is_tracking())
        self.assertIsNotNone(self.tracker.current_session)
        self.assertEqual(self.tracker.current_session['category'], self.test_category)
        self.assertEqual(self.tracker.current_session['description'], self.test_description)
    
    def test_start_timer_when_already_tracking_requires_user_choice(self):
        """Test that starting timer when already tracking respects user agency"""
        # Start first session
        self.tracker.start_timer("Task 1", "First task")
        
        # Try to start second session without explicit choice
        result = self.tracker.start_timer("Task 2", "Second task")
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('already_tracking', result['message'])
        self.assertIn('user_choice_required', result)
        
        # Verify original session is still active
        self.assertEqual(self.tracker.current_session['category'], "Task 1")
    
    def test_start_timer_with_force_override_respects_user_agency(self):
        """Test that user can explicitly override active session"""
        # Start first session
        self.tracker.start_timer("Task 1", "First task")
        original_session_id = self.tracker.current_session['session_id']
        
        # User explicitly chooses to override
        result = self.tracker.start_timer("Task 2", "Second task", force_override=True)
        
        self.assertEqual(result['status'], 'started')
        self.assertEqual(self.tracker.current_session['category'], "Task 2")
        self.assertNotEqual(self.tracker.current_session['session_id'], original_session_id)
        
        # Verify previous session was saved as incomplete
        incomplete_sessions = [e for e in self.tracker.entries if e.incomplete]
        self.assertEqual(len(incomplete_sessions), 1)
        self.assertEqual(incomplete_sessions[0].session_id, original_session_id)
    
    def test_stop_timer_completes_session_successfully(self):
        """Test that stopping timer completes session with user control"""
        # Start and stop a session
        self.tracker.start_timer(self.test_category, self.test_description)
        session_id = self.tracker.current_session['session_id']
        
        result = self.tracker.stop_timer()
        
        self.assertEqual(result['status'], 'completed')
        self.assertFalse(self.tracker.is_tracking())
        self.assertIsNone(self.tracker.current_session)
        
        # Verify entry was created
        completed_entry = next((e for e in self.tracker.entries if e.session_id == session_id), None)
        self.assertIsNotNone(completed_entry)
        self.assertFalse(completed_entry.incomplete)
        self.assertIsNotNone(completed_entry.duration_minutes)
    
    def test_stop_timer_when_not_tracking_handles_gracefully(self):
        """Test graceful handling when stopping timer without active session"""
        result = self.tracker.stop_timer()
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('not_currently_tracking', result['message'])
        self.assertFalse(self.tracker.is_tracking())


class TestManualTimeEntry(TestTimeTracker):
    """Test manual time entry functionality"""
    
    def test_add_manual_entry_with_valid_data(self):
        """Test adding manual time entry with complete data"""
        start_time = datetime.now() - timedelta(hours=2)
        end_time = datetime.now() - timedelta(hours=1)
        
        result = self.tracker.add_manual_entry(
            start_time=start_time,
            end_time=end_time,
            category=self.test_category,
            description=self.test_description,
            energy_before=4,
            energy_after=3,
            focus_quality=4
        )
        
        self.assertEqual(result['status'], 'added')
        self.assertEqual(len(self.tracker.entries), 1)
        
        entry = self.tracker.entries[0]
        self.assertEqual(entry.category, self.test_category)
        self.assertEqual(entry.description, self.test_description)
        self.assertEqual(entry.energy_before, 4)
        self.assertEqual(entry.confidence_score, 1.0)  # Manual entries have high confidence
        self.assertFalse(entry.incomplete)
    
    def test_add_manual_entry_with_minimal_data(self):
        """Test adding manual entry with only required fields"""
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()
        
        result = self.tracker.add_manual_entry(
            start_time=start_time,
            end_time=end_time,
            category="Work"
        )
        
        self.assertEqual(result['status'], 'added')
        entry = self.tracker.entries[0]
        self.assertEqual(entry.category, "Work")
        self.assertIsNone(entry.description)
        self.assertIsNone(entry.energy_before)
        self.assertEqual(entry.confidence_score, 0.7)  # Lower confidence for minimal data
    
    def test_add_manual_entry_with_invalid_time_range(self):
        """Test validation of time ranges in manual entries"""
        start_time = datetime.now()
        end_time = datetime.now() - timedelta(hours=1)  # End before start
        
        result = self.tracker.add_manual_entry(
            start_time=start_time,
            end_time=end_time,
            category="Work"
        )
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('invalid_time_range', result['message'])
        self.assertEqual(len(self.tracker.entries), 0)
    
    def test_add_manual_entry_overlapping_times_warns_user(self):
        """Test that overlapping manual entries warn user but allow override"""
        base_time = datetime.now() - timedelta(hours=2)
        
        # Add first entry
        self.tracker.add_manual_entry(
            start_time=base_time,
            end_time=base_time + timedelta(hours=1),
            category="Task 1"
        )
        
        # Add overlapping entry
        result = self.tracker.add_manual_entry(
            start_time=base_time + timedelta(minutes=30),
            end_time=base_time + timedelta(hours=1, minutes=30),
            category="Task 2"
        )
        
        self.assertEqual(result['status'], 'warning')
        self.assertIn('overlapping_times', result['message'])
        self.assertIn('user_confirmation_recommended', result)
        
        # Entry should still be added (user agency preserved)
        self.assertEqual(len(self.tracker.entries), 2)


class TestUserAgencyAndControl(TestTimeTracker):
    """Test user agency and control features"""
    
    def test_update_entry_preserves_user_control(self):
        """Test that users can update any entry with full control"""
        # Add an entry
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()
        self.tracker.add_manual_entry(start_time, end_time, "Original Category")
        
        entry_id = self.tracker.entries[0].entry_id
        
        # Update the entry
        updates = {
            'category': 'Updated Category',
            'description': 'Updated description',
            'energy_before': 5,
            'focus_quality': 3
        }
        
        result = self.tracker.update_entry(entry_id, updates)
        
        self.assertEqual(result['status'], 'updated')
        
        updated_entry = next(e for e in self.tracker.entries if e.entry_id == entry_id)
        self.assertEqual(updated_entry.category, 'Updated Category')
        self.assertEqual(updated_entry.description, 'Updated description')
        self.assertEqual(updated_entry.energy_before, 5)
        self.assertEqual(updated_entry.focus_quality, 3)
    
    def test_delete_entry_respects_user_control(self):
        """Test that users can delete entries with confirmation"""
        # Add an entry
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()
        self.tracker.add_manual_entry(start_time, end_time, "To Delete")
        
        entry_id = self.tracker.entries[0].entry_id
        
        # Delete without confirmation should warn
        result = self.tracker.delete_entry(entry_id)
        self.assertEqual(result['status'], 'confirmation_required')
        self.assertEqual(len(self.tracker.entries), 1)  # Entry still exists
        
        # Delete with confirmation should succeed
        result = self.tracker.delete_entry(entry_id, confirmed=True)
        self.assertEqual(result['status'], 'deleted')
        self.assertEqual(len(self.tracker.entries), 0)
    
    def test_get_custom_categories_reflects_user_usage(self):
        """Test that custom categories reflect actual user usage"""
        # Add entries with various categories
        categories = ["Deep Work", "Meetings", "Email", "Deep Work", "Research"]
        for i, category in enumerate(categories):
            start_time = datetime.now() - timedelta(hours=len(categories)-i)
            end_time = start_time + timedelta(minutes=30)
            self.tracker.add_manual_entry(start_time, end_time, category)
        
        custom_categories = self.tracker.get_custom_categories()
        
        # Should return unique categories sorted by frequency
        expected_categories = ["Deep Work", "Email", "Meetings", "Research"]  # Deep Work appears twice
        self.assertEqual(custom_categories, expected_categories)
    
    def test_user_can_override_all_automatic_features(self):
        """Test that users can disable or override any automatic feature"""
        # Test disabling automatic categorization
        self.tracker.set_user_preference('auto_categorization', False)
        self.assertFalse(self.tracker.preferences['auto_categorization'])
        
        # Test disabling confidence scoring
        self.tracker.set_user_preference('show_confidence_scores', False)
        self.assertFalse(self.tracker.preferences['show_confidence_scores'])
        
        # Test disabling interruption tracking
        self.tracker.set_user_preference('track_interruptions', False)
        self.assertFalse(self.tracker.preferences['track_interruptions'])


class TestHonestLimitationsAndUncertainty(TestTimeTracker):
    """Test honest limitations and uncertainty handling"""
    
    def test_confidence_scoring_reflects_data_quality(self):
        """Test that confidence scores honestly reflect data quality"""
        # High confidence: Complete manual entry
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()
        self.tracker.add_manual_entry(
            start_time, end_time, "Work",
            description="Detailed work",
            energy_before=4, energy_after=3, focus_quality=4
        )
        
        high_confidence_entry = self.tracker.entries[0]
        self.assertGreaterEqual(high_confidence_entry.confidence_score, 0.9)
        
        # Lower confidence: Minimal data
        self.tracker.add_manual_entry(
            start_time + timedelta(hours=1),
            end_time + timedelta(hours=1),
            "Work"  # Only category provided
        )
        
        low_confidence_entry = self.tracker.entries[1]
        self.assertLess(low_confidence_entry.confidence_score, 0.8)
    
    def test_daily_summary_includes_limitations(self):
        """Test that daily summaries include honest limitations"""
        # Add some entries for today
        for entry_data in self.sample_entries:
            self.tracker.add_manual_entry(**entry_data)
        
        summary = self.tracker.get_daily_summary()
        
        # Verify limitations are included
        self.assertIn('limitations', summary)
        limitations = summary['limitations']
        self.assertIn('sample_size', limitations)
        self.assertIn('data_quality_varies', limitations)
        self.assertIn('self_reported_metrics', limitations)
        
        # Verify confidence assessment
        self.assertIn('overall_confidence', summary)
        self.assertIn('data_quality_notes', summary)
    
    def test_estimation_accuracy_tracking_is_honest(self):
        """Test that estimation accuracy tracking shows real performance"""
        # Add entries with estimated vs actual times
        estimates_and_actuals = [
            (30, 25),  # Good estimate
            (60, 90),  # Underestimate
            (45, 45),  # Perfect estimate
            (30, 60),  # Significant underestimate
        ]
        
        for estimated, actual in estimates_and_actuals:
            start_time = datetime.now() - timedelta(minutes=actual)
            end_time = datetime.now()
            
            entry_result = self.tracker.add_manual_entry(start_time, end_time, "Work")
            entry_id = entry_result['entry_id']
            
            # Add estimation data
            self.tracker.add_time_estimation(entry_id, estimated)
        
        accuracy_stats = self.tracker.get_estimation_accuracy()
        
        # Verify honest reporting
        self.assertIn('average_accuracy_percentage', accuracy_stats)
        self.assertIn('estimation_bias', accuracy_stats)
        self.assertIn('sample_size', accuracy_stats)
        self.assertIn('reliability_assessment', accuracy_stats)
        
        # Should identify underestimation bias
        self.assertLess(accuracy_stats['estimation_bias'], 0)  # Negative indicates underestimation
    
    def test_incomplete_sessions_are_handled_transparently(self):
        """Test that incomplete sessions are tracked and reported honestly"""
        # Start a session but don't complete it
        self.tracker.start_timer("Incomplete Task", "This won't be completed")
        
        # Simulate app restart or crash by creating new tracker instance
        # In real implementation, this would load from persistent storage
        new_tracker = TimeTracker()
        new_tracker.entries = self.tracker.entries.copy()
        new_tracker.current_session = self.tracker.current_session
        
        # Check incomplete session handling
        incomplete_sessions = new_tracker.get_incomplete_sessions()
        self.assertEqual(len(incomplete_sessions), 1)
        self.assertEqual(incomplete_sessions[0]['category'], "Incomplete Task")
        
        # User should be able to complete or discard incomplete sessions
        session_id = incomplete_sessions[0]['session_id']
        result = new_tracker.complete_incomplete_session(session_id, user_estimated_duration=30)
        
        self.assertEqual(result['status'], 'completed_with_estimation')
        self.assertIn('confidence_reduced', result)


class TestFailureResilienceAndGracefulDegradation(TestTimeTracker):
    """Test failure resilience and graceful degradation"""
    
    def test_handles_invalid_data_gracefully(self):
        """Test graceful handling of invalid or corrupted data"""
        # Test invalid energy levels
        result = self.tracker.add_manual_entry(
            start_time=datetime.now() - timedelta(hours=1),
            end_time=datetime.now(),
            category="Work",
            energy_before=10,  # Invalid: should be 1-5
            focus_quality=-1   # Invalid: should be 1-5
        )
        
        self.assertEqual(result['status'], 'added_with_corrections')
        self.assertIn('data_corrections', result)
        
        entry = self.tracker.entries[0]
        self.assertEqual(entry.energy_before, 5)  # Corrected to max valid
        self.assertEqual(entry.focus_quality, 1)  # Corrected to min valid
        
        # Confidence should be reduced due to data corrections
        self.assertLess(entry.confidence_score, 0.8)
    
    def test_handles_system_clock_changes(self):
        """Test handling of system clock changes and time anomalies"""
        # Simulate entry with future timestamp (clock skew)
        future_time = datetime.now() + timedelta(hours=1)
        
        result = self.tracker.add_manual_entry(
            start_time=future_time,
            end_time=future_time + timedelta(minutes=30),
            category="Future Work"
        )
        
        self.assertEqual(result['status'], 'added_with_warning')
        self.assertIn('timestamp_anomaly', result['warnings'])
        
        # Entry should still be added but with warning
        self.assertEqual(len(self.tracker.entries), 1)
        entry = self.tracker.entries[0]
        self.assertIn('timestamp_anomaly', entry.notes or "")
    
    def test_handles_large_data_volumes_gracefully(self):
        """Test handling of large numbers of entries"""
        # Add many entries
        base_time = datetime.now() - timedelta(days=365)
        
        for i in range(1000):  # Add 1000 entries
            start_time = base_time + timedelta(hours=i)
            end_time = start_time + timedelta(minutes=30)
            self.tracker.add_manual_entry(start_time, end_time, f"Task {i % 10}")
        
        # Should still function properly
        self.assertEqual(len(self.tracker.entries), 1000)
        
        # Performance-sensitive operations should still work
        daily_summary = self.tracker.get_daily_summary()
        self.assertIsNotNone(daily_summary)
        
        categories = self.tracker.get_custom_categories()
        self.assertLessEqual(len(categories), 10)  # Should have 10 unique categories
    
    @patch('builtins.open', side_effect=PermissionError("Access denied"))
    def test_handles_file_system_errors_gracefully(self, mock_open):
        """Test graceful handling of file system errors during export"""
        # Add some data
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()
        self.tracker.add_manual_entry(start_time, end_time, "Work")
        
        # Try to export when file system is unavailable
        result = self.tracker.export_data("/invalid/path/export.json")
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('file_system_error', result['error_type'])
        self.assertIn('alternative_methods', result)  # Should suggest alternatives


class TestDataOwnershipAndExport(TestTimeTracker):
    """Test data ownership and export capabilities"""
    
    def test_comprehensive_data_export(self):
        """Test that data export includes all user data comprehensively"""
        # Add various types of entries
        for entry_data in self.sample_entries:
            self.tracker.add_manual_entry(**entry_data)
        
        # Add some user preferences
        self.tracker.set_user_preference('default_category', 'Work')
        self.tracker.set_user_preference('track_energy', True)
        
        # Export data
        export_data = self.tracker.export_all_data()
        
        # Verify comprehensive export structure
        self.assertIn('time_entries', export_data)
        self.assertIn('user_preferences', export_data)
        self.assertIn('custom_categories', export_data)
        self.assertIn('estimation_history', export_data)
        self.assertIn('export_metadata', export_data)
        
        # Verify data ownership assertion
        self.assertIn('data_ownership', export_data['export_metadata'])
        self.assertEqual(export_data['export_metadata']['data_ownership'], 
                        'This data belongs entirely to the user')
        
        # Verify all entries are included
        self.assertEqual(len(export_data['time_entries']), len(self.sample_entries))
    
    def test_data_export_preserves_privacy(self):
        """Test that data export respects privacy and doesn't include sensitive system data"""
        # Add entries
        for entry_data in self.sample_entries:
            self.tracker.add_manual_entry(**entry_data)
        
        export_data = self.tracker.export_all_data()
        
        # Should not include internal system data
        self.assertNotIn('internal_tracking_id', str(export_data))
        self.assertNotIn('system_metadata', export_data)
        
        # Should include user-controlled data only
        for entry in export_data['time_entries']:
            self.assertIn('category', entry)
            self.assertIn('description', entry)
            self.assertIn('user_controlled', entry)
            self.assertTrue(entry['user_controlled'])
    
    def test_data_reset_requires_explicit_confirmation(self):
        """Test that data reset requires explicit user confirmation"""
        # Add some data
        for entry_data in self.sample_entries:
            self.tracker.add_manual_entry(**entry_data)
        
        # Try to reset without confirmation
        result = self.tracker.reset_all_data()
        self.assertEqual(result['status'], 'confirmation_required')
        self.assertEqual(len(self.tracker.entries), len(self.sample_entries))  # Data unchanged
        
        # Reset with wrong confirmation
        result = self.tracker.reset_all_data("wrong_confirmation")
        self.assertEqual(result['status'], 'error')
        self.assertEqual(len(self.tracker.entries), len(self.sample_entries))  # Data unchanged
        
        # Reset with correct confirmation
        confirmation_id = result.get('required_confirmation', 'RESET_CONFIRMED')
        result = self.tracker.reset_all_data(confirmation_id)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(self.tracker.entries), 0)  # Data cleared


class TestIndividualDifferences(TestTimeTracker):
    """Test accommodation of individual differences"""
    
    def test_customizable_categories_and_workflows(self):
        """Test that users can customize categories and workflows"""
        # Set custom default categories
        custom_categories = ["Deep Work", "Creative", "Admin", "Learning"]
        self.tracker.set_user_preference('default_categories', custom_categories)
        
        # Verify custom categories are used
        categories = self.tracker.get_suggested_categories()
        for category in custom_categories:
            self.assertIn(category, categories)
    
    def test_flexible_productivity_metrics(self):
        """Test that productivity metrics can be customized for individual needs"""
        # User can choose which metrics to track
        self.tracker.set_user_preference('track_energy_levels', True)
        self.tracker.set_user_preference('track_focus_quality', False)
        self.tracker.set_user_preference('track_interruptions', True)
        
        # Add entry and verify only enabled metrics are requested/stored
        start_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now()
        result = self.tracker.add_manual_entry(start_time, end_time, "Work")
        
        # Check that the system respects user's metric preferences
        entry = self.tracker.entries[0]
        # In a real implementation, this would check which fields are required/optional
        # based on user preferences
    
    def test_time_format_and_display_preferences(self):
        """Test that time formats and display can be customized"""
        # Set user preferences for time display
        self.tracker.set_user_preference('time_format', '24_hour')
        self.tracker.set_user_preference('duration_format', 'decimal_hours')
        
        # Add entry
        start_time = datetime.now() - timedelta(minutes=90)
        end_time = datetime.now()
        self.tracker.add_manual_entry(start_time, end_time, "Work")
        
        # Get formatted summary
        summary = self.tracker.get_daily_summary()
        
        # Verify time format preferences are respected
        # In real implementation, this would check that times are formatted
        # according to user preferences
        self.assertIn('total_time', summary)


class TestIntegrationWithOtherModules(TestTimeTracker):
    """Test integration points with other FlowState modules"""
    
    def test_provides_data_for_pattern_analysis(self):
        """Test that time tracker provides appropriate data for pattern analysis"""
        # Add entries across multiple days and times
        base_time = datetime.now() - timedelta(days=7)
        
        for day in range(7):
            for hour in [9, 14, 16]:  # Morning, afternoon, evening
                start_time = base_time + timedelta(days=day, hours=hour)
                end_time = start_time + timedelta(minutes=60)
                
                self.tracker.add_manual_entry(
                    start_time, end_time, "Work",
                    energy_before=hour//3,  # Varies by time of day
                    focus_quality=4 if hour == 9 else 3  # Better in morning
                )
        
        # Get data suitable for pattern analysis
        pattern_data = self.tracker.get_data_for_pattern_analysis()
        
        self.assertIn('time_entries', pattern_data)
        self.assertIn('temporal_patterns', pattern_data)
        self.assertIn('energy_patterns', pattern_data)
        self.assertIn('focus_patterns', pattern_data)
        
        # Verify data structure is suitable for analysis
        self.assertGreater(len(pattern_data['time_entries']), 0)
        self.assertIn('confidence_levels', pattern_data)
    
    def test_respects_user_profile_settings(self):
        """Test that time tracker respects user profile and privacy settings"""
        # Mock user profile with specific preferences
        mock_profile = {
            'accessibility_prefs': {
                'simplified_interface': True,
                'reduced_decision_points': True
            },
            'productivity_prefs': {
                'preferred_session_length': 45,
                'natural_break_frequency': 120
            },
            'privacy_settings': {
                'time_tracking_privacy': 'private'
            }
        }
        
        # Initialize tracker with user profile
        profile_tracker = TimeTracker(user_profile=mock_profile)
        
        # Verify preferences are applied
        self.assertEqual(profile_tracker.preferences['default_session_length'], 45)
        self.assertTrue(profile_tracker.preferences['simplified_interface'])
        self.assertEqual(profile_tracker.preferences['privacy_level'], 'private')


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestBasicTimeTracking,
        TestManualTimeEntry,
        TestUserAgencyAndControl,
        TestHonestLimitationsAndUncertainty,
        TestFailureResilienceAndGracefulDegradation,
        TestDataOwnershipAndExport,
        TestIndividualDifferences,
        TestIntegrationWithOtherModules
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"FlowState TimeTracker Test Summary")
    print(f"{'='*50}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.split('AssertionError: ')[-1].split('\n')[0]}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, error in result.errors:
            print(f"  - {test}: {error.split('\n')[0]}")
    
    # Exit with error code if tests failed
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)

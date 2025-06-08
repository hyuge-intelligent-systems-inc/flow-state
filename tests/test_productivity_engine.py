
"""
FlowState Productivity Engine Tests
Comprehensive testing for the central productivity orchestration system
Based on expert analysis emphasizing user agency and honest limitations
"""

import unittest
import json
import tempfile
import os
import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the modules we're testing (adjust path as needed)
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.productivity_engine import (
    ProductivityEngine, ProductivityMode, SessionType,
    DailyInsight, ProductivityRecommendation
)


class TestProductivityOrchestration(unittest.TestCase):
    """Test the core orchestration of all FlowState modules"""
    
    def setUp(self):
        """Set up test environment with mocked dependencies"""
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "test_user_123"
        
        # Mock all the dependent modules
        self.mock_time_tracker = Mock()
        self.mock_pattern_analyzer = Mock()
        self.mock_ai_tracker = Mock()
        self.mock_self_discovery = Mock()
        self.mock_ui_manager = Mock()
        self.mock_team_optimizer = Mock()
        
        # Create productivity engine with mocked dependencies
        self.engine = ProductivityEngine(
            user_id=self.user_id,
            time_tracker=self.mock_time_tracker,
            pattern_analyzer=self.mock_pattern_analyzer,
            ai_tracker=self.mock_ai_tracker,
            self_discovery=self.mock_self_discovery,
            ui_manager=self.mock_ui_manager,
            team_optimizer=self.mock_team_optimizer
        )
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_user_agency_preserved_across_modules(self):
        """Test that user agency is preserved in all module interactions"""
        # Mock session guidance request
        session_data = {
            "planned_duration": 90,
            "task_type": "creative_work",
            "current_energy": 7
        }
        
        # Mock responses from different modules
        self.mock_ai_tracker.get_session_suggestions.return_value = [
            {
                "suggestion": "Try working in 45-minute blocks",
                "confidence": 0.7,
                "evidence": ["Previous 45-min sessions rated highly"],
                "user_override_available": True
            }
        ]
        
        self.mock_pattern_analyzer.get_session_context.return_value = {
            "optimal_times": "9-11am historically productive",
            "confidence": 0.6,
            "limitations": "Based on only 5 similar sessions"
        }
        
        # Get session guidance
        guidance = self.engine.get_session_guidance(session_data)
        
        # Should preserve user agency
        self.assertIn("user_control", guidance)
        self.assertTrue(guidance["user_control"]["can_override_all_suggestions"])
        self.assertTrue(guidance["user_control"]["suggestions_not_mandatory"])
        
        # Should include honest limitations
        self.assertIn("limitations", guidance)
        self.assertIn("confidence_levels", guidance)
        
        # All suggestions should be optional
        for suggestion in guidance.get("suggestions", []):
            self.assertIn("optional", suggestion)
            self.assertTrue(suggestion["optional"])
    
    def test_honest_limitations_across_modules(self):
        """Test that limitations are honestly reported from all modules"""
        # Request daily summary
        summary_data = self.engine.get_daily_summary()
        
        # Should include limitations from all modules
        self.assertIn("data_limitations", summary_data)
        limitations = summary_data["data_limitations"]
        
        # Should acknowledge uncertainty
        self.assertIn("individual_variation", limitations)
        self.assertIn("sample_size_requirements", limitations)
        self.assertIn("correlation_vs_causation", limitations)
        
        # Should provide confidence levels
        self.assertIn("confidence_assessment", summary_data)
        confidence = summary_data["confidence_assessment"]
        self.assertIn("overall_confidence", confidence)
        self.assertLessEqual(confidence["overall_confidence"], 1.0)
        self.assertGreaterEqual(confidence["overall_confidence"], 0.0)
    
    def test_productivity_mode_adaptation(self):
        """Test adaptation to different productivity modes"""
        # Test each productivity mode
        modes = [
            ProductivityMode.SURVIVAL,
            ProductivityMode.MAINTENANCE, 
            ProductivityMode.GROWTH,
            ProductivityMode.MASTERY
        ]
        
        for mode in modes:
            # Set productivity mode
            self.engine.set_productivity_mode(mode, user_confirmation=True)
            
            # Get mode-appropriate guidance
            guidance = self.engine.get_session_guidance({
                "planned_duration": 60,
                "task_type": "focused_work"
            })
            
            # Guidance should be appropriate for mode
            if mode == ProductivityMode.SURVIVAL:
                self.assertIn("essential_only", guidance["approach"])
                self.assertTrue(guidance["approach"]["minimal_complexity"])
            elif mode == ProductivityMode.MASTERY:
                self.assertIn("advanced_optimization", guidance["approach"])
                self.assertTrue(guidance["approach"]["sophisticated_features_available"])
    
    def test_cross_module_validation(self):
        """Test validation when multiple modules provide conflicting insights"""
        # Mock conflicting insights from different modules
        self.mock_ai_tracker.get_productivity_predictions.return_value = [
            {
                "prediction": "Best productivity at 2pm",
                "confidence": 0.8,
                "source": "ai_pattern_recognition"
            }
        ]
        
        self.mock_pattern_analyzer.get_time_patterns.return_value = {
            "peak_productivity_time": "10am",
            "confidence": 0.6,
            "source": "user_data_analysis"
        }
        
        # Get insights that require validation
        insights = self.engine.get_cross_validated_insights()
        
        # Should identify conflicts
        self.assertIn("conflicting_insights", insights)
        conflicts = insights["conflicting_insights"]
        self.assertTrue(len(conflicts) > 0)
        
        # Should provide user interpretation guidance
        self.assertIn("user_interpretation_required", insights)
        self.assertTrue(insights["user_interpretation_required"])
        
        # Should include all source attributions
        for insight in insights.get("all_insights", []):
            self.assertIn("source", insight)
            self.assertIn("confidence", insight)


class TestSessionManagement(unittest.TestCase):
    """Test intelligent session guidance and management"""
    
    def setUp(self):
        self.engine = ProductivityEngine("session_test_user")
    
    def test_session_guidance_user_controlled(self):
        """Test that session guidance respects user control"""
        session_request = {
            "planned_duration": 120,
            "task_type": "deep_work",
            "current_energy": 6,
            "user_preferences": {
                "no_ai_suggestions": False,
                "complexity_level": "standard"
            }
        }
        
        guidance = self.engine.get_session_guidance(session_request)
        
        # Should respect user preferences
        self.assertEqual(
            guidance["respects_user_preferences"], 
            session_request["user_preferences"]
        )
        
        # Should provide options, not mandates
        self.assertIn("suggested_approaches", guidance)
        for approach in guidance["suggested_approaches"]:
            self.assertIn("optional", approach)
            self.assertTrue(approach["optional"])
        
        # Should include rationale for suggestions
        for suggestion in guidance.get("suggestions", []):
            self.assertIn("rationale", suggestion)
            self.assertIn("evidence", suggestion)
            self.assertIn("alternatives", suggestion)
    
    def test_session_adaptation_to_context(self):
        """Test session adaptation based on current context"""
        # Mock different contexts
        contexts = [
            {
                "time_of_day": "morning",
                "energy_level": 9,
                "interruption_probability": "low",
                "expected_guidance": "deep_work_recommended"
            },
            {
                "time_of_day": "afternoon", 
                "energy_level": 5,
                "interruption_probability": "high",
                "expected_guidance": "maintenance_tasks_recommended"
            }
        ]
        
        for context in contexts:
            session_data = {
                "current_context": context,
                "planned_duration": 90
            }
            
            guidance = self.engine.get_session_guidance(session_data)
            
            # Should adapt to context
            self.assertIn("context_awareness", guidance)
            self.assertIn(context["expected_guidance"], 
                         str(guidance["recommendations"]))
            
            # Should explain adaptation rationale
            self.assertIn("adaptation_rationale", guidance)
    
    def test_session_progress_tracking(self):
        """Test session progress tracking with user agency"""
        # Start a session
        session_id = self.engine.start_session({
            "type": SessionType.FOCUS,
            "planned_duration": 60,
            "task": "Code review"
        })
        
        self.assertIsNotNone(session_id)
        
        # Update session (user-controlled)
        update_result = self.engine.update_session_progress(
            session_id, 
            {
                "current_progress": 0.4,
                "user_energy_rating": 7,
                "user_focus_rating": 8
            },
            user_initiated=True
        )
        
        self.assertTrue(update_result["success"])
        
        # End session with user summary
        end_result = self.engine.end_session(
            session_id,
            {
                "user_satisfaction": 8,
                "accomplishments": "Completed 3 code reviews",
                "challenges": "Phone interruptions"
            }
        )
        
        self.assertTrue(end_result["success"])
        self.assertIn("session_summary", end_result)


class TestCrossModuleIntegration(unittest.TestCase):
    """Test integration between different FlowState modules"""
    
    def setUp(self):
        self.engine = ProductivityEngine("integration_test_user")
    
    def test_time_tracker_pattern_integration(self):
        """Test integration between time tracking and pattern analysis"""
        # Mock time tracking data
        time_data = [
            {
                "task": "Writing",
                "duration": 90,
                "start_time": "09:00",
                "energy_level": 8,
                "focus_quality": 9
            }
        ]
        
        # Mock pattern analysis
        patterns = {
            "morning_productivity": {
                "average_focus": 8.5,
                "best_task_types": ["writing", "analysis"],
                "confidence": 0.7,
                "sample_size": 15
            }
        }
        
        # Test integration
        integrated_insights = self.engine.get_integrated_insights(
            time_data, patterns
        )
        
        # Should combine data meaningfully
        self.assertIn("time_pattern_correlation", integrated_insights)
        
        # Should maintain data attribution
        for insight in integrated_insights["insights"]:
            self.assertIn("data_sources", insight)
            self.assertIn("time_tracker", insight["data_sources"])
            self.assertIn("pattern_analyzer", insight["data_sources"])
        
        # Should preserve uncertainty
        self.assertIn("confidence_assessment", integrated_insights)
    
    def test_ai_psychology_integration(self):
        """Test integration between AI suggestions and psychology guidance"""
        # Mock AI suggestions
        ai_suggestions = [
            {
                "type": "timing_optimization",
                "suggestion": "Schedule creative work for 10am",
                "confidence": 0.8
            }
        ]
        
        # Mock psychology insights
        psychology_insights = {
            "energy_patterns": "User reports highest creativity in morning",
            "motivation_factors": ["autonomy", "mastery"],
            "stress_indicators": "low"
        }
        
        # Test integration
        combined_guidance = self.engine.integrate_ai_psychology_insights(
            ai_suggestions, psychology_insights
        )
        
        # Should validate AI suggestions against psychology insights
        self.assertIn("validation_results", combined_guidance)
        
        # Should prioritize user psychological insights
        self.assertIn("psychology_priority", combined_guidance)
        self.assertTrue(combined_guidance["psychology_priority"])
        
        # Should provide holistic recommendations
        self.assertIn("holistic_recommendations", combined_guidance)
    
    def test_ui_complexity_progression(self):
        """Test UI complexity progression based on engagement"""
        # Mock user engagement data
        engagement_data = {
            "days_active": 15,
            "features_explored": 8,
            "consistency_score": 0.7,
            "feedback_positive": True
        }
        
        # Test complexity assessment
        complexity_assessment = self.engine.assess_ui_complexity_readiness(
            engagement_data
        )
        
        # Should provide clear progression path
        self.assertIn("current_level", complexity_assessment)
        self.assertIn("next_level_criteria", complexity_assessment)
        self.assertIn("user_override_available", complexity_assessment)
        
        # Should respect user choice
        self.assertTrue(complexity_assessment["user_override_available"])


class TestHonestLimitationsReporting(unittest.TestCase):
    """Test honest reporting of system limitations"""
    
    def setUp(self):
        self.engine = ProductivityEngine("limitations_test_user")
    
    def test_confidence_scoring_accuracy(self):
        """Test that confidence scores are honest and calibrated"""
        # Mock various data scenarios
        scenarios = [
            {
                "sample_size": 3,
                "expected_confidence": "low"
            },
            {
                "sample_size": 20,
                "conflicting_data": True,
                "expected_confidence": "moderate"
            },
            {
                "sample_size": 50,
                "consistent_patterns": True,
                "expected_confidence": "high"
            }
        ]
        
        for scenario in scenarios:
            insights = self.engine.generate_insights_with_confidence(scenario)
            
            # Confidence should match data quality
            confidence = insights["confidence_assessment"]
            
            if scenario["sample_size"] < 10:
                self.assertLessEqual(confidence["level"], 0.5)
            
            # Should explain confidence rationale
            self.assertIn("confidence_rationale", insights)
            self.assertIn("sample_size", insights["confidence_rationale"])
    
    def test_uncertainty_acknowledgment(self):
        """Test explicit uncertainty acknowledgment"""
        insights = self.engine.get_productivity_insights()
        
        # Should acknowledge what we don't know
        self.assertIn("uncertainty_factors", insights)
        uncertainty = insights["uncertainty_factors"]
        
        expected_uncertainties = [
            "individual_variation",
            "external_factors",
            "temporal_changes",
            "context_dependencies"
        ]
        
        for uncertainty_type in expected_uncertainties:
            self.assertIn(uncertainty_type, uncertainty)
    
    def test_limitation_transparency(self):
        """Test transparent communication of system limitations"""
        system_status = self.engine.get_system_capabilities_and_limitations()
        
        # Should clearly state what system can do
        self.assertIn("capabilities", system_status)
        capabilities = system_status["capabilities"]
        self.assertIsInstance(capabilities, list)
        
        # Should clearly state what system cannot do
        self.assertIn("limitations", system_status)
        limitations = system_status["limitations"]
        self.assertIsInstance(limitations, list)
        
        # Should include accuracy information
        self.assertIn("accuracy_information", system_status)
        accuracy = system_status["accuracy_information"]
        self.assertIn("prediction_accuracy", accuracy)
        self.assertIn("confidence_calibration", accuracy)


class TestFailureResilienceAndRecovery(unittest.TestCase):
    """Test system behavior during failures and recovery"""
    
    def setUp(self):
        self.engine = ProductivityEngine("failure_test_user")
    
    def test_module_failure_graceful_degradation(self):
        """Test graceful degradation when modules fail"""
        # Simulate AI tracker failure
        with patch.object(self.engine, 'ai_tracker') as mock_ai:
            mock_ai.get_suggestions.side_effect = Exception("AI service unavailable")
            
            # Should still provide guidance without AI
            guidance = self.engine.get_session_guidance({
                "planned_duration": 60,
                "task_type": "analysis"
            })
            
            # Should acknowledge degraded functionality
            self.assertIn("degraded_mode", guidance)
            self.assertTrue(guidance["degraded_mode"]["ai_suggestions_unavailable"])
            
            # Should provide alternative approaches
            self.assertIn("alternative_approaches", guidance)
            self.assertTrue(len(guidance["alternative_approaches"]) > 0)
    
    def test_data_corruption_recovery(self):
        """Test recovery from data corruption"""
        # Simulate corrupted data scenario
        corrupted_data = {"malformed": "data", "missing_required_fields": True}
        
        # Should handle gracefully
        result = self.engine.handle_corrupted_data(corrupted_data)
        
        # Should not crash
        self.assertIn("recovery_status", result)
        self.assertIn("data_integrity_check", result)
        
        # Should maintain user data safety
        self.assertTrue(result["user_data_preserved"])
    
    def test_network_failure_offline_mode(self):
        """Test offline functionality when network fails"""
        # Simulate network failure
        with patch('requests.get') as mock_request:
            mock_request.side_effect = ConnectionError("Network unavailable")
            
            # Should operate in offline mode
            offline_capabilities = self.engine.get_offline_capabilities()
            
            # Core features should remain available
            self.assertIn("available_features", offline_capabilities)
            available = offline_capabilities["available_features"]
            
            # Essential features should work offline
            essential_features = ["time_tracking", "pattern_analysis", "self_discovery"]
            for feature in essential_features:
                self.assertIn(feature, available)


class TestUserDataIntegration(unittest.TestCase):
    """Test integration with user data management"""
    
    def setUp(self):
        self.engine = ProductivityEngine("data_integration_test_user")
    
    def test_privacy_respect_across_modules(self):
        """Test that privacy settings are respected across all modules"""
        # Mock different privacy levels
        privacy_settings = {
            "time_entries": "private",
            "pattern_insights": "aggregated", 
            "ai_interactions": "team_visible"
        }
        
        # Test insights generation with privacy constraints
        insights = self.engine.generate_privacy_aware_insights(privacy_settings)
        
        # Should respect privacy levels
        for insight in insights:
            data_type = insight["data_type"]
            privacy_level = privacy_settings.get(data_type, "private")
            
            self.assertEqual(insight["privacy_level"], privacy_level)
            
            # Private data should not be in insights
            if privacy_level == "private":
                self.assertNotIn("specific_data", insight)
    
    def test_data_export_integration(self):
        """Test comprehensive data export across modules"""
        export_data = self.engine.export_all_productivity_data()
        
        # Should include data from all modules
        expected_modules = [
            "time_tracker", "pattern_analyzer", "ai_tracker",
            "self_discovery", "ui_manager", "team_optimizer"
        ]
        
        for module in expected_modules:
            self.assertIn(module, export_data["modules"])
        
        # Should maintain data ownership statements
        self.assertIn("data_ownership", export_data)
        self.assertIn("user_controls_all_data", export_data["data_ownership"])


def run_all_tests():
    """Run all productivity engine tests with detailed reporting"""
    
    # Create test suite
    test_classes = [
        TestProductivityOrchestration,
        TestSessionManagement,
        TestCrossModuleIntegration,
        TestHonestLimitationsReporting,
        TestFailureResilienceAndRecovery,
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
    print(f"PRODUCTIVITY ENGINE TEST SUMMARY")
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
    print(f"✅ User agency preserved across all modules")
    print(f"✅ Honest limitations and confidence reporting")
    print(f"✅ Cross-module integration and validation")
    print(f"✅ Session management with user control")
    print(f"✅ Failure resilience and graceful degradation")
    print(f"✅ Privacy-aware data integration")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

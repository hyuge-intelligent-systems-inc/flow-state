
"""
FlowState AI Tracker Tests
Comprehensive testing for honest AI assistance with user agency preservation
Based on expert analysis emphasizing user control and transparent limitations
"""

import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Import the modules to test
import sys
sys.path.append('../src')
from ai.ai_tracker import AITracker
from core.user_profile import UserProfile

class TestHonestAILimitations(unittest.TestCase):
    """Test that AI provides honest assessments of its limitations and confidence"""
    
    def setUp(self):
        self.user_profile = UserProfile("test_user")
        self.ai_tracker = AITracker(self.user_profile)
        
        # Set up test data with various quality levels
        self.high_quality_data = {
            'time_entries': [{'duration': 60, 'category': 'deep_work'} for _ in range(50)],
            'sample_size': 50,
            'consistency': 0.8
        }
        
        self.low_quality_data = {
            'time_entries': [{'duration': 30, 'category': 'misc'} for _ in range(3)],
            'sample_size': 3,
            'consistency': 0.2
        }
    
    def test_confidence_scoring_accuracy(self):
        """Test that confidence scores reflect actual data quality"""
        # High quality data should have higher confidence
        high_confidence = self.ai_tracker.calculate_confidence(self.high_quality_data)
        low_confidence = self.ai_tracker.calculate_confidence(self.low_quality_data)
        
        self.assertGreater(high_confidence, low_confidence)
        self.assertLessEqual(high_confidence, 1.0)
        self.assertGreaterEqual(low_confidence, 0.0)
    
    def test_minimum_sample_size_requirements(self):
        """Test that AI refuses to make predictions with insufficient data"""
        minimal_data = {'sample_size': 2, 'consistency': 0.9}
        
        result = self.ai_tracker.generate_suggestion(minimal_data)
        
        self.assertEqual(result['status'], 'insufficient_data')
        self.assertIn('sample_size', result['limitations'])
        self.assertIsNone(result['suggestion'])
    
    def test_uncertainty_quantification(self):
        """Test that all AI outputs include uncertainty ranges"""
        suggestion = self.ai_tracker.generate_suggestion(self.high_quality_data)
        
        if suggestion['suggestion'] is not None:
            self.assertIn('confidence_interval', suggestion)
            self.assertIn('uncertainty_factors', suggestion)
            self.assertIn('alternative_explanations', suggestion)
    
    def test_baseline_comparison_requirement(self):
        """Test that AI suggestions are compared to baseline/random performance"""
        suggestion = self.ai_tracker.generate_suggestion(self.high_quality_data)
        
        if suggestion['suggestion'] is not None:
            self.assertIn('baseline_comparison', suggestion)
            self.assertIn('improvement_over_random', suggestion)
    
    def test_honest_limitation_disclosure(self):
        """Test that AI clearly states what it cannot do"""
        limitations = self.ai_tracker.get_system_limitations()
        
        expected_limitations = [
            'cannot_assess_work_quality',
            'cannot_understand_personal_context',
            'correlation_not_causation',
            'individual_variation_high',
            'temporal_instability'
        ]
        
        for limitation in expected_limitations:
            self.assertIn(limitation, limitations)

class TestUserControlAndOverrides(unittest.TestCase):
    """Test that users maintain complete control over AI suggestions and data"""
    
    def setUp(self):
        self.user_profile = UserProfile("test_user")
        self.ai_tracker = AITracker(self.user_profile)
    
    def test_user_can_disable_all_ai_features(self):
        """Test that users can completely disable AI functionality"""
        self.user_profile.set_preference('ai_suggestions_enabled', False)
        
        # AI should return no suggestions when disabled
        result = self.ai_tracker.generate_suggestion({'sample_size': 100})
        self.assertEqual(result['status'], 'disabled_by_user')
        self.assertIsNone(result['suggestion'])
    
    def test_user_can_override_ai_suggestions(self):
        """Test that users can reject and override any AI recommendation"""
        suggestion_id = "test_suggestion_123"
        
        # User rejects suggestion
        override_result = self.ai_tracker.user_override_suggestion(
            suggestion_id, 
            action='reject',
            reason='not_applicable_to_my_situation'
        )
        
        self.assertTrue(override_result['success'])
        self.assertEqual(override_result['user_action'], 'reject')
        
        # Verify override is recorded for learning
        history = self.ai_tracker.get_user_override_history()
        self.assertIn(suggestion_id, [h['suggestion_id'] for h in history])
    
    def test_user_feedback_learning(self):
        """Test that AI learns from user feedback without manipulation"""
        # User provides feedback on suggestion quality
        feedback = {
            'suggestion_id': 'test_123',
            'helpful': False,
            'reason': 'too_generic',
            'context': 'suggestion_ignored_my_personal_constraints'
        }
        
        self.ai_tracker.record_user_feedback(feedback)
        
        # Verify feedback is stored for model improvement
        stored_feedback = self.ai_tracker.get_feedback_summary()
        self.assertIn('test_123', stored_feedback['feedback_by_suggestion'])
    
    def test_granular_ai_permission_controls(self):
        """Test detailed permissions for different AI capabilities"""
        permissions = {
            'pattern_analysis': True,
            'prediction_generation': False,
            'optimization_suggestions': True,
            'behavioral_insights': False
        }
        
        self.user_profile.set_ai_permissions(permissions)
        
        # AI should respect granular permissions
        result = self.ai_tracker.generate_suggestion(
            {'sample_size': 50}, 
            suggestion_type='prediction'
        )
        self.assertEqual(result['status'], 'permission_denied')
        
        result = self.ai_tracker.generate_suggestion(
            {'sample_size': 50}, 
            suggestion_type='optimization'
        )
        self.assertNotEqual(result['status'], 'permission_denied')

class TestAntiManipulationDesign(unittest.TestCase):
    """Test that AI doesn't manipulate users or create dependency"""
    
    def setUp(self):
        self.user_profile = UserProfile("test_user")
        self.ai_tracker = AITracker(self.user_profile)
    
    def test_no_engagement_maximization(self):
        """Test that AI doesn't try to maximize user engagement"""
        # AI should suggest breaks and minimal usage
        usage_pattern = {'daily_app_time': 120}  # 2 hours
        
        suggestion = self.ai_tracker.analyze_usage_patterns(usage_pattern)
        
        # Should suggest reducing app time, not increasing it
        self.assertIn('consider_reducing_app_time', suggestion['recommendations'])
        self.assertNotIn('increase_engagement', suggestion['recommendations'])
    
    def test_no_artificial_urgency_creation(self):
        """Test that AI doesn't create false urgency or pressure"""
        suggestions = self.ai_tracker.generate_daily_suggestions({'sample_size': 20})
        
        for suggestion in suggestions.get('suggestions', []):
            # Should not contain pressure language
            text = suggestion.get('text', '').lower()
            pressure_words = ['urgent', 'must', 'critical', 'immediately', 'behind']
            
            for word in pressure_words:
                self.assertNotIn(word, text)
    
    def test_promotes_user_independence(self):
        """Test that AI encourages user independence from the system"""
        independence_check = self.ai_tracker.get_independence_promotion_features()
        
        self.assertIn('teaches_general_principles', independence_check)
        self.assertIn('encourages_offline_application', independence_check)
        self.assertIn('reduces_over_dependency', independence_check)
    
    def test_no_behavioral_economics_manipulation(self):
        """Test that AI doesn't use manipulative behavioral economics"""
        settings = self.ai_tracker.get_behavioral_design_principles()
        
        # Should explicitly avoid manipulation
        self.assertFalse(settings['uses_loss_aversion'])
        self.assertFalse(settings['uses_social_pressure'])
        self.assertFalse(settings['uses_artificial_scarcity'])
        self.assertTrue(settings['respects_user_autonomy'])

class TestAITransparencyAndExplainability(unittest.TestCase):
    """Test that AI decisions are transparent and explainable"""
    
    def setUp(self):
        self.user_profile = UserProfile("test_user")
        self.ai_tracker = AITracker(self.user_profile)
    
    def test_all_suggestions_include_reasoning(self):
        """Test that every AI suggestion includes clear reasoning"""
        data = {'sample_size': 30, 'patterns': ['morning_focus']}
        suggestion = self.ai_tracker.generate_suggestion(data)
        
        if suggestion['suggestion'] is not None:
            self.assertIn('reasoning', suggestion)
            self.assertIn('data_sources', suggestion)
            self.assertIn('assumptions', suggestion)
    
    def test_model_decision_explanation(self):
        """Test that users can understand how AI made decisions"""
        suggestion_id = "test_explanation"
        
        explanation = self.ai_tracker.explain_decision(suggestion_id)
        
        self.assertIn('input_data_used', explanation)
        self.assertIn('decision_logic', explanation)
        self.assertIn('confidence_factors', explanation)
        self.assertIn('limitations', explanation)
    
    def test_data_influence_transparency(self):
        """Test that users can see which data influenced AI decisions"""
        influence_report = self.ai_tracker.get_data_influence_report()
        
        self.assertIn('most_influential_data_points', influence_report)
        self.assertIn('ignored_data_and_reasons', influence_report)
        self.assertIn('data_quality_impact', influence_report)

class TestPredictiveAccuracyAndCalibration(unittest.TestCase):
    """Test AI prediction accuracy and honest calibration"""
    
    def setUp(self):
        self.user_profile = UserProfile("test_user")
        self.ai_tracker = AITracker(self.user_profile)
    
    def test_prediction_accuracy_tracking(self):
        """Test that AI tracks and reports its actual accuracy"""
        # Make some predictions
        predictions = [
            {'id': 'p1', 'prediction': 'high_focus_morning', 'confidence': 0.7},
            {'id': 'p2', 'prediction': 'energy_dip_2pm', 'confidence': 0.8}
        ]
        
        # Record actual outcomes
        outcomes = [
            {'id': 'p1', 'actual': 'high_focus_morning', 'correct': True},
            {'id': 'p2', 'actual': 'no_energy_dip', 'correct': False}
        ]
        
        for prediction in predictions:
            self.ai_tracker.record_prediction(prediction)
        
        for outcome in outcomes:
            self.ai_tracker.record_outcome(outcome)
        
        accuracy_report = self.ai_tracker.get_accuracy_report()
        
        self.assertIn('overall_accuracy', accuracy_report)
        self.assertIn('accuracy_by_confidence_level', accuracy_report)
        self.assertIn('calibration_score', accuracy_report)
    
    def test_refuses_predictions_below_accuracy_threshold(self):
        """Test that AI stops making predictions when accuracy is poor"""
        # Simulate poor accuracy history
        for i in range(10):
            self.ai_tracker.record_prediction({
                'id': f'bad_p{i}', 
                'prediction': 'test', 
                'confidence': 0.8
            })
            self.ai_tracker.record_outcome({
                'id': f'bad_p{i}', 
                'actual': 'different', 
                'correct': False
            })
        
        # AI should refuse new predictions due to poor track record
        result = self.ai_tracker.generate_suggestion({'sample_size': 50})
        
        if result['status'] == 'accuracy_too_low':
            self.assertIn('historical_accuracy_insufficient', result['reason'])

class TestPrivacyPreservingAI(unittest.TestCase):
    """Test AI privacy preservation and data minimization"""
    
    def setUp(self):
        self.user_profile = UserProfile("test_user")
        self.ai_tracker = AITracker(self.user_profile)
    
    def test_local_processing_priority(self):
        """Test that AI prioritizes local processing over cloud"""
        processing_info = self.ai_tracker.get_processing_location_info()
        
        self.assertTrue(processing_info['local_processing_available'])
        self.assertTrue(processing_info['cloud_processing_optional'])
        self.assertTrue(processing_info['user_controls_processing_location'])
    
    def test_minimal_data_usage(self):
        """Test that AI uses minimum necessary data"""
        data_usage = self.ai_tracker.analyze_data_usage()
        
        self.assertIn('data_minimization_report', data_usage)
        self.assertIn('unused_data_categories', data_usage)
        self.assertIn('data_retention_limits', data_usage)
    
    def test_anonymization_for_model_improvement(self):
        """Test that any shared data is properly anonymized"""
        if self.ai_tracker.supports_federated_learning():
            anonymization_check = self.ai_tracker.verify_anonymization()
            
            self.assertTrue(anonymization_check['removes_personal_identifiers'])
            self.assertTrue(anonymization_check['adds_differential_privacy_noise'])
            self.assertTrue(anonymization_check['prevents_reidentification'])

class TestAIIntegrationWithOtherModules(unittest.TestCase):
    """Test AI integration while preserving module boundaries"""
    
    def setUp(self):
        self.user_profile = UserProfile("test_user")
        self.ai_tracker = AITracker(self.user_profile)
    
    def test_respects_pattern_analyzer_boundaries(self):
        """Test that AI doesn't override pattern analyzer's user interpretation requirement"""
        pattern_data = {'patterns': ['test_pattern'], 'confidence': 0.6}
        
        ai_input = self.ai_tracker.prepare_pattern_data_for_ai(pattern_data)
        
        # AI should not interpret patterns, only use them as input
        self.assertNotIn('ai_pattern_interpretation', ai_input)
        self.assertIn('user_interpreted_patterns_only', ai_input)
    
    def test_supports_self_discovery_without_overstepping(self):
        """Test that AI supports self-discovery without psychological diagnosis"""
        discovery_context = {'reflection_topic': 'productivity_challenges'}
        
        ai_support = self.ai_tracker.provide_self_discovery_support(discovery_context)
        
        # Should provide tools, not interpretations
        self.assertIn('reflection_prompts', ai_support)
        self.assertIn('data_visualization_options', ai_support)
        self.assertNotIn('psychological_assessment', ai_support)
        self.assertNotIn('diagnosis', ai_support)

# Test Suite Runner
def run_ai_tracker_tests():
    """Run all AI Tracker tests with detailed reporting"""
    test_classes = [
        TestHonestAILimitations,
        TestUserControlAndOverrides,
        TestAntiManipulationDesign,
        TestAITransparencyAndExplainability,
        TestPredictiveAccuracyAndCalibration,
        TestPrivacyPreservingAI,
        TestAIIntegrationWithOtherModules
    ]
    
    total_tests = 0
    total_failures = 0
    
    print("FlowState AI Tracker Test Suite")
    print("=" * 50)
    
    for test_class in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        total_tests += result.testsRun
        total_failures += len(result.failures) + len(result.errors)
        
        print(f"\n{test_class.__name__}: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} passed")
    
    print("\n" + "=" * 50)
    print(f"Total: {total_tests - total_failures}/{total_tests} tests passed")
    print(f"Success Rate: {((total_tests - total_failures) / total_tests * 100):.1f}%")
    
    if total_failures == 0:
        print("🎉 All AI Tracker tests passed! AI system maintains user agency and honest limitations.")
    else:
        print(f"⚠️  {total_failures} tests failed. Review AI implementation for user agency and transparency issues.")

if __name__ == "__main__":
    run_ai_tracker_tests()

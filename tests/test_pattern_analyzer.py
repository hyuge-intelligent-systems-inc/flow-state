

"""
FlowState Pattern Analyzer Tests
Comprehensive testing for ethical pattern analysis functionality

Key testing principles implemented:
- Test user interpretation requirements (no AI diagnosis)
- Verify transparent limitations and uncertainty handling
- Validate collaborative self-discovery approach
- Ensure conservative confidence thresholds
- Test minimum sample size requirements
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
from typing import Dict, Any, List

# Import the modules we're testing
import sys
sys.path.append('../src/core')
from pattern_analyzer import PatternAnalyzer, PatternInsight, ReflectionPrompt, UserExperiment
from time_tracker import TimeEntry


class TestPatternAnalyzer(unittest.TestCase):
    """Base test class for Pattern Analyzer functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.analyzer = PatternAnalyzer()
        
        # Create comprehensive test data spanning multiple weeks
        self.test_entries = self._create_test_time_entries()
        
        # Add test entries to analyzer
        for entry in self.test_entries:
            self.analyzer.add_time_entry(entry)
    
    def _create_test_time_entries(self) -> List[TimeEntry]:
        """Create realistic test time entries for pattern analysis"""
        entries = []
        base_date = datetime.now() - timedelta(days=30)
        
        # Create entries with clear patterns for testing
        for week in range(4):
            for day in range(7):
                current_date = base_date + timedelta(weeks=week, days=day)
                
                # Morning work session (consistent pattern)
                if day < 5:  # Weekdays only
                    morning_start = current_date.replace(hour=9, minute=0)
                    morning_end = morning_start + timedelta(hours=2)
                    entries.append(TimeEntry(
                        start_time=morning_start,
                        end_time=morning_end,
                        category="Deep Work",
                        description="Morning focus session",
                        energy_before=4 if day < 3 else 3,  # Energy varies by week day
                        energy_after=4,
                        focus_quality=5 if day < 3 else 4,  # Better focus early week
                        confidence_score=0.9
                    ))
                
                # Afternoon meeting pattern
                if day in [1, 3]:  # Tuesday, Thursday
                    meeting_start = current_date.replace(hour=14, minute=0)
                    meeting_end = meeting_start + timedelta(hours=1)
                    entries.append(TimeEntry(
                        start_time=meeting_start,
                        end_time=meeting_end,
                        category="Meeting",
                        description="Team meeting",
                        energy_before=3,
                        energy_after=2,  # Meetings drain energy
                        focus_quality=2,
                        confidence_score=0.8
                    ))
                
                # Weekend different pattern
                if day >= 5:  # Weekends
                    weekend_start = current_date.replace(hour=10, minute=0)
                    weekend_end = weekend_start + timedelta(hours=1)
                    entries.append(TimeEntry(
                        start_time=weekend_start,
                        end_time=weekend_end,
                        category="Personal Project",
                        description="Weekend creative work",
                        energy_before=4,
                        energy_after=5,  # Personal work energizes
                        focus_quality=4,
                        confidence_score=0.7
                    ))
        
        return entries


class TestEthicalPatternAnalysis(TestPatternAnalyzer):
    """Test ethical pattern analysis that requires user interpretation"""
    
    def test_no_ai_diagnosis_or_prescriptive_advice(self):
        """Test that analyzer never makes diagnosis or gives prescriptive advice"""
        patterns = self.analyzer.analyze_time_patterns()
        
        # Verify no diagnostic language
        pattern_text = str(patterns)
        forbidden_words = [
            "you should", "you must", "you need to", "diagnose", 
            "disorder", "problem", "fix", "cure", "treatment"
        ]
        
        for word in forbidden_words:
            self.assertNotIn(word.lower(), pattern_text.lower(), 
                           f"Analyzer should not use prescriptive language: '{word}'")
        
        # Verify observational language is used
        observational_words = [
            "observation", "pattern", "correlation", "appears", 
            "might", "could", "seems", "data shows"
        ]
        
        pattern_text_lower = pattern_text.lower()
        has_observational = any(word in pattern_text_lower for word in observational_words)
        self.assertTrue(has_observational, "Analyzer should use observational language")
    
    def test_user_interpretation_required_for_all_insights(self):
        """Test that all insights explicitly require user interpretation"""
        patterns = self.analyzer.analyze_time_patterns()
        
        # Every insight should require user interpretation
        for insight in patterns.get('insights', []):
            self.assertIn('user_interpretation_required', insight)
            self.assertTrue(insight['user_interpretation_required'])
            self.assertIn('reflection_questions', insight)
            self.assertGreater(len(insight['reflection_questions']), 0)
    
    def test_conservative_confidence_thresholds(self):
        """Test that confidence thresholds are conservative"""
        # Test with minimal data (should have low confidence)
        minimal_analyzer = PatternAnalyzer()
        
        # Add only 3 entries (below minimum threshold)
        for i in range(3):
            entry = self.test_entries[i]
            minimal_analyzer.add_time_entry(entry)
        
        patterns = minimal_analyzer.analyze_time_patterns()
        
        # Should indicate insufficient data
        self.assertIn('insufficient_data', patterns)
        self.assertIn('minimum_entries_needed', patterns['insufficient_data'])
        self.assertLess(patterns['insufficient_data']['current_entries'], 
                       patterns['insufficient_data']['minimum_entries_needed'])
    
    def test_sample_size_requirements_enforced(self):
        """Test that minimum sample size requirements are enforced"""
        # Test various analysis types with insufficient data
        insufficient_analyzer = PatternAnalyzer()
        
        # Add only 5 entries
        for entry in self.test_entries[:5]:
            insufficient_analyzer.add_time_entry(entry)
        
        # Energy pattern analysis
        energy_patterns = insufficient_analyzer.analyze_energy_patterns()
        self.assertIn('sample_size_warning', energy_patterns)
        self.assertIn('reliability_limited', energy_patterns)
        
        # Day-of-week analysis
        dow_patterns = insufficient_analyzer.analyze_day_of_week_patterns()
        self.assertIn('insufficient_data_for_reliable_patterns', dow_patterns)
    
    def test_correlation_vs_causation_warnings(self):
        """Test that correlation vs causation warnings are included"""
        patterns = self.analyzer.analyze_time_patterns()
        
        # Every correlation should include causation warning
        for insight in patterns.get('insights', []):
            if 'correlation' in insight.get('type', ''):
                self.assertIn('limitations', insight)
                limitations_text = str(insight['limitations']).lower()
                self.assertIn('correlation', limitations_text)
                self.assertIn('causation', limitations_text)


class TestTransparentLimitations(TestPatternAnalyzer):
    """Test transparent limitations and uncertainty handling"""
    
    def test_every_insight_includes_clear_limitations(self):
        """Test that every insight includes honest limitations"""
        patterns = self.analyzer.analyze_time_patterns()
        
        for insight in patterns.get('insights', []):
            self.assertIn('limitations', insight)
            self.assertIn('confidence_level', insight)
            self.assertIn('sample_size', insight)
            
            # Limitations should be meaningful, not generic
            limitations = insight['limitations']
            self.assertGreater(len(limitations), 20, "Limitations should be detailed")
    
    def test_confidence_levels_are_realistic(self):
        """Test that confidence levels are realistic and honest"""
        patterns = self.analyzer.analyze_time_patterns()
        
        for insight in patterns.get('insights', []):
            confidence = insight.get('confidence_level', 0)
            
            # Confidence should be conservative (not overconfident)
            self.assertLessEqual(confidence, 0.8, "Confidence should be conservative")
            self.assertGreaterEqual(confidence, 0.1, "Confidence should be meaningful")
            
            # Higher confidence should require more data
            sample_size = insight.get('sample_size', 0)
            if confidence > 0.6:
                self.assertGreaterEqual(sample_size, 20, 
                                      "High confidence requires large sample size")
    
    def test_alternative_explanations_provided(self):
        """Test that alternative explanations are provided for patterns"""
        patterns = self.analyzer.analyze_energy_patterns()
        
        for insight in patterns.get('insights', []):
            self.assertIn('alternative_explanations', insight)
            alternatives = insight['alternative_explanations']
            self.assertGreater(len(alternatives), 0, 
                             "Should provide alternative explanations")
            
            # Alternatives should be substantive
            for alt in alternatives:
                self.assertGreater(len(alt), 10, "Alternatives should be detailed")
    
    def test_data_quality_assessment_included(self):
        """Test that data quality assessment is included in results"""
        patterns = self.analyzer.analyze_time_patterns()
        
        self.assertIn('data_quality_assessment', patterns)
        quality = patterns['data_quality_assessment']
        
        self.assertIn('total_entries', quality)
        self.assertIn('confidence_distribution', quality)
        self.assertIn('completeness_score', quality)
        self.assertIn('reliability_notes', quality)


class TestCollaborativeSelfDiscovery(TestPatternAnalyzer):
    """Test collaborative self-discovery features"""
    
    def test_reflection_prompts_are_thoughtful_and_open_ended(self):
        """Test that reflection prompts encourage self-discovery"""
        prompts = self.analyzer.generate_reflection_prompts()
        
        for prompt in prompts:
            self.assertIn('question', prompt)
            self.assertIn('category', prompt)
            
            question = prompt['question']
            
            # Questions should be open-ended (not yes/no)
            self.assertFalse(question.lower().startswith('do you'), 
                           "Questions should be open-ended, not yes/no")
            self.assertFalse(question.lower().startswith('are you'), 
                           "Questions should be open-ended, not yes/no")
            
            # Questions should encourage reflection
            reflection_words = ['how', 'what', 'when', 'where', 'why', 'which']
            starts_with_reflection = any(question.lower().startswith(word) 
                                       for word in reflection_words)
            self.assertTrue(starts_with_reflection, 
                          f"Question should encourage reflection: {question}")
    
    def test_user_experiment_suggestions_are_testable(self):
        """Test that suggested experiments are testable by users"""
        experiments = self.analyzer.suggest_user_experiments()
        
        for experiment in experiments:
            self.assertIn('hypothesis', experiment)
            self.assertIn('test_method', experiment)
            self.assertIn('duration_days', experiment)
            self.assertIn('measurement_approach', experiment)
            
            # Experiments should be reasonable in duration
            duration = experiment['duration_days']
            self.assertGreaterEqual(duration, 3, "Experiments should be at least 3 days")
            self.assertLessEqual(duration, 30, "Experiments should be at most 30 days")
            
            # Test method should be specific and actionable
            test_method = experiment['test_method']
            self.assertGreater(len(test_method), 20, "Test method should be detailed")
    
    def test_insight_recording_preserves_user_attribution(self):
        """Test that user insights are properly attributed to user"""
        user_insight = "I notice I'm more creative in the morning after coffee"
        
        result = self.analyzer.record_user_insight(
            insight=user_insight,
            category="energy_patterns",
            confidence="high",
            supporting_data=["morning_sessions", "energy_ratings"]
        )
        
        self.assertEqual(result['status'], 'recorded')
        
        # Retrieve recorded insights
        insights = self.analyzer.get_user_insights()
        user_insights = [i for i in insights if i['insight'] == user_insight]
        
        self.assertEqual(len(user_insights), 1)
        recorded = user_insights[0]
        
        self.assertEqual(recorded['source'], 'user')
        self.assertEqual(recorded['user_controlled'], True)
        self.assertIn('recorded_date', recorded)
    
    def test_pattern_discovery_session_supports_exploration(self):
        """Test that discovery sessions support user-led exploration"""
        session = self.analyzer.start_discovery_session("energy_patterns")
        
        self.assertIn('session_id', session)
        self.assertIn('exploration_areas', session)
        self.assertIn('guided_questions', session)
        self.assertIn('data_available', session)
        
        # Should provide data for exploration without conclusions
        data = session['data_available']
        self.assertIn('energy_by_time', data)
        self.assertIn('energy_by_day', data)
        
        # Should not include pre-drawn conclusions
        self.assertNotIn('conclusions', session)
        self.assertNotIn('recommendations', session)


class TestPatternAnalysisTypes(TestPatternAnalyzer):
    """Test specific types of pattern analysis"""
    
    def test_time_of_day_pattern_analysis(self):
        """Test time-of-day pattern analysis with user interpretation"""
        patterns = self.analyzer.analyze_time_of_day_patterns()
        
        self.assertIn('hourly_distribution', patterns)
        self.assertIn('peak_hours', patterns)
        self.assertIn('user_interpretation_required', patterns)
        
        # Should identify morning pattern from test data
        peak_hours = patterns['peak_hours']
        morning_peak = any(8 <= hour <= 11 for hour in peak_hours)
        self.assertTrue(morning_peak, "Should identify morning peak from test data")
        
        # Should include reflection questions
        self.assertIn('reflection_questions', patterns)
        questions = patterns['reflection_questions']
        self.assertIn('What times feel most natural for focused work?', 
                     str(questions))
    
    def test_day_of_week_pattern_analysis(self):
        """Test day-of-week pattern analysis"""
        patterns = self.analyzer.analyze_day_of_week_patterns()
        
        self.assertIn('daily_patterns', patterns)
        self.assertIn('weekday_vs_weekend', patterns)
        
        # Should identify weekday work pattern from test data
        daily = patterns['daily_patterns']
        weekday_pattern = any(daily[day]['total_minutes'] > 0 
                            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        self.assertTrue(weekday_pattern, "Should identify weekday patterns")
        
        # Should require user interpretation
        self.assertTrue(patterns['user_interpretation_required'])
    
    def test_energy_pattern_analysis(self):
        """Test energy pattern analysis with limitations"""
        patterns = self.analyzer.analyze_energy_patterns()
        
        if patterns.get('sufficient_data', False):
            self.assertIn('energy_trends', patterns)
            self.assertIn('energy_correlations', patterns)
            
            # Should include energy pattern observations
            trends = patterns['energy_trends']
            self.assertIn('observations', trends)
            
            # Should include limitations about self-reported data
            self.assertIn('limitations', patterns)
            limitations_text = str(patterns['limitations']).lower()
            self.assertIn('self-reported', limitations_text)
    
    def test_focus_quality_analysis(self):
        """Test focus quality analysis with correlation warnings"""
        patterns = self.analyzer.analyze_focus_patterns()
        
        if patterns.get('sufficient_data', False):
            self.assertIn('focus_correlations', patterns)
            
            # Should warn about correlation vs causation
            for correlation in patterns['focus_correlations']:
                self.assertIn('correlation_warning', correlation)
                warning = correlation['correlation_warning'].lower()
                self.assertIn('does not imply causation', warning)
    
    def test_session_duration_analysis(self):
        """Test session duration pattern analysis"""
        patterns = self.analyzer.analyze_session_duration_patterns()
        
        self.assertIn('duration_statistics', patterns)
        self.assertIn('optimal_ranges', patterns)
        
        # Should include user context questions
        self.assertIn('reflection_questions', patterns)
        questions = str(patterns['reflection_questions']).lower()
        self.assertIn('what duration feels most productive', questions)


class TestUserControlAndAgency(TestPatternAnalyzer):
    """Test user control and agency preservation"""
    
    def test_users_can_override_all_pattern_interpretations(self):
        """Test that users can override any pattern interpretation"""
        patterns = self.analyzer.analyze_time_patterns()
        
        # User disagrees with a pattern
        pattern_id = patterns['insights'][0]['insight_id']
        
        result = self.analyzer.override_pattern_interpretation(
            pattern_id=pattern_id,
            user_interpretation="I disagree - this pattern doesn't apply to me",
            reasoning="My work style is different from what the data suggests"
        )
        
        self.assertEqual(result['status'], 'override_recorded')
        self.assertTrue(result['user_interpretation_preserved'])
        
        # Verify override is stored and respected
        updated_patterns = self.analyzer.analyze_time_patterns()
        overridden_insight = next(
            (i for i in updated_patterns['insights'] if i['insight_id'] == pattern_id),
            None
        )
        
        if overridden_insight:
            self.assertIn('user_override', overridden_insight)
            self.assertEqual(overridden_insight['user_override']['active'], True)
    
    def test_users_can_customize_analysis_parameters(self):
        """Test that users can customize analysis parameters"""
        # Set custom parameters
        custom_params = {
            'minimum_confidence_threshold': 0.7,
            'minimum_sample_size': 15,
            'include_weekend_data': False,
            'focus_on_categories': ['Deep Work', 'Creative']
        }
        
        self.analyzer.set_analysis_parameters(custom_params)
        
        # Verify parameters are applied
        stored_params = self.analyzer.get_analysis_parameters()
        self.assertEqual(stored_params['minimum_confidence_threshold'], 0.7)
        self.assertEqual(stored_params['include_weekend_data'], False)
        
        # Run analysis with custom parameters
        patterns = self.analyzer.analyze_time_patterns()
        
        # Should respect custom thresholds
        if patterns.get('insights'):
            for insight in patterns['insights']:
                self.assertGreaterEqual(insight['confidence_level'], 0.7)
    
    def test_users_can_disable_specific_analysis_types(self):
        """Test that users can disable specific types of analysis"""
        # Disable energy analysis
        self.analyzer.set_analysis_preferences({
            'energy_analysis_enabled': False,
            'focus_analysis_enabled': True,
            'time_analysis_enabled': True
        })
        
        # Request full analysis
        patterns = self.analyzer.analyze_time_patterns()
        
        # Should not include energy insights
        insight_types = [insight.get('type') for insight in patterns.get('insights', [])]
        energy_types = [t for t in insight_types if 'energy' in str(t).lower()]
        self.assertEqual(len(energy_types), 0, "Energy analysis should be disabled")
    
    def test_analysis_can_be_completely_user_driven(self):
        """Test that analysis can be completely driven by user questions"""
        user_question = "When am I most creative and energized?"
        
        result = self.analyzer.analyze_for_user_question(user_question)
        
        self.assertIn('question', result)
        self.assertEqual(result['question'], user_question)
        self.assertIn('relevant_data', result)
        self.assertIn('exploration_suggestions', result)
        
        # Should not provide conclusions, only data for user exploration
        self.assertNotIn('conclusions', result)
        self.assertNotIn('answers', result)
        self.assertTrue(result['user_interpretation_required'])


class TestPrivacyAndDataHandling(TestPatternAnalyzer):
    """Test privacy preservation and data handling"""
    
    def test_no_sensitive_data_exposed_in_patterns(self):
        """Test that sensitive data is not exposed in pattern analysis"""
        # Add entry with sensitive description
        sensitive_entry = TimeEntry(
            start_time=datetime.now() - timedelta(hours=1),
            end_time=datetime.now(),
            category="Personal",
            description="Private medical appointment",
            confidence_score=0.9
        )
        
        self.analyzer.add_time_entry(sensitive_entry)
        patterns = self.analyzer.analyze_time_patterns()
        
        # Should not expose sensitive descriptions
        pattern_text = str(patterns)
        self.assertNotIn("medical appointment", pattern_text)
        self.assertNotIn("Private", pattern_text)
    
    def test_aggregated_patterns_preserve_privacy(self):
        """Test that aggregated patterns preserve individual privacy"""
        patterns = self.analyzer.analyze_time_patterns()
        
        # Should contain aggregated statistics, not individual entries
        for insight in patterns.get('insights', []):
            insight_text = str(insight)
            # Should not contain specific timestamps or descriptions
            self.assertNotRegex(insight_text, r'\d{4}-\d{2}-\d{2}', 
                              "Should not contain specific dates")
    
    def test_user_controls_data_sharing_for_patterns(self):
        """Test that users control what data is used in pattern analysis"""
        # Set privacy preferences
        self.analyzer.set_privacy_preferences({
            'include_personal_categories': False,
            'include_energy_data': True,
            'include_descriptions': False
        })
        
        patterns = self.analyzer.analyze_time_patterns()
        
        # Should respect privacy preferences
        insights = patterns.get('insights', [])
        for insight in insights:
            # Should not include personal category analysis
            self.assertNotIn('Personal', str(insight))


class TestIntegrationWithOtherModules(TestPatternAnalyzer):
    """Test integration with other FlowState modules"""
    
    def test_provides_data_for_self_discovery_module(self):
        """Test that analyzer provides appropriate data for self-discovery"""
        discovery_data = self.analyzer.get_data_for_self_discovery()
        
        self.assertIn('pattern_observations', discovery_data)
        self.assertIn('reflection_prompts', discovery_data)
        self.assertIn('user_experiments', discovery_data)
        self.assertIn('data_limitations', discovery_data)
        
        # Should include user interpretation requirements
        for observation in discovery_data['pattern_observations']:
            self.assertTrue(observation['user_interpretation_required'])
    
    def test_accepts_ai_insights_for_correlation(self):
        """Test that analyzer can incorporate AI insights while preserving user agency"""
        ai_insight = {
            'type': 'temporal_pattern',
            'observation': 'Morning sessions show 20% higher focus ratings',
            'confidence': 0.6,
            'source': 'ai_tracker'
        }
        
        result = self.analyzer.incorporate_ai_insight(ai_insight)
        
        self.assertEqual(result['status'], 'incorporated')
        self.assertTrue(result['user_validation_required'])
        
        # AI insights should be marked as requiring user validation
        patterns = self.analyzer.analyze_time_patterns()
        ai_insights = [i for i in patterns.get('insights', []) 
                      if i.get('source') == 'ai_tracker']
        
        for insight in ai_insights:
            self.assertTrue(insight['requires_user_validation'])
            self.assertIn('ai_confidence', insight)
    
    def test_supports_user_profile_customization(self):
        """Test that analyzer respects user profile settings"""
        mock_user_profile = {
            'accessibility_prefs': {
                'simplified_interface': True,
                'extended_processing_time': True
            },
            'productivity_prefs': {
                'prefers_visual_patterns': True,
                'detail_level': 'summary'
            }
        }
        
        # Initialize analyzer with user profile
        profile_analyzer = PatternAnalyzer(user_profile=mock_user_profile)
        
        # Add test data
        for entry in self.test_entries[:10]:
            profile_analyzer.add_time_entry(entry)
        
        patterns = profile_analyzer.analyze_time_patterns()
        
        # Should respect accessibility preferences
        self.assertTrue(patterns.get('simplified_presentation', False))
        self.assertEqual(patterns.get('detail_level'), 'summary')


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestEthicalPatternAnalysis,
        TestTransparentLimitations,
        TestCollaborativeSelfDiscovery,
        TestPatternAnalysisTypes,
        TestUserControlAndAgency,
        TestPrivacyAndDataHandling,
        TestIntegrationWithOtherModules
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"FlowState PatternAnalyzer Test Summary")
    print(f"{'='*60}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.split('AssertionError: ')[-1].split(chr(10))[0]}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, error in result.errors:
            print(f"  - {test}: {error.split(chr(10))[0]}")
    
    # Exit with error code if tests failed
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)

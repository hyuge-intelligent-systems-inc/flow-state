
"""
FlowState Self-Discovery Psychology Tests
Comprehensive testing for ethical psychology support functionality

Key testing principles implemented:
- Test professional boundaries and scope limitations
- Verify no psychological diagnosis or assessment by AI
- Validate user-controlled self-reflection and discovery
- Ensure proper professional referral protocols
- Test ethical safeguards and transparency
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
from typing import Dict, Any, List

# Import the modules we're testing
import sys
sys.path.append('../src/psychology')
from self_discovery import SelfDiscoveryGuide, DiscoverySession, ReflectionPrompt, ProfessionalReferralAssessment


class TestSelfDiscoveryGuide(unittest.TestCase):
    """Base test class for Self-Discovery Guide functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.guide = SelfDiscoveryGuide()
        
        # Create test user data for discovery sessions
        self.test_user_data = {
            'productivity_patterns': self._create_test_productivity_patterns(),
            'energy_patterns': self._create_test_energy_patterns(),
            'user_reported_challenges': self._create_test_challenges()
        }
        
        # Set up mock pattern data
        self.guide.set_user_data(self.test_user_data)
    
    def _create_test_productivity_patterns(self) -> Dict[str, Any]:
        """Create test productivity patterns for discovery"""
        return {
            'peak_hours': [9, 10, 11],
            'low_energy_times': [14, 15],
            'productive_days': ['Monday', 'Tuesday', 'Wednesday'],
            'challenging_days': ['Friday'],
            'focus_session_patterns': {
                'average_duration': 45,
                'interruption_frequency': 'moderate',
                'best_environment': 'quiet_space'
            }
        }
    
    def _create_test_energy_patterns(self) -> Dict[str, Any]:
        """Create test energy patterns for discovery"""
        return {
            'morning_energy': 'high',
            'afternoon_energy': 'moderate',
            'evening_energy': 'low',
            'energy_drains': ['long_meetings', 'email_processing'],
            'energy_boosters': ['creative_work', 'problem_solving']
        }
    
    def _create_test_challenges(self) -> List[Dict[str, Any]]:
        """Create test user-reported challenges"""
        return [
            {
                'challenge': 'Difficulty focusing in open office',
                'frequency': 'daily',
                'severity': 'moderate',
                'user_reported': True
            },
            {
                'challenge': 'Procrastination on complex projects',
                'frequency': 'weekly',
                'severity': 'high',
                'user_reported': True
            }
        ]


class TestProfessionalBoundariesAndScope(TestSelfDiscoveryGuide):
    """Test professional boundaries and scope limitations"""
    
    def test_no_psychological_diagnosis_or_assessment(self):
        """Test that system never makes psychological diagnoses"""
        session = self.guide.start_discovery_session('productivity_obstacles')
        
        # Check that no diagnostic language is used
        session_text = str(session)
        forbidden_diagnostic_terms = [
            'diagnose', 'disorder', 'syndrome', 'condition', 'pathology',
            'dysfunction', 'abnormal', 'symptoms', 'treatment', 'therapy',
            'depression', 'anxiety', 'adhd', 'add', 'ocd'
        ]
        
        for term in forbidden_diagnostic_terms:
            self.assertNotIn(term.lower(), session_text.lower(),
                           f"System should not use diagnostic language: '{term}'")
    
    def test_clear_scope_limitations_communicated(self):
        """Test that scope limitations are clearly communicated"""
        session = self.guide.start_discovery_session('motivation_understanding')
        
        self.assertIn('scope_limitations', session)
        limitations = session['scope_limitations']
        
        # Should explicitly state what the system cannot do
        self.assertIn('cannot_provide', limitations)
        cannot_provide = limitations['cannot_provide']
        
        expected_limitations = [
            'psychological_diagnosis',
            'mental_health_treatment',
            'therapeutic_intervention',
            'medical_advice'
        ]
        
        for limitation in expected_limitations:
            self.assertIn(limitation, cannot_provide)
    
    def test_professional_referral_guidelines_included(self):
        """Test that professional referral guidelines are included"""
        referral_info = self.guide.get_professional_referral_information()
        
        self.assertIn('when_to_seek_help', referral_info)
        self.assertIn('types_of_professionals', referral_info)
        self.assertIn('how_to_find_help', referral_info)
        
        # Should include specific indicators for professional help
        when_to_seek = referral_info['when_to_seek_help']
        self.assertIn('persistent_challenges', when_to_seek)
        self.assertIn('emotional_distress', when_to_seek)
        self.assertIn('life_interference', when_to_seek)
    
    def test_crisis_detection_protocols_present(self):
        """Test that crisis detection protocols are in place"""
        # Simulate concerning user input
        concerning_input = "I feel completely overwhelmed and can't see any way forward"
        
        assessment = self.guide.assess_professional_referral_needs(concerning_input)
        
        self.assertIn('urgency_level', assessment)
        self.assertIn('recommended_action', assessment)
        self.assertIn('resources', assessment)
        
        # Should recommend professional help for concerning input
        if assessment['urgency_level'] in ['moderate', 'high']:
            self.assertIn('professional_support_recommended', assessment['recommended_action'])
    
    def test_licensed_professional_requirements_acknowledged(self):
        """Test that requirements for licensed professionals are acknowledged"""
        session = self.guide.start_discovery_session('goal_clarity')
        
        self.assertIn('professional_support_note', session)
        note = session['professional_support_note']
        
        # Should acknowledge licensed professional requirements
        note_text = note.lower()
        self.assertIn('licensed', note_text)
        self.assertIn('qualified', note_text)
        self.assertIn('professional', note_text)


class TestUserControlledSelfReflection(TestSelfDiscoveryGuide):
    """Test user-controlled self-reflection and discovery"""
    
    def test_reflection_prompts_are_open_ended_and_non_leading(self):
        """Test that reflection prompts are open-ended and don't lead users"""
        prompts = self.guide.generate_reflection_prompts('productivity_patterns')
        
        for prompt in prompts:
            question = prompt['question']
            
            # Should be open-ended (not yes/no questions)
            self.assertFalse(question.lower().startswith('do you'))
            self.assertFalse(question.lower().startswith('are you'))
            self.assertFalse(question.lower().startswith('can you'))
            
            # Should not be leading or suggestive
            leading_phrases = [
                'you should consider',
                'it might be because',
                'this suggests that',
                'you probably',
                'clearly you'
            ]
            
            for phrase in leading_phrases:
                self.assertNotIn(phrase.lower(), question.lower(),
                               f"Question should not be leading: '{question}'")
            
            # Should encourage self-discovery
            discovery_words = ['what', 'how', 'when', 'where', 'why', 'which']
            starts_with_discovery = any(question.lower().startswith(word) 
                                      for word in discovery_words)
            self.assertTrue(starts_with_discovery,
                          f"Question should encourage discovery: '{question}'")
    
    def test_users_control_all_interpretations_and_insights(self):
        """Test that users control all interpretations and insights"""
        session = self.guide.start_discovery_session('energy_awareness')
        
        # System should provide data and questions, not interpretations
        self.assertIn('observations_for_reflection', session)
        self.assertIn('guided_questions', session)
        self.assertNotIn('interpretations', session)
        self.assertNotIn('conclusions', session)
        self.assertNotIn('analysis_results', session)
        
        # User should record their own insights
        user_insight = "I notice I'm most creative in the morning when I'm well-rested"
        
        result = self.guide.record_user_insight(
            session_id=session['session_id'],
            insight=user_insight,
            category='energy_awareness',
            confidence_level='high'
        )
        
        self.assertEqual(result['status'], 'recorded')
        self.assertTrue(result['user_controlled'])
        
        # Verify insight is attributed to user
        recorded_insights = self.guide.get_user_insights()
        matching_insights = [i for i in recorded_insights if i['insight'] == user_insight]
        
        self.assertEqual(len(matching_insights), 1)
        recorded = matching_insights[0]
        self.assertEqual(recorded['source'], 'user_self_discovery')
        self.assertTrue(recorded['user_interpretation'])
    
    def test_discovery_sessions_support_personal_exploration(self):
        """Test that discovery sessions support personal exploration"""
        session = self.guide.start_discovery_session('values_alignment')
        
        self.assertIn('exploration_areas', session)
        self.assertIn('personal_reflection_space', session)
        self.assertIn('self_paced', session)
        
        # Should allow users to explore at their own pace
        self.assertTrue(session['self_paced'])
        self.assertIn('no_time_pressure', session)
        
        # Should provide space for personal notes
        personal_space = session['personal_reflection_space']
        self.assertTrue(personal_space['private_to_user'])
        self.assertTrue(personal_space['user_controlled'])
    
    def test_users_can_customize_discovery_focus_areas(self):
        """Test that users can customize their discovery focus areas"""
        # User defines custom focus areas
        custom_areas = [
            'work_life_integration',
            'creative_productivity',
            'team_collaboration_preferences'
        ]
        
        result = self.guide.set_user_discovery_preferences(
            focus_areas=custom_areas,
            depth_level='detailed',
            session_frequency='weekly'
        )
        
        self.assertEqual(result['status'], 'preferences_set')
        
        # Discovery sessions should reflect user preferences
        session = self.guide.start_discovery_session('user_defined')
        
        self.assertIn('custom_focus_areas', session)
        session_areas = session['custom_focus_areas']
        
        for area in custom_areas:
            self.assertIn(area, session_areas)


class TestEthicalSafeguardsAndTransparency(TestSelfDiscoveryGuide):
    """Test ethical safeguards and transparency"""
    
    def test_user_data_privacy_and_control(self):
        """Test that user data privacy and control are maintained"""
        session = self.guide.start_discovery_session('obstacle_recognition')
        
        # Check privacy controls
        self.assertIn('privacy_controls', session)
        privacy = session['privacy_controls']
        
        self.assertTrue(privacy['user_owns_all_data'])
        self.assertTrue(privacy['can_delete_anytime'])
        self.assertTrue(privacy['not_shared_without_permission'])
        
        # Test data deletion
        session_id = session['session_id']
        delete_result = self.guide.delete_discovery_session(session_id, user_confirmed=True)
        
        self.assertEqual(delete_result['status'], 'deleted')
        self.assertTrue(delete_result['user_confirmed'])
    
    def test_no_hidden_analysis_or_interpretation(self):
        """Test that there is no hidden analysis or interpretation"""
        session = self.guide.start_discovery_session('productivity_patterns')
        
        # All analysis should be transparent
        self.assertIn('data_sources', session)
        self.assertIn('methodology_explanation', session)
        
        # Should not perform hidden psychological analysis
        self.assertNotIn('psychological_profile', session)
        self.assertNotIn('personality_assessment', session)
        self.assertNotIn('behavioral_analysis', session)
        
        # Any data processing should be explained
        methodology = session['methodology_explanation']
        self.assertIn('how_data_is_used', methodology)
        self.assertIn('no_hidden_analysis', methodology)
    
    def test_transparent_limitations_about_self_discovery_accuracy(self):
        """Test transparent limitations about self-discovery accuracy"""
        session = self.guide.start_discovery_session('motivation_understanding')
        
        self.assertIn('process_limitations', session)
        limitations = session['process_limitations']
        
        expected_limitations = [
            'self_reflection_biases',
            'individual_variation',
            'context_dependency',
            'temporal_changes'
        ]
        
        for limitation in expected_limitations:
            self.assertIn(limitation, limitations)
        
        # Should acknowledge that self-discovery is ongoing process
        self.assertIn('ongoing_process_note', session)
        note = session['ongoing_process_note']
        self.assertIn('evolving', note.lower())
        self.assertIn('journey', note.lower())
    
    def test_user_consent_for_all_discovery_activities(self):
        """Test that user consent is required for all discovery activities"""
        # Starting any session should require explicit consent
        consent_info = self.guide.get_discovery_consent_information()
        
        self.assertIn('what_happens_in_discovery', consent_info)
        self.assertIn('user_control_assurance', consent_info)
        self.assertIn('data_usage_explanation', consent_info)
        self.assertIn('right_to_withdraw', consent_info)
        
        # User must provide informed consent
        consent_result = self.guide.provide_informed_consent(
            understands_process=True,
            agrees_to_participate=True,
            acknowledges_limitations=True
        )
        
        self.assertEqual(consent_result['status'], 'consent_provided')
        self.assertTrue(consent_result['informed_consent_given'])


class TestProfessionalReferralProtocols(TestSelfDiscoveryGuide):
    """Test professional referral protocols and assessments"""
    
    def test_referral_assessment_detects_complexity_beyond_scope(self):
        """Test that referral assessment detects complexity beyond scope"""
        complex_situations = [
            "I've been struggling with productivity for months and it's affecting my relationships",
            "I can't seem to focus on anything and it's making me feel hopeless",
            "My work patterns have completely changed since a major life event"
        ]
        
        for situation in complex_situations:
            assessment = self.guide.assess_professional_referral_needs(situation)
            
            self.assertIn('complexity_assessment', assessment)
            complexity = assessment['complexity_assessment']
            
            # Should identify when professional help is appropriate
            if complexity['level'] in ['moderate', 'high']:
                self.assertIn('professional_support_recommended', 
                            assessment['recommended_action'])
    
    def test_referral_resources_are_comprehensive_and_helpful(self):
        """Test that referral resources are comprehensive and helpful"""
        resources = self.guide.get_professional_referral_resources()
        
        self.assertIn('types_of_help', resources)
        self.assertIn('how_to_find_professionals', resources)
        self.assertIn('what_to_expect', resources)
        self.assertIn('cost_and_insurance_info', resources)
        
        # Should include different types of professional help
        types = resources['types_of_help']
        expected_types = [
            'licensed_therapist',
            'productivity_coach',
            'career_counselor',
            'adhd_specialist'
        ]
        
        for help_type in expected_types:
            self.assertIn(help_type, types)
    
    def test_crisis_support_information_is_readily_available(self):
        """Test that crisis support information is readily available"""
        crisis_info = self.guide.get_crisis_support_information()
        
        self.assertIn('immediate_help_available', crisis_info)
        self.assertIn('crisis_hotlines', crisis_info)
        self.assertIn('emergency_contacts', crisis_info)
        
        # Should provide immediate access to crisis resources
        immediate_help = crisis_info['immediate_help_available']
        self.assertTrue(immediate_help['24_7_access'])
        self.assertIn('hotline_numbers', immediate_help)
    
    def test_referral_suggestions_are_not_diagnostic(self):
        """Test that referral suggestions are not diagnostic"""
        user_input = "I have trouble concentrating and staying organized"
        
        assessment = self.guide.assess_professional_referral_needs(user_input)
        
        # Should suggest professional consultation without diagnosing
        self.assertNotIn('likely_condition', assessment)
        self.assertNotIn('probable_diagnosis', assessment)
        self.assertNotIn('symptoms_suggest', assessment)
        
        # Should frame as general support, not specific treatment
        if 'recommended_action' in assessment:
            action_text = str(assessment['recommended_action']).lower()
            self.assertIn('explore with professional', action_text)
            self.assertNotIn('treatment for', action_text)


class TestDiscoverySessionTypes(TestSelfDiscoveryGuide):
    """Test different types of discovery sessions"""
    
    def test_productivity_pattern_discovery_session(self):
        """Test productivity pattern discovery session"""
        session = self.guide.start_discovery_session('productivity_patterns')
        
        self.assertIn('pattern_observations', session)
        self.assertIn('reflection_questions', session)
        self.assertIn('exploration_exercises', session)
        
        # Should include questions about personal patterns
        questions = session['reflection_questions']
        question_text = str(questions).lower()
        self.assertIn('when', question_text)
        self.assertIn('productive', question_text)
        
        # Should not provide pattern interpretations
        self.assertNotIn('pattern_conclusions', session)
        self.assertNotIn('productivity_diagnosis', session)
    
    def test_energy_awareness_discovery_session(self):
        """Test energy awareness discovery session"""
        session = self.guide.start_discovery_session('energy_awareness')
        
        self.assertIn('energy_reflection_prompts', session)
        self.assertIn('energy_tracking_suggestions', session)
        
        # Should encourage personal energy awareness
        prompts = session['energy_reflection_prompts']
        self.assertGreater(len(prompts), 0)
        
        for prompt in prompts:
            self.assertIn('question', prompt)
            self.assertTrue(prompt['user_reflection_required'])
    
    def test_goal_clarity_discovery_session(self):
        """Test goal clarity discovery session"""
        session = self.guide.start_discovery_session('goal_clarity')
        
        self.assertIn('values_exploration', session)
        self.assertIn('goal_reflection_process', session)
        self.assertIn('alignment_questions', session)
        
        # Should help users explore their own goals and values
        values_exploration = session['values_exploration']
        self.assertTrue(values_exploration['user_guided'])
        self.assertFalse(values_exploration.get('prescriptive', True))
    
    def test_obstacle_recognition_discovery_session(self):
        """Test obstacle recognition discovery session"""
        session = self.guide.start_discovery_session('obstacle_recognition')
        
        self.assertIn('obstacle_categories', session)
        self.assertIn('distinction_questions', session)
        
        # Should help distinguish individual vs systemic obstacles
        categories = session['obstacle_categories']
        self.assertIn('individual_factors', categories)
        self.assertIn('systemic_factors', categories)
        self.assertIn('environmental_factors', categories)
        
        # Should include questions to help users categorize obstacles
        distinction_questions = session['distinction_questions']
        self.assertGreater(len(distinction_questions), 0)


class TestUserInsightRecordingAndTracking(TestSelfDiscoveryGuide):
    """Test user insight recording and tracking"""
    
    def test_user_insights_are_properly_attributed_and_stored(self):
        """Test that user insights are properly attributed and stored"""
        insight_text = "I work best in short bursts with frequent breaks"
        category = "work_style_preferences"
        
        result = self.guide.record_user_insight(
            insight=insight_text,
            category=category,
            confidence_level="moderate",
            supporting_observations=["energy_patterns", "focus_data"]
        )
        
        self.assertEqual(result['status'], 'recorded')
        
        # Retrieve and verify insight
        insights = self.guide.get_user_insights(category=category)
        matching_insights = [i for i in insights if i['insight'] == insight_text]
        
        self.assertEqual(len(matching_insights), 1)
        recorded_insight = matching_insights[0]
        
        self.assertEqual(recorded_insight['source'], 'user_self_discovery')
        self.assertEqual(recorded_insight['category'], category)
        self.assertTrue(recorded_insight['user_controlled'])
        self.assertIn('recorded_date', recorded_insight)
    
    def test_users_can_update_and_modify_their_insights(self):
        """Test that users can update and modify their insights"""
        # Record initial insight
        initial_insight = "I think I'm more productive in the afternoon"
        
        result = self.guide.record_user_insight(
            insight=initial_insight,
            category="timing_preferences"
        )
        
        insight_id = result['insight_id']
        
        # Update the insight
        updated_insight = "Actually, I'm most productive in the morning after coffee"
        
        update_result = self.guide.update_user_insight(
            insight_id=insight_id,
            updated_insight=updated_insight,
            reason_for_update="Discovered through more careful observation"
        )
        
        self.assertEqual(update_result['status'], 'updated')
        
        # Verify update was recorded with history
        insight_history = self.guide.get_insight_history(insight_id)
        self.assertEqual(len(insight_history), 2)  # Original + update
        self.assertEqual(insight_history[-1]['insight'], updated_insight)
    
    def test_insight_connections_and_patterns_user_controlled(self):
        """Test that insight connections and patterns are user-controlled"""
        # Record related insights
        insights = [
            "I focus better with background music",
            "Open offices are distracting for me",
            "I need quiet space for complex thinking"
        ]
        
        insight_ids = []
        for insight in insights:
            result = self.guide.record_user_insight(insight, "environment_preferences")
            insight_ids.append(result['insight_id'])
        
        # User identifies connections between insights
        connection_result = self.guide.connect_user_insights(
            insight_ids=insight_ids,
            connection_description="All relate to my need for auditory control",
            user_identified=True
        )
        
        self.assertEqual(connection_result['status'], 'connection_recorded')
        self.assertTrue(connection_result['user_identified'])
        
        # Verify connection is stored as user-identified
        connections = self.guide.get_insight_connections()
        matching_connections = [c for c in connections 
                              if set(c['insight_ids']) == set(insight_ids)]
        
        self.assertEqual(len(matching_connections), 1)
        connection = matching_connections[0]
        self.assertTrue(connection['user_identified'])
        self.assertFalse(connection.get('ai_suggested', True))


class TestIntegrationWithOtherModules(TestSelfDiscoveryGuide):
    """Test integration with other FlowState modules"""
    
    def test_receives_pattern_data_for_user_reflection(self):
        """Test that guide receives pattern data for user reflection"""
        # Mock pattern data from PatternAnalyzer
        pattern_data = {
            'time_patterns': {
                'peak_hours': [9, 10, 11],
                'low_energy_periods': [14, 15]
            },
            'energy_correlations': {
                'morning_high_energy': 0.7,
                'afternoon_energy_drop': 0.6
            },
            'limitations': 'Based on 30 days of data'
        }
        
        self.guide.receive_pattern_data_for_reflection(pattern_data)
        
        # Should incorporate data into discovery sessions
        session = self.guide.start_discovery_session('productivity_patterns')
        
        self.assertIn('available_pattern_data', session)
        available_data = session['available_pattern_data']
        
        self.assertIn('time_patterns', available_data)
        self.assertIn('data_limitations', available_data)
        
        # Should still require user interpretation
        self.assertTrue(session['user_interpretation_required'])
    
    def test_provides_insights_to_ai_tracker_with_user_permission(self):
        """Test that guide provides insights to AI tracker with user permission"""
        # User records insights
        user_insights = [
            "I work best in 25-minute focused sessions",
            "Background music helps my concentration",
            "I need breaks every 90 minutes"
        ]
        
        for insight in user_insights:
            self.guide.record_user_insight(insight, "work_preferences")
        
        # User gives permission to share insights with AI tracker
        permission_result = self.guide.set_insight_sharing_permission(
            module='ai_tracker',
            permission_granted=True,
            specific_categories=['work_preferences']
        )
        
        self.assertEqual(permission_result['status'], 'permission_set')
        
        # Get insights for AI tracker
        shared_insights = self.guide.get_insights_for_ai_tracker()
        
        self.assertIn('user_insights', shared_insights)
        self.assertIn('sharing_permissions', shared_insights)
        self.assertTrue(shared_insights['user_controlled'])
        
        # Should only include permitted categories
        insights_list = shared_insights['user_insights']
        for insight in insights_list:
            self.assertIn(insight['category'], ['work_preferences'])
    
    def test_integrates_with_user_profile_preferences(self):
        """Test integration with user profile preferences"""
        mock_user_profile = {
            'accessibility_prefs': {
                'simplified_interface': True,
                'extended_processing_time': True
            },
            'psychology_prefs': {
                'reflection_depth': 'moderate',
                'session_frequency': 'weekly'
            }
        }
        
        # Initialize guide with user profile
        profile_guide = SelfDiscoveryGuide(user_profile=mock_user_profile)
        
        session = profile_guide.start_discovery_session('energy_awareness')
        
        # Should respect accessibility preferences
        self.assertTrue(session.get('simplified_presentation', False))
        self.assertTrue(session.get('extended_time_allowance', False))
        
        # Should respect psychology preferences
        self.assertEqual(session.get('reflection_depth'), 'moderate')


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestProfessionalBoundariesAndScope,
        TestUserControlledSelfReflection,
        TestEthicalSafeguardsAndTransparency,
        TestProfessionalReferralProtocols,
        TestDiscoverySessionTypes,
        TestUserInsightRecordingAndTracking,
        TestIntegrationWithOtherModules
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*65}")
    print(f"FlowState SelfDiscoveryGuide Test Summary")
    print(f"{'='*65}")
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

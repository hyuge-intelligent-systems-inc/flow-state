
"""
FlowState Team Optimizer Tests
Comprehensive testing for privacy-preserving team collaboration
Based on expert analysis emphasizing trust-building and collaboration without surveillance
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
from team.team_optimizer import TeamOptimizer
from core.user_profile import UserProfile

class TestPrivacyPreservingCollaboration(unittest.TestCase):
    """Test that team features preserve individual privacy while enabling collaboration"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(5)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
        
        # Set up test team with various privacy preferences
        for i, profile in enumerate(self.user_profiles):
            privacy_level = ['private', 'anonymous', 'aggregated', 'team_visible', 'full_collaboration'][i]
            profile.set_preference('team_privacy_level', privacy_level)
    
    def test_respects_individual_privacy_levels(self):
        """Test that team insights respect each member's privacy preferences"""
        team_insights = self.team_optimizer.generate_team_insights()
        
        # Private users should not appear in any team data
        private_users = [p for p in self.user_profiles if p.get_preference('team_privacy_level') == 'private']
        
        for insight in team_insights['insights']:
            for private_user in private_users:
                self.assertNotIn(private_user.user_id, str(insight))
    
    def test_aggregated_data_prevents_individual_identification(self):
        """Test that aggregated team data cannot identify individuals"""
        aggregated_data = self.team_optimizer.get_aggregated_team_patterns()
        
        # Should contain team-level patterns but no individual identifiers
        self.assertIn('team_productivity_patterns', aggregated_data)
        self.assertIn('optimal_collaboration_times', aggregated_data)
        
        # Should not contain individual user data
        for user_profile in self.user_profiles:
            self.assertNotIn(user_profile.user_id, str(aggregated_data))
    
    def test_user_can_opt_out_of_team_features(self):
        """Test that users can completely opt out of team optimization"""
        opt_out_user = self.user_profiles[0]
        opt_out_user.set_preference('team_participation', False)
        
        team_data = self.team_optimizer.get_team_participation_status()
        
        self.assertFalse(team_data['users'][opt_out_user.user_id]['participating'])
        self.assertTrue(team_data['users'][opt_out_user.user_id]['can_rejoin_anytime'])
    
    def test_granular_sharing_controls(self):
        """Test detailed controls over what team data is shared"""
        user = self.user_profiles[0]
        sharing_preferences = {
            'productivity_patterns': True,
            'focus_times': True,
            'availability': False,
            'task_categories': False,
            'energy_levels': True
        }
        
        user.set_team_sharing_preferences(sharing_preferences)
        
        shared_data = self.team_optimizer.get_user_shared_data(user.user_id)
        
        # Should only include data user explicitly agreed to share
        self.assertIn('productivity_patterns', shared_data)
        self.assertIn('focus_times', shared_data)
        self.assertNotIn('availability', shared_data)
        self.assertNotIn('task_categories', shared_data)

class TestTrustBuildingFeatures(unittest.TestCase):
    """Test features that build team trust rather than surveillance"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(3)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
    
    def test_mutual_benefit_focus(self):
        """Test that team optimization focuses on mutual benefit, not individual monitoring"""
        team_suggestions = self.team_optimizer.generate_team_suggestions()
        
        for suggestion in team_suggestions['suggestions']:
            # Should focus on team benefits
            self.assertIn('team_benefit', suggestion)
            self.assertIn('individual_benefit', suggestion)
            
            # Should not include monitoring or surveillance language
            suggestion_text = suggestion['description'].lower()
            surveillance_words = ['monitor', 'track', 'watch', 'surveillance', 'control']
            
            for word in surveillance_words:
                self.assertNotIn(word, suggestion_text)
    
    def test_transparency_in_team_insights(self):
        """Test that team insights are transparent about data sources and limitations"""
        insights = self.team_optimizer.generate_team_insights()
        
        for insight in insights['insights']:
            self.assertIn('data_sources', insight)
            self.assertIn('confidence_level', insight)
            self.assertIn('limitations', insight)
            self.assertIn('participating_users_count', insight)
    
    def test_no_individual_performance_comparison(self):
        """Test that system doesn't create individual performance comparisons"""
        team_metrics = self.team_optimizer.get_team_metrics()
        
        # Should have team-level metrics but no individual rankings
        self.assertIn('team_collaboration_score', team_metrics)
        self.assertIn('team_productivity_trends', team_metrics)
        
        # Should not have individual comparisons
        self.assertNotIn('individual_rankings', team_metrics)
        self.assertNotIn('performance_comparisons', team_metrics)
        self.assertNotIn('productivity_leaderboard', team_metrics)
    
    def test_voluntary_accountability_systems(self):
        """Test that accountability features are voluntary and supportive"""
        accountability_options = self.team_optimizer.get_accountability_options()
        
        # All accountability should be opt-in
        for option in accountability_options['options']:
            self.assertTrue(option['voluntary'])
            self.assertTrue(option['user_controlled'])
            self.assertIn('exit_strategy', option)

class TestCollaborationWithoutSurveillance(unittest.TestCase):
    """Test collaborative features that don't create surveillance dynamics"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(4)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
    
    def test_focus_time_coordination(self):
        """Test coordinating team focus time without monitoring individual work"""
        focus_coordination = self.team_optimizer.coordinate_team_focus_time()
        
        # Should suggest optimal team focus times
        self.assertIn('suggested_team_focus_blocks', focus_coordination)
        self.assertIn('individual_preferences_respected', focus_coordination)
        
        # Should not monitor what individuals do during focus time
        self.assertNotIn('individual_focus_monitoring', focus_coordination)
        self.assertNotIn('productivity_measurement_during_focus', focus_coordination)
    
    def test_meeting_optimization_suggestions(self):
        """Test meeting optimization that improves team effectiveness"""
        meeting_insights = self.team_optimizer.analyze_meeting_patterns()
        
        # Should provide team-level meeting insights
        self.assertIn('optimal_meeting_times', meeting_insights)
        self.assertIn('meeting_frequency_recommendations', meeting_insights)
        
        # Should respect individual privacy about meeting content
        self.assertNotIn('individual_meeting_performance', meeting_insights)
        self.assertNotIn('meeting_content_analysis', meeting_insights)
    
    def test_knowledge_sharing_facilitation(self):
        """Test features that facilitate knowledge sharing without pressure"""
        knowledge_sharing = self.team_optimizer.facilitate_knowledge_sharing()
        
        # Should create opportunities, not requirements
        self.assertIn('optional_sharing_opportunities', knowledge_sharing)
        self.assertIn('expertise_matching_suggestions', knowledge_sharing)
        
        # Should not create pressure or tracking
        self.assertNotIn('sharing_requirements', knowledge_sharing)
        self.assertNotIn('knowledge_sharing_tracking', knowledge_sharing)

class TestAntiGamingProtections(unittest.TestCase):
    """Test protections against gaming team metrics"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(3)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
    
    def test_outcome_based_metrics(self):
        """Test that team metrics focus on outcomes rather than activities"""
        team_metrics = self.team_optimizer.get_team_effectiveness_metrics()
        
        # Should include outcome-based measures
        outcome_metrics = ['project_completion_rate', 'goal_achievement', 'team_satisfaction']
        for metric in outcome_metrics:
            self.assertIn(metric, team_metrics)
        
        # Should avoid easily gamed activity metrics
        activity_metrics = ['hours_logged', 'app_usage_time', 'task_count']
        for metric in activity_metrics:
            self.assertNotIn(metric, team_metrics)
    
    def test_multiple_validation_sources(self):
        """Test that team insights use multiple data sources for validation"""
        insight_validation = self.team_optimizer.validate_team_insights()
        
        for insight in insight_validation['insights']:
            # Should require multiple independent sources
            self.assertGreaterEqual(len(insight['data_sources']), 2)
            self.assertIn('cross_validation_score', insight)
    
    def test_gaming_detection_systems(self):
        """Test detection of unusual patterns that might indicate gaming"""
        gaming_check = self.team_optimizer.detect_unusual_patterns()
        
        self.assertIn('pattern_anomaly_detection', gaming_check)
        self.assertIn('consistency_validation', gaming_check)
        self.assertIn('cross_user_correlation_check', gaming_check)

class TestTeamHealthIndicators(unittest.TestCase):
    """Test indicators of team health and psychological safety"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(5)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
    
    def test_psychological_safety_indicators(self):
        """Test metrics that indicate team psychological safety"""
        safety_indicators = self.team_optimizer.get_psychological_safety_indicators()
        
        expected_indicators = [
            'participation_equality',
            'knowledge_sharing_frequency',
            'question_asking_comfort',
            'mistake_discussion_openness',
            'diverse_perspective_inclusion'
        ]
        
        for indicator in expected_indicators:
            self.assertIn(indicator, safety_indicators)
    
    def test_collaboration_quality_metrics(self):
        """Test metrics that measure collaboration quality"""
        collaboration_metrics = self.team_optimizer.get_collaboration_quality()
        
        # Should measure team dynamics, not individual performance
        self.assertIn('communication_effectiveness', collaboration_metrics)
        self.assertIn('decision_making_speed', collaboration_metrics)
        self.assertIn('conflict_resolution_efficiency', collaboration_metrics)
    
    def test_burnout_prevention_indicators(self):
        """Test early warning indicators for team burnout"""
        burnout_indicators = self.team_optimizer.get_burnout_prevention_insights()
        
        # Should identify team-level risk factors
        self.assertIn('workload_distribution_balance', burnout_indicators)
        self.assertIn('sustainable_pace_indicators', burnout_indicators)
        self.assertIn('recovery_time_adequacy', burnout_indicators)

class TestTeamLearningAndDevelopment(unittest.TestCase):
    """Test features that support team learning and skill development"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(4)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
    
    def test_skill_gap_identification(self):
        """Test identification of team skill gaps and development opportunities"""
        skill_analysis = self.team_optimizer.analyze_team_skills()
        
        # Should identify team needs without individual assessment
        self.assertIn('team_skill_gaps', skill_analysis)
        self.assertIn('development_opportunities', skill_analysis)
        
        # Should not include individual skill assessments
        self.assertNotIn('individual_skill_levels', skill_analysis)
        self.assertNotIn('individual_development_needs', skill_analysis)
    
    def test_mentorship_opportunity_matching(self):
        """Test features that facilitate peer mentorship"""
        mentorship_matching = self.team_optimizer.suggest_mentorship_opportunities()
        
        # Should suggest mutual learning opportunities
        self.assertIn('peer_learning_suggestions', mentorship_matching)
        self.assertIn('expertise_sharing_opportunities', mentorship_matching)
        
        # Should be completely voluntary
        for opportunity in mentorship_matching.get('opportunities', []):
            self.assertTrue(opportunity['voluntary'])
            self.assertIn('both_parties_benefit', opportunity)
    
    def test_team_learning_experiments(self):
        """Test support for team productivity experiments"""
        experiment_suggestions = self.team_optimizer.suggest_team_experiments()
        
        # Should suggest testable team improvements
        for experiment in experiment_suggestions['experiments']:
            self.assertIn('hypothesis', experiment)
            self.assertIn('measurement_approach', experiment)
            self.assertIn('rollback_plan', experiment)
            self.assertTrue(experiment['team_decides'])

class TestCrisisAndSupportDetection(unittest.TestCase):
    """Test features that identify when teams need additional support"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(3)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
    
    def test_team_dysfunction_early_warning(self):
        """Test early detection of team dysfunction patterns"""
        dysfunction_indicators = self.team_optimizer.detect_team_dysfunction_risk()
        
        warning_signs = [
            'communication_breakdown_indicators',
            'conflict_escalation_patterns',
            'participation_inequality_trends',
            'decision_making_delays'
        ]
        
        for sign in warning_signs:
            self.assertIn(sign, dysfunction_indicators)
    
    def test_external_support_recommendations(self):
        """Test recommendations for when teams need external help"""
        support_assessment = self.team_optimizer.assess_external_support_needs()
        
        # Should suggest appropriate professional support
        self.assertIn('team_coaching_recommendations', support_assessment)
        self.assertIn('facilitation_suggestions', support_assessment)
        self.assertIn('training_opportunities', support_assessment)
    
    def test_escalation_protocols(self):
        """Test protocols for escalating serious team issues"""
        escalation_check = self.team_optimizer.check_escalation_needs()
        
        if escalation_check['escalation_needed']:
            self.assertIn('recommended_actions', escalation_check)
            self.assertIn('confidentiality_preserved', escalation_check)
            self.assertIn('support_resources', escalation_check)

class TestIntegrationWithOtherModules(unittest.TestCase):
    """Test team optimizer integration with other FlowState modules"""
    
    def setUp(self):
        self.user_profiles = [UserProfile(f"user_{i}") for i in range(3)]
        self.team_optimizer = TeamOptimizer(self.user_profiles)
    
    def test_respects_individual_module_privacy_settings(self):
        """Test that team features respect individual module privacy preferences"""
        user = self.user_profiles[0]
        user.set_privacy_level('time_tracking', 'private')
        user.set_privacy_level('pattern_analysis', 'team_visible')
        
        team_data_request = self.team_optimizer.request_user_data_for_team_insights(user.user_id)
        
        # Should only access data user has made team-visible
        self.assertNotIn('time_tracking_data', team_data_request['available_data'])
        self.assertIn('pattern_analysis_data', team_data_request['available_data'])
    
    def test_enhances_individual_modules_without_replacement(self):
        """Test that team features enhance rather than replace individual modules"""
        enhancement_check = self.team_optimizer.get_individual_module_enhancement()
        
        # Should provide team context to individual modules
        self.assertIn('team_context_for_time_tracking', enhancement_check)
        self.assertIn('team_context_for_pattern_analysis', enhancement_check)
        
        # Should not replace individual functionality
        self.assertNotIn('replaces_individual_tracking', enhancement_check)
        self.assertNotIn('overrides_personal_insights', enhancement_check)

# Test Suite Runner
def run_team_optimizer_tests():
    """Run all Team Optimizer tests with detailed reporting"""
    test_classes = [
        TestPrivacyPreservingCollaboration,
        TestTrustBuildingFeatures,
        TestCollaborationWithoutSurveillance,
        TestAntiGamingProtections,
        TestTeamHealthIndicators,
        TestTeamLearningAndDevelopment,
        TestCrisisAndSupportDetection,
        TestIntegrationWithOtherModules
    ]
    
    total_tests = 0
    total_failures = 0
    
    print("FlowState Team Optimizer Test Suite")
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
        print("🎉 All Team Optimizer tests passed! Team features maintain privacy and build trust.")
    else:
        print(f"⚠️  {total_failures} tests failed. Review team implementation for privacy and trust issues.")

if __name__ == "__main__":
    run_team_optimizer_tests()

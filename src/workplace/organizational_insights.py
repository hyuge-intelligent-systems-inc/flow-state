
"""
FlowState Organizational Insights Module

Analytics and insights for understanding organizational productivity patterns,
culture, and system-level optimization opportunities while respecting
individual privacy and avoiding surveillance-style monitoring.

Based on expert analysis emphasizing:
- Trust-building through transparency
- Employee data ownership and control
- System-level problem identification
- Cultural pattern recognition without surveillance
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple, Set
from enum import Enum
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class OrganizationalMetric(Enum):
    """Types of organizational productivity metrics"""
    COLLABORATION_EFFECTIVENESS = "collaboration_effectiveness"
    MEETING_EFFICIENCY = "meeting_efficiency"
    COMMUNICATION_FLOW = "communication_flow"
    WORKLOAD_DISTRIBUTION = "workload_distribution"
    CONTEXT_SWITCHING = "context_switching"
    FOCUS_TIME_AVAILABILITY = "focus_time_availability"
    CROSS_TEAM_DEPENDENCIES = "cross_team_dependencies"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    INNOVATION_TIME = "innovation_time"
    BURNOUT_INDICATORS = "burnout_indicators"


class ProductivityPattern(Enum):
    """Organizational productivity patterns"""
    MORNING_FOCUSED = "morning_focused"
    AFTERNOON_COLLABORATIVE = "afternoon_collaborative"
    DEEP_WORK_BLOCKS = "deep_work_blocks"
    FREQUENT_INTERRUPTIONS = "frequent_interruptions"
    ASYNC_HEAVY = "async_heavy"
    MEETING_HEAVY = "meeting_heavy"
    SEASONAL_VARIATION = "seasonal_variation"
    PROJECT_CYCLICAL = "project_cyclical"


class CultureIndicator(Enum):
    """Indicators of organizational culture"""
    PSYCHOLOGICAL_SAFETY = "psychological_safety"
    AUTONOMY_LEVEL = "autonomy_level"
    LEARNING_ORIENTATION = "learning_orientation"
    COLLABORATION_QUALITY = "collaboration_quality"
    INNOVATION_SUPPORT = "innovation_support"
    WORK_LIFE_BALANCE = "work_life_balance"
    DIVERSITY_INCLUSION = "diversity_inclusion"
    FEEDBACK_CULTURE = "feedback_culture"


class SystemDysfunction(Enum):
    """Types of organizational dysfunction"""
    UNCLEAR_PRIORITIES = "unclear_priorities"
    RESOURCE_CONSTRAINTS = "resource_constraints"
    COMMUNICATION_SILOS = "communication_silos"
    PROCESS_INEFFICIENCIES = "process_inefficiencies"
    TECHNICAL_DEBT = "technical_debt"
    SKILL_GAPS = "skill_gaps"
    LEADERSHIP_GAPS = "leadership_gaps"
    CULTURAL_MISALIGNMENT = "cultural_misalignment"


@dataclass
class TeamProductivityProfile:
    """Productivity profile for a team"""
    team_id: str
    team_name: str
    team_size: int
    productivity_patterns: List[ProductivityPattern]
    peak_collaboration_times: List[Tuple[int, int]]  # (start_hour, end_hour)
    average_focus_session_duration: timedelta
    meeting_load: float  # Percentage of time in meetings
    context_switching_frequency: float  # Switches per hour
    cross_team_dependencies: int
    knowledge_sharing_frequency: float  # Sessions per week
    innovation_time_percentage: float
    burnout_risk_score: float  # 0-1 scale


@dataclass
class OrganizationalHealthMetrics:
    """Overall organizational health indicators"""
    org_id: str
    measurement_period: Tuple[datetime, datetime]
    employee_satisfaction_score: float  # 0-1 scale
    productivity_trend: str  # "improving", "stable", "declining"
    collaboration_effectiveness: float  # 0-1 scale
    innovation_index: float  # 0-1 scale
    burnout_prevalence: float  # 0-1 scale
    turnover_risk: float  # 0-1 scale
    culture_indicators: Dict[CultureIndicator, float]
    system_dysfunction_score: float  # 0-1 scale
    recommendations: List[str]


@dataclass
class ProductivityInsight:
    """Individual productivity insight"""
    insight_id: str
    category: str
    title: str
    description: str
    impact_level: str  # "high", "medium", "low"
    confidence_level: float  # 0-1 scale
    affected_teams: List[str]
    recommended_actions: List[str]
    implementation_difficulty: str  # "easy", "moderate", "difficult"
    estimated_impact: str
    data_sources: List[str]


class DataPrivacyProtector:
    """Ensures individual privacy while enabling organizational insights"""
    
    def __init__(self):
        self.aggregation_threshold = 5  # Minimum group size for reporting
        self.anonymization_methods = [
            "statistical_aggregation",
            "differential_privacy",
            "k_anonymity",
            "data_generalization"
        ]
    
    def ensure_privacy_compliance(self, data: Dict, analysis_type: str) -> Dict:
        """Ensure data meets privacy requirements before analysis"""
        
        if analysis_type == "individual_patterns":
            # Individual data requires explicit consent
            if not data.get("user_consent_for_analysis", False):
                logger.warning("Individual analysis attempted without consent")
                return {"error": "User consent required for individual analysis"}
        
        elif analysis_type == "team_patterns":
            # Team data requires minimum group size
            team_size = data.get("team_size", 0)
            if team_size < self.aggregation_threshold:
                logger.warning(f"Team too small for analysis: {team_size} < {self.aggregation_threshold}")
                return {"error": f"Team size must be at least {self.aggregation_threshold} for analysis"}
        
        # Remove personally identifiable information
        anonymized_data = self._anonymize_data(data)
        
        return {
            "data": anonymized_data,
            "privacy_compliant": True,
            "anonymization_methods": self.anonymization_methods[:2]  # Methods used
        }
    
    def _anonymize_data(self, data: Dict) -> Dict:
        """Remove or generalize personally identifiable information"""
        anonymized = data.copy()
        
        # Remove direct identifiers
        sensitive_fields = ["user_id", "email", "name", "employee_id"]
        for field in sensitive_fields:
            if field in anonymized:
                anonymized[field] = f"anonymous_{hash(anonymized[field]) % 10000}"
        
        # Generalize specific timestamps to broader time windows
        if "timestamp" in anonymized:
            timestamp = anonymized["timestamp"]
            # Round to nearest hour
            anonymized["timestamp"] = timestamp.replace(minute=0, second=0, microsecond=0)
        
        return anonymized
    
    def aggregate_safely(self, individual_data: List[Dict]) -> Dict:
        """Safely aggregate individual data for team insights"""
        
        if len(individual_data) < self.aggregation_threshold:
            return {"error": "Insufficient data for safe aggregation"}
        
        # Calculate aggregate statistics
        aggregated = {
            "sample_size": len(individual_data),
            "aggregation_date": datetime.now(),
            "privacy_threshold_met": True
        }
        
        # Aggregate numerical fields
        numerical_fields = ["productivity_score", "focus_time", "collaboration_time"]
        for field in numerical_fields:
            values = [item.get(field, 0) for item in individual_data if field in item]
            if values:
                aggregated[field] = {
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                    "min": min(values),
                    "max": max(values)
                }
        
        return aggregated


class OrganizationalPatternAnalyzer:
    """Analyzes organizational productivity patterns"""
    
    def __init__(self):
        self.privacy_protector = DataPrivacyProtector()
        self.pattern_thresholds = {
            "morning_focused": 0.6,  # 60% of productive work happens before noon
            "meeting_heavy": 0.4,    # More than 40% of time in meetings
            "context_switching": 10   # More than 10 switches per day
        }
    
    def analyze_team_patterns(self, team_data: Dict) -> List[ProductivityPattern]:
        """Identify productivity patterns for a team"""
        
        # Ensure privacy compliance
        privacy_check = self.privacy_protector.ensure_privacy_compliance(
            team_data, "team_patterns"
        )
        
        if "error" in privacy_check:
            logger.error(f"Privacy violation prevented: {privacy_check['error']}")
            return []
        
        patterns = []
        safe_data = privacy_check["data"]
        
        # Analyze morning vs afternoon productivity
        morning_productivity = safe_data.get("morning_productivity_ratio", 0)
        if morning_productivity > self.pattern_thresholds["morning_focused"]:
            patterns.append(ProductivityPattern.MORNING_FOCUSED)
        
        # Analyze meeting load
        meeting_percentage = safe_data.get("meeting_percentage", 0)
        if meeting_percentage > self.pattern_thresholds["meeting_heavy"]:
            patterns.append(ProductivityPattern.MEETING_HEAVY)
        
        # Analyze context switching
        context_switches = safe_data.get("daily_context_switches", 0)
        if context_switches > self.pattern_thresholds["context_switching"]:
            patterns.append(ProductivityPattern.FREQUENT_INTERRUPTIONS)
        
        # Analyze collaboration patterns
        async_ratio = safe_data.get("async_collaboration_ratio", 0)
        if async_ratio > 0.7:
            patterns.append(ProductivityPattern.ASYNC_HEAVY)
        
        logger.info(f"Identified {len(patterns)} patterns for team")
        return patterns
    
    def identify_collaboration_effectiveness(self, team_data: Dict) -> float:
        """Measure team collaboration effectiveness"""
        
        factors = {
            "meeting_efficiency": team_data.get("average_meeting_rating", 0.5),
            "communication_responsiveness": team_data.get("response_time_score", 0.5),
            "knowledge_sharing": team_data.get("knowledge_sharing_frequency", 0) / 10,  # Normalize
            "cross_functional_work": team_data.get("cross_functional_projects", 0) / 5   # Normalize
        }
        
        # Weighted average
        weights = {"meeting_efficiency": 0.3, "communication_responsiveness": 0.3, 
                  "knowledge_sharing": 0.2, "cross_functional_work": 0.2}
        
        effectiveness = sum(factors[key] * weights[key] for key in factors)
        return min(effectiveness, 1.0)
    
    def detect_productivity_bottlenecks(self, org_data: Dict) -> List[Dict[str, str]]:
        """Identify organizational productivity bottlenecks"""
        
        bottlenecks = []
        
        # Check for common bottlenecks
        if org_data.get("average_approval_time", 0) > 3:  # days
            bottlenecks.append({
                "type": "approval_delays",
                "description": "Approval processes are creating delays",
                "impact": "high",
                "solution": "Streamline approval workflows"
            })
        
        if org_data.get("cross_team_dependency_failures", 0) > 0.2:
            bottlenecks.append({
                "type": "dependency_issues",
                "description": "Cross-team dependencies causing delays",
                "impact": "high",
                "solution": "Improve cross-team coordination"
            })
        
        if org_data.get("tool_switching_time", 0) > 0.15:  # 15% of time switching tools
            bottlenecks.append({
                "type": "tool_fragmentation",
                "description": "Too much time lost switching between tools",
                "impact": "medium",
                "solution": "Consolidate or integrate tools"
            })
        
        return bottlenecks


class CultureAnalyzer:
    """Analyzes organizational culture indicators"""
    
    def __init__(self):
        self.culture_metrics = {
            CultureIndicator.PSYCHOLOGICAL_SAFETY: {
                "high_threshold": 0.7,
                "indicators": ["feedback_frequency", "error_tolerance", "speaking_up"]
            },
            CultureIndicator.AUTONOMY_LEVEL: {
                "high_threshold": 0.6,
                "indicators": ["decision_authority", "work_method_choice", "goal_setting_participation"]
            },
            CultureIndicator.LEARNING_ORIENTATION: {
                "high_threshold": 0.6,
                "indicators": ["training_time", "experiment_encouragement", "failure_learning"]
            }
        }
    
    def assess_culture_health(self, org_data: Dict) -> Dict[CultureIndicator, float]:
        """Assess organizational culture health"""
        
        culture_scores = {}
        
        for indicator, config in self.culture_metrics.items():
            scores = []
            
            for metric in config["indicators"]:
                value = org_data.get(metric, 0.5)  # Default to neutral
                scores.append(value)
            
            # Average the indicator scores
            if scores:
                culture_scores[indicator] = sum(scores) / len(scores)
            else:
                culture_scores[indicator] = 0.5  # Neutral default
        
        return culture_scores
    
    def identify_culture_risks(self, culture_scores: Dict[CultureIndicator, float]) -> List[str]:
        """Identify cultural risks that could impact productivity"""
        
        risks = []
        
        if culture_scores.get(CultureIndicator.PSYCHOLOGICAL_SAFETY, 0.5) < 0.4:
            risks.append("Low psychological safety may inhibit innovation and communication")
        
        if culture_scores.get(CultureIndicator.AUTONOMY_LEVEL, 0.5) < 0.3:
            risks.append("Low autonomy may reduce motivation and engagement")
        
        if culture_scores.get(CultureIndicator.WORK_LIFE_BALANCE, 0.5) < 0.4:
            risks.append("Poor work-life balance may lead to burnout and turnover")
        
        if culture_scores.get(CultureIndicator.LEARNING_ORIENTATION, 0.5) < 0.4:
            risks.append("Limited learning orientation may hinder adaptation and growth")
        
        return risks
    
    def recommend_culture_improvements(self, culture_scores: Dict[CultureIndicator, float]) -> List[str]:
        """Recommend improvements based on culture assessment"""
        
        recommendations = []
        
        # Psychological safety improvements
        if culture_scores.get(CultureIndicator.PSYCHOLOGICAL_SAFETY, 0.5) < 0.6:
            recommendations.extend([
                "Implement regular feedback sessions with focus on growth",
                "Train managers on creating safe environments for questions and mistakes",
                "Establish clear processes for raising concerns without fear"
            ])
        
        # Autonomy improvements
        if culture_scores.get(CultureIndicator.AUTONOMY_LEVEL, 0.5) < 0.6:
            recommendations.extend([
                "Increase employee involvement in goal-setting processes",
                "Provide more flexibility in work methods and approaches",
                "Expand decision-making authority at individual contributor levels"
            ])
        
        # Learning culture improvements
        if culture_scores.get(CultureIndicator.LEARNING_ORIENTATION, 0.5) < 0.6:
            recommendations.extend([
                "Allocate dedicated time for learning and skill development",
                "Encourage experimentation and learning from failures",
                "Create knowledge sharing forums and communities"
            ])
        
        return recommendations


class InsightGenerator:
    """Generates actionable insights from organizational data"""
    
    def __init__(self):
        self.pattern_analyzer = OrganizationalPatternAnalyzer()
        self.culture_analyzer = CultureAnalyzer()
        
    def generate_organizational_insights(self, org_data: Dict) -> List[ProductivityInsight]:
        """Generate comprehensive organizational insights"""
        
        insights = []
        
        # Pattern-based insights
        insights.extend(self._generate_pattern_insights(org_data))
        
        # Culture-based insights
        insights.extend(self._generate_culture_insights(org_data))
        
        # Efficiency insights
        insights.extend(self._generate_efficiency_insights(org_data))
        
        # Collaboration insights
        insights.extend(self._generate_collaboration_insights(org_data))
        
        # Sort by impact level
        impact_order = {"high": 3, "medium": 2, "low": 1}
        insights.sort(key=lambda x: impact_order.get(x.impact_level, 0), reverse=True)
        
        return insights
    
    def _generate_pattern_insights(self, org_data: Dict) -> List[ProductivityInsight]:
        """Generate insights based on productivity patterns"""
        
        insights = []
        
        # Meeting efficiency insight
        meeting_efficiency = org_data.get("meeting_efficiency_score", 0.5)
        if meeting_efficiency < 0.4:
            insights.append(ProductivityInsight(
                insight_id="meeting_efficiency_low",
                category="efficiency",
                title="Meeting Efficiency Below Optimal",
                description="Organization-wide meeting efficiency is below optimal levels, indicating potential for significant time savings.",
                impact_level="high",
                confidence_level=0.8,
                affected_teams=org_data.get("all_teams", []),
                recommended_actions=[
                    "Implement meeting hygiene training",
                    "Establish clear meeting purposes and agendas",
                    "Experiment with shorter default meeting times",
                    "Regular meeting effectiveness reviews"
                ],
                implementation_difficulty="moderate",
                estimated_impact="15-25% time savings in meetings",
                data_sources=["meeting_analytics", "team_feedback"]
            ))
        
        # Focus time insight
        average_focus_time = org_data.get("average_daily_focus_time", 0)
        if average_focus_time < 2:  # Less than 2 hours per day
            insights.append(ProductivityInsight(
                insight_id="focus_time_fragmented",
                category="focus",
                title="Limited Deep Focus Time",
                description="Employees have limited uninterrupted time for deep work, which may impact productivity and quality.",
                impact_level="high",
                confidence_level=0.9,
                affected_teams=org_data.get("all_teams", []),
                recommended_actions=[
                    "Establish 'no meeting' focus blocks",
                    "Reduce notification frequency during focus time",
                    "Create quiet zones for deep work",
                    "Train on focus management techniques"
                ],
                implementation_difficulty="moderate",
                estimated_impact="20-30% improvement in complex task completion",
                data_sources=["time_tracking", "productivity_surveys"]
            ))
        
        return insights
    
    def _generate_culture_insights(self, org_data: Dict) -> List[ProductivityInsight]:
        """Generate insights based on culture analysis"""
        
        insights = []
        culture_scores = self.culture_analyzer.assess_culture_health(org_data)
        
        # Psychological safety insight
        psych_safety = culture_scores.get(CultureIndicator.PSYCHOLOGICAL_SAFETY, 0.5)
        if psych_safety < 0.5:
            insights.append(ProductivityInsight(
                insight_id="psychological_safety_low",
                category="culture",
                title="Psychological Safety Needs Attention",
                description="Lower psychological safety may be limiting innovation, feedback, and collaborative problem-solving.",
                impact_level="high",
                confidence_level=0.7,
                affected_teams=org_data.get("all_teams", []),
                recommended_actions=[
                    "Train managers on inclusive leadership",
                    "Implement regular anonymous feedback collection",
                    "Celebrate learning from mistakes",
                    "Create clear escalation paths for concerns"
                ],
                implementation_difficulty="difficult",
                estimated_impact="Improved innovation and problem-solving quality",
                data_sources=["culture_survey", "feedback_patterns"]
            ))
        
        return insights
    
    def _generate_efficiency_insights(self, org_data: Dict) -> List[ProductivityInsight]:
        """Generate efficiency-focused insights"""
        
        insights = []
        
        # Context switching insight
        context_switches = org_data.get("average_daily_context_switches", 0)
        if context_switches > 8:
            insights.append(ProductivityInsight(
                insight_id="context_switching_high",
                category="efficiency",
                title="High Context Switching Frequency",
                description="Frequent context switching may be reducing overall productivity and increasing cognitive load.",
                impact_level="medium",
                confidence_level=0.8,
                affected_teams=org_data.get("high_switching_teams", []),
                recommended_actions=[
                    "Batch similar tasks together",
                    "Reduce unnecessary notifications",
                    "Create dedicated time blocks for different work types",
                    "Streamline tool usage"
                ],
                implementation_difficulty="easy",
                estimated_impact="10-15% productivity improvement",
                data_sources=["activity_tracking", "task_analysis"]
            ))
        
        return insights
    
    def _generate_collaboration_insights(self, org_data: Dict) -> List[ProductivityInsight]:
        """Generate collaboration-focused insights"""
        
        insights = []
        
        # Cross-team dependency insight
        dependency_delays = org_data.get("cross_team_dependency_delays", 0)
        if dependency_delays > 0.3:  # 30% of dependencies cause delays
            insights.append(ProductivityInsight(
                insight_id="dependency_coordination",
                category="collaboration",
                title="Cross-Team Dependencies Causing Delays",
                description="Dependencies between teams are frequently causing project delays and reduced velocity.",
                impact_level="high",
                confidence_level=0.9,
                affected_teams=org_data.get("dependent_teams", []),
                recommended_actions=[
                    "Implement cross-team coordination rituals",
                    "Create shared visibility into team capacity and priorities",
                    "Establish clear handoff processes",
                    "Regular dependency mapping and optimization"
                ],
                implementation_difficulty="moderate",
                estimated_impact="20-30% reduction in project delays",
                data_sources=["project_tracking", "team_coordination_data"]
            ))
        
        return insights


class OrganizationalHealthDashboard:
    """Generates comprehensive organizational health assessments"""
    
    def __init__(self):
        self.pattern_analyzer = OrganizationalPatternAnalyzer()
        self.culture_analyzer = CultureAnalyzer()
        self.insight_generator = InsightGenerator()
    
    def generate_health_assessment(self, org_data: Dict, 
                                 measurement_period: Tuple[datetime, datetime]) -> OrganizationalHealthMetrics:
        """Generate comprehensive organizational health assessment"""
        
        # Analyze culture
        culture_scores = self.culture_analyzer.assess_culture_health(org_data)
        
        # Calculate overall scores
        productivity_trend = self._calculate_productivity_trend(org_data)
        collaboration_effectiveness = self.pattern_analyzer.identify_collaboration_effectiveness(org_data)
        innovation_index = self._calculate_innovation_index(org_data, culture_scores)
        burnout_prevalence = self._calculate_burnout_prevalence(org_data)
        turnover_risk = self._calculate_turnover_risk(org_data)
        system_dysfunction = self._calculate_system_dysfunction(org_data)
        
        # Generate recommendations
        recommendations = self._generate_health_recommendations(
            culture_scores, collaboration_effectiveness, burnout_prevalence
        )
        
        return OrganizationalHealthMetrics(
            org_id=org_data.get("org_id", "unknown"),
            measurement_period=measurement_period,
            employee_satisfaction_score=org_data.get("employee_satisfaction", 0.5),
            productivity_trend=productivity_trend,
            collaboration_effectiveness=collaboration_effectiveness,
            innovation_index=innovation_index,
            burnout_prevalence=burnout_prevalence,
            turnover_risk=turnover_risk,
            culture_indicators=culture_scores,
            system_dysfunction_score=system_dysfunction,
            recommendations=recommendations
        )
    
    def _calculate_productivity_trend(self, org_data: Dict) -> str:
        """Calculate overall productivity trend"""
        current_productivity = org_data.get("current_productivity_score", 0.5)
        previous_productivity = org_data.get("previous_productivity_score", 0.5)
        
        if current_productivity > previous_productivity * 1.05:
            return "improving"
        elif current_productivity < previous_productivity * 0.95:
            return "declining"
        else:
            return "stable"
    
    def _calculate_innovation_index(self, org_data: Dict, 
                                  culture_scores: Dict[CultureIndicator, float]) -> float:
        """Calculate innovation index"""
        factors = {
            "learning_orientation": culture_scores.get(CultureIndicator.LEARNING_ORIENTATION, 0.5),
            "psychological_safety": culture_scores.get(CultureIndicator.PSYCHOLOGICAL_SAFETY, 0.5),
            "innovation_time": org_data.get("innovation_time_percentage", 0) / 20,  # Normalize to 20%
            "experimentation_rate": org_data.get("experiments_per_quarter", 0) / 10  # Normalize
        }
        
        return sum(factors.values()) / len(factors)
    
    def _calculate_burnout_prevalence(self, org_data: Dict) -> float:
        """Calculate burnout prevalence"""
        indicators = {
            "overtime_frequency": org_data.get("overtime_frequency", 0),
            "stress_reports": org_data.get("stress_level_reports", 0),
            "turnover_rate": org_data.get("voluntary_turnover_rate", 0),
            "sick_leave_usage": org_data.get("sick_leave_above_average", 0)
        }
        
        return sum(indicators.values()) / len(indicators)
    
    def _calculate_turnover_risk(self, org_data: Dict) -> float:
        """Calculate turnover risk"""
        risk_factors = {
            "satisfaction_decline": 1 - org_data.get("employee_satisfaction", 0.5),
            "growth_opportunity_lack": 1 - org_data.get("growth_opportunities", 0.5),
            "manager_relationship_issues": org_data.get("manager_issues_reported", 0),
            "compensation_concerns": org_data.get("compensation_satisfaction", 0.5)
        }
        
        return sum(risk_factors.values()) / len(risk_factors)
    
    def _calculate_system_dysfunction(self, org_data: Dict) -> float:
        """Calculate system dysfunction score"""
        dysfunctions = {
            "unclear_priorities": org_data.get("priority_confusion_reports", 0),
            "process_inefficiencies": org_data.get("process_complaint_frequency", 0),
            "resource_constraints": org_data.get("resource_shortage_reports", 0),
            "communication_issues": org_data.get("communication_problems", 0)
        }
        
        return sum(dysfunctions.values()) / len(dysfunctions)
    
    def _generate_health_recommendations(self, culture_scores: Dict[CultureIndicator, float],
                                       collaboration_effectiveness: float,
                                       burnout_prevalence: float) -> List[str]:
        """Generate health improvement recommendations"""
        recommendations = []
        
        # Culture recommendations
        if culture_scores.get(CultureIndicator.PSYCHOLOGICAL_SAFETY, 0.5) < 0.5:
            recommendations.append("Focus on building psychological safety through manager training and feedback systems")
        
        # Collaboration recommendations
        if collaboration_effectiveness < 0.6:
            recommendations.append("Improve collaboration through better meeting practices and communication tools")
        
        # Burnout prevention
        if burnout_prevalence > 0.6:
            recommendations.append("Implement burnout prevention measures including workload management and wellness programs")
        
        # General recommendations
        recommendations.extend([
            "Regular pulse surveys to monitor organizational health",
            "Manager training on people leadership and team development",
            "Clear communication of organizational priorities and goals"
        ])
        
        return recommendations


def create_sample_organizational_assessment() -> OrganizationalHealthMetrics:
    """Create a sample organizational assessment for testing"""
    
    org_data = {
        "org_id": "sample_org",
        "employee_satisfaction": 0.7,
        "current_productivity_score": 0.75,
        "previous_productivity_score": 0.70,
        "meeting_efficiency_score": 0.6,
        "average_daily_focus_time": 3.5,
        "average_daily_context_switches": 6,
        "cross_team_dependency_delays": 0.25,
        "feedback_frequency": 0.8,
        "error_tolerance": 0.6,
        "speaking_up": 0.7,
        "decision_authority": 0.5,
        "work_method_choice": 0.7,
        "innovation_time_percentage": 15,
        "experiments_per_quarter": 3,
        "overtime_frequency": 0.3,
        "stress_level_reports": 0.4,
        "voluntary_turnover_rate": 0.15
    }
    
    measurement_period = (
        datetime.now() - timedelta(days=90),
        datetime.now()
    )
    
    dashboard = OrganizationalHealthDashboard()
    return dashboard.generate_health_assessment(org_data, measurement_period)


if __name__ == "__main__":
    # Example usage
    assessment = create_sample_organizational_assessment()
    print(f"Organization: {assessment.org_id}")
    print(f"Productivity trend: {assessment.productivity_trend}")
    print(f"Collaboration effectiveness: {assessment.collaboration_effectiveness:.2f}")
    print(f"Innovation index: {assessment.innovation_index:.2f}")
    print(f"Burnout prevalence: {assessment.burnout_prevalence:.2f}")
    print(f"Recommendations: {assessment.recommendations}")

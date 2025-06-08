
"""
FlowState Procrastination Analysis Module

Root cause analysis for procrastination patterns that addresses systemic, rational,
and individual factors while maintaining ethical boundaries around psychological assessment.

Based on expert analysis emphasizing:
- Distinguishing systemic causes from individual issues
- Recognizing when procrastination is rational avoidance
- Professional referral for clinical-level concerns
- User agency in self-discovery
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from enum import Enum
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ProcrastinationType(Enum):
    """Types of procrastination based on root causes"""
    SYSTEMIC = "systemic"
    RATIONAL = "rational"
    INDIVIDUAL = "individual"
    PROFESSIONAL_REFERRAL_NEEDED = "professional_referral"


class SystemicCause(Enum):
    """Organizational/systemic causes of procrastination"""
    UNCLEAR_REQUIREMENTS = "unclear_requirements"
    UNREALISTIC_DEADLINES = "unrealistic_deadlines"
    RESOURCE_SHORTAGE = "resource_shortage"
    CONFLICTING_PRIORITIES = "conflicting_priorities"
    ORGANIZATIONAL_DYSFUNCTION = "organizational_dysfunction"


class ReferralReason(Enum):
    """Reasons for professional mental health referral"""
    PERSISTENT_ANXIETY = "persistent_anxiety"
    DEPRESSION_INDICATORS = "depression_indicators"
    ATTENTION_DIFFICULTIES = "attention_difficulties"
    PERFECTIONISM_PARALYSIS = "perfectionism_paralysis"
    CHRONIC_OVERWHELM = "chronic_overwhelm"


@dataclass
class TaskContext:
    """Context information about a task being procrastinated"""
    task_id: str
    description: str
    deadline: Optional[datetime]
    estimated_duration: Optional[timedelta]
    clarity_score: float  # 0-1, how clear are the requirements
    resource_availability: float  # 0-1, how available are needed resources
    personal_meaningfulness: float  # 0-1, how meaningful to the user
    skill_match: float  # 0-1, how well skills match requirements
    competing_tasks: List[str]
    organizational_priority: Optional[float]  # 0-1, org-stated priority


@dataclass
class UserContext:
    """User's current context and patterns"""
    user_id: str
    current_stress_level: float  # 0-1, self-reported
    energy_level: float  # 0-1, self-reported
    recent_procrastination_patterns: List[str]
    support_systems: List[str]
    previous_successful_strategies: List[str]
    anxiety_indicators: int  # frequency of anxiety-related behaviors
    depression_indicators: int  # frequency of depression-related behaviors
    attention_difficulties: int  # frequency of attention-related struggles


@dataclass
class ProcrastinationAnalysis:
    """Results of procrastination analysis"""
    primary_type: ProcrastinationType
    confidence: float  # 0-1, confidence in assessment
    systemic_factors: List[SystemicCause]
    rational_factors: List[str]
    addressable_factors: List[str]
    recommended_actions: List[str]
    referral_reason: Optional[ReferralReason]
    user_explanation: str  # Plain English explanation


class SystemicCauseDetector:
    """Identifies systemic/organizational causes of procrastination"""
    
    def __init__(self):
        self.clarity_threshold = 0.3  # Below this, requirements are unclear
        self.resource_threshold = 0.4  # Below this, resources are insufficient
        self.deadline_pressure_threshold = 0.8  # Above this, deadline is unrealistic
    
    def analyze_systemic_factors(self, task: TaskContext) -> List[SystemicCause]:
        """Identify systemic causes in task context"""
        factors = []
        
        # Check for unclear requirements
        if task.clarity_score < self.clarity_threshold:
            factors.append(SystemicCause.UNCLEAR_REQUIREMENTS)
            logger.info(f"Task {task.task_id}: Unclear requirements detected")
        
        # Check for resource shortage
        if task.resource_availability < self.resource_threshold:
            factors.append(SystemicCause.RESOURCE_SHORTAGE)
            logger.info(f"Task {task.task_id}: Resource shortage detected")
        
        # Check for unrealistic deadlines
        if task.deadline and task.estimated_duration:
            time_to_deadline = task.deadline - datetime.now()
            if time_to_deadline < task.estimated_duration * 1.5:  # Less than 1.5x estimated time
                factors.append(SystemicCause.UNREALISTIC_DEADLINES)
                logger.info(f"Task {task.task_id}: Unrealistic deadline detected")
        
        # Check for conflicting priorities
        if len(task.competing_tasks) > 3:
            factors.append(SystemicCause.CONFLICTING_PRIORITIES)
            logger.info(f"Task {task.task_id}: Conflicting priorities detected")
        
        return factors
    
    def calculate_systemic_score(self, factors: List[SystemicCause]) -> float:
        """Calculate how much procrastination is due to systemic factors"""
        if not factors:
            return 0.0
        
        # Weight different factors
        weights = {
            SystemicCause.UNCLEAR_REQUIREMENTS: 0.3,
            SystemicCause.UNREALISTIC_DEADLINES: 0.3,
            SystemicCause.RESOURCE_SHORTAGE: 0.25,
            SystemicCause.CONFLICTING_PRIORITIES: 0.15
        }
        
        total_weight = sum(weights.get(factor, 0.1) for factor in factors)
        return min(total_weight, 1.0)


class RationalAvoidanceAssessor:
    """Assesses whether procrastination is rational decision-making"""
    
    def __init__(self):
        self.meaningfulness_threshold = 0.3
        self.skill_mismatch_threshold = 0.4
        self.success_probability_threshold = 0.3
    
    def assess_rational_avoidance(self, task: TaskContext, user: UserContext) -> Dict[str, Union[bool, str]]:
        """Determine if avoiding this task is rationally justified"""
        reasons = []
        
        # Low personal meaningfulness
        if task.personal_meaningfulness < self.meaningfulness_threshold:
            reasons.append("Task has low personal meaning or value alignment")
        
        # Significant skill mismatch
        if task.skill_match < self.skill_mismatch_threshold:
            reasons.append("Task requires skills not yet developed")
        
        # Low probability of success
        success_probability = (task.clarity_score + task.resource_availability + task.skill_match) / 3
        if success_probability < self.success_probability_threshold:
            reasons.append("Low probability of successful completion given current conditions")
        
        # Better alternatives available
        if task.organizational_priority and task.organizational_priority < 0.5:
            reasons.append("Other tasks may provide better return on time investment")
        
        is_rational = len(reasons) >= 2  # Multiple rational reasons
        
        return {
            "is_rational": is_rational,
            "reasons": reasons,
            "recommendation": "Consider task elimination, delegation, or modification" if is_rational else None
        }


class ProfessionalReferralAssessor:
    """Determines when professional mental health support is recommended"""
    
    def __init__(self):
        self.anxiety_threshold = 7  # Out of 10 frequency scale
        self.depression_threshold = 6
        self.attention_threshold = 8
        self.pattern_duration_threshold = 14  # Days
    
    def assess_referral_need(self, user: UserContext, task: TaskContext) -> Optional[ReferralReason]:
        """Determine if professional referral is recommended"""
        
        # High anxiety indicators
        if user.anxiety_indicators >= self.anxiety_threshold:
            logger.info(f"User {user.user_id}: High anxiety indicators detected")
            return ReferralReason.PERSISTENT_ANXIETY
        
        # Depression indicators
        if user.depression_indicators >= self.depression_threshold:
            logger.info(f"User {user.user_id}: Depression indicators detected")
            return ReferralReason.DEPRESSION_INDICATORS
        
        # Attention difficulties
        if user.attention_difficulties >= self.attention_threshold:
            logger.info(f"User {user.user_id}: Attention difficulties detected")
            return ReferralReason.ATTENTION_DIFFICULTIES
        
        # Perfectionism paralysis pattern
        if ("perfectionism" in user.recent_procrastination_patterns and 
            user.current_stress_level > 0.7):
            logger.info(f"User {user.user_id}: Perfectionism paralysis pattern detected")
            return ReferralReason.PERFECTIONISM_PARALYSIS
        
        # Chronic overwhelm
        if (user.current_stress_level > 0.8 and 
            user.energy_level < 0.3 and
            len(user.recent_procrastination_patterns) > 5):
            logger.info(f"User {user.user_id}: Chronic overwhelm detected")
            return ReferralReason.CHRONIC_OVERWHELM
        
        return None


class AddressableFactorIdentifier:
    """Identifies factors within user's control that can be addressed"""
    
    def identify_addressable_factors(self, task: TaskContext, user: UserContext) -> List[str]:
        """Find factors user can actually change"""
        factors = []
        
        # Skill development opportunities
        if 0.3 <= task.skill_match <= 0.7:  # Learnable gap
            factors.append("Skill development: This task could help build capabilities")
        
        # Environmental modifications
        if user.energy_level < 0.5:
            factors.append("Energy management: Consider optimal timing for this type of work")
        
        # Task breakdown possibilities
        if task.estimated_duration and task.estimated_duration > timedelta(hours=2):
            factors.append("Task chunking: Break into smaller, manageable pieces")
        
        # Support seeking opportunities
        if task.clarity_score < 0.5 and user.support_systems:
            factors.append("Clarification seeking: Ask for clearer requirements")
        
        # Approach modifications
        if task.skill_match < 0.5:
            factors.append("Alternative approaches: Find different ways to accomplish goal")
        
        return factors


class ProcrastinationAnalyzer:
    """Main class for analyzing procrastination patterns"""
    
    def __init__(self):
        self.systemic_detector = SystemicCauseDetector()
        self.rational_assessor = RationalAvoidanceAssessor()
        self.referral_assessor = ProfessionalReferralAssessor()
        self.addressable_identifier = AddressableFactorIdentifier()
    
    def analyze_procrastination(self, task: TaskContext, user: UserContext) -> ProcrastinationAnalysis:
        """Comprehensive procrastination analysis"""
        
        # Check for professional referral needs first
        referral_reason = self.referral_assessor.assess_referral_need(user, task)
        if referral_reason:
            return self._create_referral_analysis(referral_reason, user)
        
        # Analyze systemic factors
        systemic_factors = self.systemic_detector.analyze_systemic_factors(task)
        systemic_score = self.systemic_detector.calculate_systemic_score(systemic_factors)
        
        # Assess rational avoidance
        rational_assessment = self.rational_assessor.assess_rational_avoidance(task, user)
        
        # Identify addressable factors
        addressable_factors = self.addressable_identifier.identify_addressable_factors(task, user)
        
        # Determine primary type and recommendations
        if systemic_score > 0.7:
            return self._create_systemic_analysis(systemic_factors, task, user)
        elif rational_assessment["is_rational"]:
            return self._create_rational_analysis(rational_assessment, task, user)
        else:
            return self._create_individual_analysis(addressable_factors, task, user)
    
    def _create_systemic_analysis(self, factors: List[SystemicCause], 
                                task: TaskContext, user: UserContext) -> ProcrastinationAnalysis:
        """Create analysis for systemic procrastination"""
        recommendations = [
            "Document the systemic issues affecting this task",
            "Escalate unclear requirements to appropriate stakeholders",
            "Request additional resources or timeline adjustment",
            "This is likely not a personal productivity issue"
        ]
        
        explanation = (
            "Your procrastination on this task appears to be caused by organizational "
            "or systemic factors outside your control. This is a rational response to "
            "unclear requirements, insufficient resources, or unrealistic expectations."
        )
        
        return ProcrastinationAnalysis(
            primary_type=ProcrastinationType.SYSTEMIC,
            confidence=0.8,
            systemic_factors=factors,
            rational_factors=[],
            addressable_factors=[],
            recommended_actions=recommendations,
            referral_reason=None,
            user_explanation=explanation
        )
    
    def _create_rational_analysis(self, assessment: Dict, 
                                task: TaskContext, user: UserContext) -> ProcrastinationAnalysis:
        """Create analysis for rational avoidance"""
        recommendations = [
            "Consider whether this task should be eliminated or modified",
            "Explore delegation or collaboration opportunities",
            "Negotiate task requirements or timeline",
            "Your instincts about avoiding this task may be correct"
        ]
        
        explanation = (
            f"Your avoidance of this task appears to be rational decision-making. "
            f"Reasons include: {', '.join(assessment['reasons'])}. Consider whether "
            f"the task needs to be modified rather than forcing completion."
        )
        
        return ProcrastinationAnalysis(
            primary_type=ProcrastinationType.RATIONAL,
            confidence=0.7,
            systemic_factors=[],
            rational_factors=assessment["reasons"],
            addressable_factors=[],
            recommended_actions=recommendations,
            referral_reason=None,
            user_explanation=explanation
        )
    
    def _create_individual_analysis(self, addressable_factors: List[str],
                                   task: TaskContext, user: UserContext) -> ProcrastinationAnalysis:
        """Create analysis for individual-level procrastination"""
        recommendations = [
            "Focus on the addressable factors identified below",
            "Try breaking the task into smaller pieces",
            "Consider when your energy levels are best for this type of work",
            "Seek support or clarification where available"
        ]
        
        if user.previous_successful_strategies:
            recommendations.append(f"Consider using strategies that worked before: {', '.join(user.previous_successful_strategies)}")
        
        explanation = (
            "This procrastination appears to have individual factors that you can address. "
            "Focus on the specific elements within your control rather than trying to "
            "force motivation."
        )
        
        return ProcrastinationAnalysis(
            primary_type=ProcrastinationType.INDIVIDUAL,
            confidence=0.6,
            systemic_factors=[],
            rational_factors=[],
            addressable_factors=addressable_factors,
            recommended_actions=recommendations,
            referral_reason=None,
            user_explanation=explanation
        )
    
    def _create_referral_analysis(self, reason: ReferralReason, 
                                user: UserContext) -> ProcrastinationAnalysis:
        """Create analysis recommending professional support"""
        referral_messages = {
            ReferralReason.PERSISTENT_ANXIETY: "Consider speaking with a counselor or therapist about anxiety management techniques",
            ReferralReason.DEPRESSION_INDICATORS: "A mental health professional could help address underlying mood concerns",
            ReferralReason.ATTENTION_DIFFICULTIES: "Consider an evaluation for ADHD or other attention-related conditions",
            ReferralReason.PERFECTIONISM_PARALYSIS: "A therapist specializing in perfectionism could provide helpful strategies",
            ReferralReason.CHRONIC_OVERWHELM: "Professional support could help develop better stress management strategies"
        }
        
        explanation = (
            "Your procrastination patterns suggest that professional mental health support "
            "could be helpful. This is very common and nothing to be concerned about. "
            f"{referral_messages.get(reason, 'Professional guidance could be beneficial.')}"
        )
        
        return ProcrastinationAnalysis(
            primary_type=ProcrastinationType.PROFESSIONAL_REFERRAL_NEEDED,
            confidence=0.9,
            systemic_factors=[],
            rational_factors=[],
            addressable_factors=[],
            recommended_actions=["Consider scheduling an appointment with a mental health professional"],
            referral_reason=reason,
            user_explanation=explanation
        )


class ProcrastinationPatternTracker:
    """Tracks procrastination patterns over time without being invasive"""
    
    def __init__(self):
        self.pattern_storage = {}  # In real app, this would be proper storage
    
    def record_procrastination_episode(self, user_id: str, task_id: str, 
                                     analysis: ProcrastinationAnalysis):
        """Record a procrastination episode for pattern detection"""
        if user_id not in self.pattern_storage:
            self.pattern_storage[user_id] = []
        
        episode = {
            "timestamp": datetime.now(),
            "task_id": task_id,
            "type": analysis.primary_type,
            "systemic_factors": analysis.systemic_factors,
            "rational_factors": analysis.rational_factors
        }
        
        self.pattern_storage[user_id].append(episode)
        
        # Keep only last 30 days
        cutoff = datetime.now() - timedelta(days=30)
        self.pattern_storage[user_id] = [
            ep for ep in self.pattern_storage[user_id] 
            if ep["timestamp"] > cutoff
        ]
    
    def get_user_patterns(self, user_id: str) -> Dict[str, Union[int, List[str]]]:
        """Get user's procrastination patterns for self-reflection"""
        if user_id not in self.pattern_storage:
            return {"total_episodes": 0, "common_types": [], "insights": []}
        
        episodes = self.pattern_storage[user_id]
        type_counts = {}
        
        for episode in episodes:
            ep_type = episode["type"].value
            type_counts[ep_type] = type_counts.get(ep_type, 0) + 1
        
        # Generate insights
        insights = []
        total = len(episodes)
        
        if total > 0:
            systemic_ratio = type_counts.get("systemic", 0) / total
            if systemic_ratio > 0.6:
                insights.append("Many of your procrastination episodes seem to be caused by organizational issues")
            
            rational_ratio = type_counts.get("rational", 0) / total
            if rational_ratio > 0.4:
                insights.append("You often avoid tasks that may not be worth your time - this could be good instincts")
        
        return {
            "total_episodes": total,
            "common_types": sorted(type_counts.keys(), key=lambda x: type_counts[x], reverse=True),
            "insights": insights
        }


def create_sample_analysis() -> ProcrastinationAnalysis:
    """Create a sample analysis for testing"""
    task = TaskContext(
        task_id="sample_task",
        description="Write quarterly report",
        deadline=datetime.now() + timedelta(days=2),
        estimated_duration=timedelta(hours=8),
        clarity_score=0.3,  # Unclear requirements
        resource_availability=0.6,
        personal_meaningfulness=0.5,
        skill_match=0.7,
        competing_tasks=["client_presentation", "team_meeting", "budget_review"],
        organizational_priority=0.8
    )
    
    user = UserContext(
        user_id="sample_user",
        current_stress_level=0.6,
        energy_level=0.4,
        recent_procrastination_patterns=["unclear_tasks", "overwhelming_projects"],
        support_systems=["manager", "colleagues"],
        previous_successful_strategies=["breaking_into_chunks", "asking_for_clarification"],
        anxiety_indicators=5,
        depression_indicators=3,
        attention_difficulties=4
    )
    
    analyzer = ProcrastinationAnalyzer()
    return analyzer.analyze_procrastination(task, user)


if __name__ == "__main__":
    # Example usage
    analysis = create_sample_analysis()
    print(f"Procrastination Type: {analysis.primary_type.value}")
    print(f"Confidence: {analysis.confidence}")
    print(f"Explanation: {analysis.user_explanation}")
    print(f"Recommended Actions: {analysis.recommended_actions}")

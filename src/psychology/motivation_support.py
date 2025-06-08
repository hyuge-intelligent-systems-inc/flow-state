
"""
FlowState Motivation Support Module

Intrinsic motivation support system based on Self-Determination Theory that enhances
rather than undermines natural human motivation through autonomy, competence, and purpose.

Based on expert analysis emphasizing:
- Protecting intrinsic motivation from external corruption
- Supporting autonomy, competence, and relatedness
- Avoiding manipulation and external rewards
- Cultural sensitivity and individual differences
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple
from enum import Enum
import logging
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class MotivationType(Enum):
    """Types of motivation according to Self-Determination Theory"""
    INTRINSIC = "intrinsic"
    INTEGRATED = "integrated"  # Fully internalized extrinsic
    IDENTIFIED = "identified"  # Personally important extrinsic
    INTROJECTED = "introjected"  # Partially internalized (guilt/shame driven)
    EXTERNAL = "external"  # Purely external rewards/punishments
    AMOTIVATED = "amotivated"  # Lack of motivation


class AutonomyThreat(Enum):
    """Things that threaten sense of autonomy"""
    EXTERNAL_PRESSURE = "external_pressure"
    SURVEILLANCE = "surveillance"
    CONTROLLING_LANGUAGE = "controlling_language"
    IMPOSED_GOALS = "imposed_goals"
    RESTRICTED_CHOICE = "restricted_choice"


class CompetenceBarrier(Enum):
    """Barriers to feeling competent"""
    UNCLEAR_EXPECTATIONS = "unclear_expectations"
    INSUFFICIENT_FEEDBACK = "insufficient_feedback"
    OVERWHELMING_CHALLENGE = "overwhelming_challenge"
    TRIVIAL_CHALLENGE = "trivial_challenge"
    LACK_OF_PROGRESS_VISIBILITY = "lack_of_progress_visibility"


class PurposeDisconnection(Enum):
    """Ways work becomes disconnected from purpose"""
    VALUES_MISALIGNMENT = "values_misalignment"
    UNCLEAR_IMPACT = "unclear_impact"
    MEANINGLESS_TASKS = "meaningless_tasks"
    IDENTITY_CONFLICT = "identity_conflict"
    ISOLATION_FROM_OTHERS = "isolation_from_others"


@dataclass
class UserValues:
    """User's personal values and what matters to them"""
    core_values: List[str]
    life_priorities: List[str]
    professional_aspirations: List[str]
    contribution_desires: List[str]  # How they want to help others
    identity_elements: List[str]  # How they see themselves
    cultural_background: Optional[str] = None


@dataclass
class TaskMeaning:
    """How a task connects to user's sense of purpose"""
    task_id: str
    personal_value_connections: List[str]
    skill_development_opportunities: List[str]
    impact_on_others: Optional[str]
    contribution_to_larger_goals: Optional[str]
    identity_reinforcement: List[str]
    meaning_score: float  # 0-1, how meaningful the task feels


@dataclass
class AutonomyProfile:
    """User's autonomy needs and current state"""
    preferred_choice_level: str  # "high", "moderate", "structured"
    decision_making_style: str  # "independent", "collaborative", "guided"
    control_preferences: List[str]  # What they want control over
    current_autonomy_satisfaction: float  # 0-1
    autonomy_threats: List[AutonomyThreat]


@dataclass
class CompetenceProfile:
    """User's competence development and current state"""
    current_skills: Dict[str, float]  # Skill name -> proficiency (0-1)
    growth_areas: List[str]
    preferred_challenge_level: str  # "gradual", "moderate", "steep"
    feedback_preferences: List[str]
    confidence_level: float  # 0-1
    competence_barriers: List[CompetenceBarrier]


@dataclass
class RelatednessProfile:
    """User's social connection needs and current state"""
    collaboration_preferences: str  # "solo", "small_group", "team", "community"
    support_network: List[str]
    mentorship_interests: List[str]  # "giving", "receiving", "peer"
    social_impact_importance: float  # 0-1
    current_connection_satisfaction: float  # 0-1


@dataclass
class MotivationAssessment:
    """Assessment of current motivation state"""
    primary_motivation_type: MotivationType
    autonomy_level: float  # 0-1
    competence_level: float  # 0-1
    relatedness_level: float  # 0-1
    intrinsic_motivation_threats: List[str]
    motivation_sustainability: float  # 0-1, how sustainable current motivation is
    recommendations: List[str]


class AutonomySupport:
    """Supports user's sense of autonomy and choice"""
    
    def __init__(self):
        self.controlling_language_patterns = [
            "you should", "you must", "you have to", "you need to"
        ]
        self.supportive_language_patterns = [
            "you might consider", "one option is", "you could", "what would work for you"
        ]
    
    def assess_autonomy_threats(self, user_context: Dict) -> List[AutonomyThreat]:
        """Identify current threats to user's autonomy"""
        threats = []
        
        # Check for external pressure
        if user_context.get("external_deadlines", 0) > 3:
            threats.append(AutonomyThreat.EXTERNAL_PRESSURE)
        
        # Check for surveillance feelings
        if user_context.get("feels_monitored", False):
            threats.append(AutonomyThreat.SURVEILLANCE)
        
        # Check for imposed goals
        if user_context.get("self_set_goals", 0) < user_context.get("imposed_goals", 0):
            threats.append(AutonomyThreat.IMPOSED_GOALS)
        
        # Check for choice restriction
        if user_context.get("choice_options", 0) < 2:
            threats.append(AutonomyThreat.RESTRICTED_CHOICE)
        
        return threats
    
    def provide_meaningful_choices(self, task_context: Dict) -> List[Dict[str, str]]:
        """Provide genuine choices about how to approach work"""
        choices = []
        
        # Method choices
        if task_context.get("task_type") == "creative":
            choices.extend([
                {"type": "method", "option": "Start with brainstorming", "rationale": "Generate ideas first"},
                {"type": "method", "option": "Begin with research", "rationale": "Build knowledge foundation"},
                {"type": "method", "option": "Create rough prototype", "rationale": "Learn through making"}
            ])
        
        # Timing choices
        choices.extend([
            {"type": "timing", "option": "Work in morning", "rationale": "When energy is highest"},
            {"type": "timing", "option": "Work in afternoon", "rationale": "When focus often improves"},
            {"type": "timing", "option": "Split across multiple sessions", "rationale": "Maintain freshness"}
        ])
        
        # Environment choices
        choices.extend([
            {"type": "environment", "option": "Quiet space", "rationale": "Minimize distractions"},
            {"type": "environment", "option": "Background ambiance", "rationale": "Pleasant stimulation"},
            {"type": "environment", "option": "Change locations", "rationale": "Vary context for freshness"}
        ])
        
        return choices
    
    def use_autonomy_supportive_language(self, message: str) -> str:
        """Convert controlling language to autonomy-supportive language"""
        for controlling, supportive in zip(self.controlling_language_patterns, 
                                         self.supportive_language_patterns):
            message = message.replace(controlling, supportive)
        
        # Add choice emphasis
        if "recommend" in message.lower():
            message += " What feels right for your situation?"
        
        return message
    
    def enhance_user_control(self, current_context: Dict) -> Dict[str, List[str]]:
        """Identify ways to increase user's sense of control"""
        control_enhancements = {
            "goal_setting": [
                "Define your own success criteria for this task",
                "Set personal milestones that matter to you",
                "Choose which aspects of the work to prioritize"
            ],
            "method_selection": [
                "Experiment with different approaches",
                "Modify suggested techniques to fit your style",
                "Create your own workflow variations"
            ],
            "timing_control": [
                "Work when your energy levels are best",
                "Take breaks when you need them",
                "Adjust session lengths to your preference"
            ],
            "feedback_control": [
                "Choose how often you want progress updates",
                "Select which metrics matter most to you",
                "Control the level of detail in feedback"
            ]
        }
        
        return control_enhancements


class CompetenceBuilder:
    """Supports development of genuine competence"""
    
    def __init__(self):
        self.optimal_challenge_ratio = 0.7  # Slightly above current ability
        self.skill_development_pace = "gradual"  # vs "rapid" or "intensive"
    
    def assess_current_competence(self, user_profile: CompetenceProfile, 
                                task_requirements: Dict) -> float:
        """Assess user's competence for specific task"""
        required_skills = task_requirements.get("required_skills", [])
        if not required_skills:
            return 0.5  # Neutral if no skills specified
        
        relevant_skills = [
            user_profile.current_skills.get(skill, 0.0) 
            for skill in required_skills
        ]
        
        return sum(relevant_skills) / len(relevant_skills) if relevant_skills else 0.0
    
    def design_optimal_challenge(self, current_competence: float, 
                               user_preferences: Dict) -> Dict[str, Union[str, float]]:
        """Design appropriately challenging experience"""
        target_difficulty = current_competence + 0.1  # Slightly above current level
        
        if user_preferences.get("challenge_preference") == "gradual":
            target_difficulty = min(target_difficulty, current_competence + 0.05)
        elif user_preferences.get("challenge_preference") == "steep":
            target_difficulty = min(target_difficulty, current_competence + 0.2)
        
        challenge_design = {
            "target_difficulty": target_difficulty,
            "support_level": "high" if target_difficulty > current_competence + 0.15 else "moderate",
            "breakdown_strategy": "micro_steps" if target_difficulty > current_competence + 0.1 else "normal",
            "feedback_frequency": "frequent" if target_difficulty > current_competence + 0.1 else "periodic"
        }
        
        return challenge_design
    
    def provide_competence_feedback(self, progress_data: Dict, 
                                  user_preferences: Dict) -> Dict[str, str]:
        """Provide feedback that builds sense of competence"""
        feedback = {}
        
        # Progress feedback
        if progress_data.get("completion_percentage", 0) > 0:
            progress = progress_data["completion_percentage"]
            feedback["progress"] = f"You've made meaningful progress: {progress:.0%} complete"
        
        # Skill development feedback
        if progress_data.get("new_skills_practiced"):
            skills = progress_data["new_skills_practiced"]
            feedback["skill_growth"] = f"You're developing: {', '.join(skills)}"
        
        # Problem-solving feedback
        if progress_data.get("challenges_overcome"):
            challenges = len(progress_data["challenges_overcome"])
            feedback["problem_solving"] = f"You've successfully navigated {challenges} challenges"
        
        # Quality feedback
        if progress_data.get("quality_indicators"):
            feedback["quality"] = "The quality of your work shows your growing expertise"
        
        return feedback
    
    def identify_skill_development_opportunities(self, current_skills: Dict[str, float],
                                               task_requirements: Dict) -> List[Dict[str, str]]:
        """Identify opportunities for skill growth"""
        opportunities = []
        
        required_skills = task_requirements.get("required_skills", [])
        
        for skill in required_skills:
            current_level = current_skills.get(skill, 0.0)
            
            if current_level < 0.3:
                opportunities.append({
                    "skill": skill,
                    "type": "foundational",
                    "description": f"Build foundational knowledge in {skill}",
                    "approach": "Start with basics and build gradually"
                })
            elif current_level < 0.7:
                opportunities.append({
                    "skill": skill,
                    "type": "development",
                    "description": f"Develop intermediate {skill} capabilities",
                    "approach": "Practice with guided challenges"
                })
            else:
                opportunities.append({
                    "skill": skill,
                    "type": "mastery",
                    "description": f"Refine {skill} expertise",
                    "approach": "Tackle complex applications"
                })
        
        return opportunities


class PurposeConnector:
    """Helps users connect tasks to personal meaning and purpose"""
    
    def __init__(self):
        self.meaning_categories = [
            "personal_growth", "helping_others", "creating_value", 
            "solving_problems", "expressing_creativity", "building_relationships"
        ]
    
    def assess_task_meaning(self, task_details: Dict, user_values: UserValues) -> TaskMeaning:
        """Assess how meaningful a task is to the user"""
        value_connections = self._find_value_connections(task_details, user_values)
        skill_opportunities = self._identify_skill_development(task_details, user_values)
        impact_assessment = self._assess_impact_on_others(task_details)
        identity_reinforcement = self._assess_identity_reinforcement(task_details, user_values)
        
        # Calculate overall meaning score
        meaning_score = (
            len(value_connections) * 0.3 +
            len(skill_opportunities) * 0.2 +
            (1.0 if impact_assessment else 0.0) * 0.3 +
            len(identity_reinforcement) * 0.2
        ) / 4.0
        
        return TaskMeaning(
            task_id=task_details.get("task_id", "unknown"),
            personal_value_connections=value_connections,
            skill_development_opportunities=skill_opportunities,
            impact_on_others=impact_assessment,
            contribution_to_larger_goals=task_details.get("larger_goal_connection"),
            identity_reinforcement=identity_reinforcement,
            meaning_score=min(meaning_score, 1.0)
        )
    
    def _find_value_connections(self, task_details: Dict, user_values: UserValues) -> List[str]:
        """Find connections between task and user's values"""
        connections = []
        
        task_keywords = task_details.get("description", "").lower().split()
        
        for value in user_values.core_values:
            value_keywords = value.lower().split()
            if any(keyword in task_keywords for keyword in value_keywords):
                connections.append(f"Aligns with your value of {value}")
        
        # Check for contribution connections
        if any(contrib in task_details.get("description", "").lower() 
               for contrib in ["help", "support", "assist", "improve"]):
            if "helping_others" in user_values.core_values:
                connections.append("Opportunity to help others")
        
        return connections
    
    def _identify_skill_development(self, task_details: Dict, user_values: UserValues) -> List[str]:
        """Identify skill development opportunities"""
        opportunities = []
        
        required_skills = task_details.get("required_skills", [])
        desired_skills = user_values.professional_aspirations
        
        for skill in required_skills:
            if any(aspiration in skill.lower() for aspiration in desired_skills):
                opportunities.append(f"Develops {skill} capabilities you want to build")
        
        return opportunities
    
    def _assess_impact_on_others(self, task_details: Dict) -> Optional[str]:
        """Assess how task impacts other people"""
        impact_keywords = ["customer", "client", "team", "user", "colleague", "community"]
        description = task_details.get("description", "").lower()
        
        for keyword in impact_keywords:
            if keyword in description:
                return f"Directly benefits {keyword}s"
        
        return None
    
    def _assess_identity_reinforcement(self, task_details: Dict, user_values: UserValues) -> List[str]:
        """Assess how task reinforces positive identity"""
        reinforcements = []
        
        identity_elements = user_values.identity_elements
        task_description = task_details.get("description", "").lower()
        
        for identity in identity_elements:
            identity_keywords = identity.lower().split()
            if any(keyword in task_description for keyword in identity_keywords):
                reinforcements.append(f"Reinforces your identity as {identity}")
        
        return reinforcements
    
    def enhance_task_meaning(self, task_meaning: TaskMeaning, 
                           user_values: UserValues) -> Dict[str, List[str]]:
        """Suggest ways to enhance the meaning of a task"""
        enhancements = {
            "value_alignment": [],
            "skill_framing": [],
            "impact_awareness": [],
            "identity_connection": []
        }
        
        # Value alignment enhancements
        if task_meaning.meaning_score < 0.5:
            enhancements["value_alignment"].extend([
                "Consider how this task serves your larger goals",
                "Connect this work to what matters most to you",
                "Frame this as an opportunity to practice your values"
            ])
        
        # Skill development framing
        enhancements["skill_framing"].extend([
            "Focus on what you'll learn from this experience",
            "Consider how this builds capabilities you want to develop",
            "View challenges as opportunities for growth"
        ])
        
        # Impact awareness
        enhancements["impact_awareness"].extend([
            "Consider who benefits from this work being done well",
            "Think about the positive ripple effects of your contribution",
            "Connect your effort to outcomes that matter to others"
        ])
        
        return enhancements


class IntrinsicMotivationProtector:
    """Protects intrinsic motivation from external corruption"""
    
    def __init__(self):
        self.motivation_threats = [
            "external_rewards", "surveillance", "competition", 
            "imposed_deadlines", "controlling_feedback"
        ]
    
    def assess_motivation_threats(self, current_context: Dict) -> List[str]:
        """Identify threats to intrinsic motivation"""
        threats = []
        
        # External rewards
        if current_context.get("external_rewards_present", False):
            threats.append("External rewards may be undermining natural motivation")
        
        # Surveillance
        if current_context.get("monitoring_level", 0) > 0.7:
            threats.append("High monitoring may be reducing sense of autonomy")
        
        # Competition
        if current_context.get("competitive_elements", False):
            threats.append("Competition may be shifting focus from intrinsic satisfaction")
        
        # Time pressure
        if current_context.get("time_pressure", 0) > 0.8:
            threats.append("High time pressure may be reducing enjoyment")
        
        return threats
    
    def protect_intrinsic_motivation(self, motivation_context: Dict) -> Dict[str, List[str]]:
        """Provide strategies to protect intrinsic motivation"""
        protections = {
            "avoid_external_rewards": [
                "Focus on internal satisfaction rather than external recognition",
                "Celebrate personal growth and learning",
                "Find joy in the process, not just outcomes"
            ],
            "maintain_autonomy": [
                "Preserve choice in how you approach tasks",
                "Set your own standards for quality",
                "Control your own learning and development pace"
            ],
            "emphasize_mastery": [
                "Focus on getting better rather than being the best",
                "Celebrate skill development and understanding",
                "View challenges as opportunities to grow"
            ],
            "connect_to_purpose": [
                "Regularly reflect on why this work matters to you",
                "Connect daily tasks to larger personal goals",
                "Consider how your work contributes to something meaningful"
            ]
        }
        
        return protections
    
    def design_motivation_sustainable_approach(self, user_profile: Dict) -> Dict[str, str]:
        """Design approach that maintains motivation over time"""
        sustainable_design = {
            "pacing": "Allow for natural rhythms rather than forcing consistent intensity",
            "variety": "Vary approaches and challenges to maintain interest",
            "ownership": "Maintain sense of personal ownership over work and goals",
            "growth": "Focus on continuous learning rather than performance optimization",
            "balance": "Balance challenge with achievability to maintain confidence",
            "reflection": "Regular reflection on personal satisfaction and meaning"
        }
        
        return sustainable_design


class MotivationAssessor:
    """Assesses user's current motivation state and provides support recommendations"""
    
    def __init__(self):
        self.autonomy_support = AutonomySupport()
        self.competence_builder = CompetenceBuilder()
        self.purpose_connector = PurposeConnector()
        self.intrinsic_protector = IntrinsicMotivationProtector()
    
    def assess_overall_motivation(self, user_context: Dict, 
                                task_context: Dict) -> MotivationAssessment:
        """Comprehensive motivation assessment"""
        
        # Assess autonomy level
        autonomy_threats = self.autonomy_support.assess_autonomy_threats(user_context)
        autonomy_level = max(0.0, 1.0 - len(autonomy_threats) * 0.2)
        
        # Assess competence level
        competence_level = user_context.get("competence_feeling", 0.5)
        
        # Assess relatedness level
        relatedness_level = user_context.get("connection_feeling", 0.5)
        
        # Identify motivation type
        motivation_type = self._determine_motivation_type(
            autonomy_level, competence_level, relatedness_level, user_context
        )
        
        # Assess intrinsic motivation threats
        intrinsic_threats = self.intrinsic_protector.assess_motivation_threats(user_context)
        
        # Calculate sustainability
        sustainability = (autonomy_level + competence_level + relatedness_level) / 3
        sustainability *= (1.0 - len(intrinsic_threats) * 0.1)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            motivation_type, autonomy_level, competence_level, 
            relatedness_level, intrinsic_threats
        )
        
        return MotivationAssessment(
            primary_motivation_type=motivation_type,
            autonomy_level=autonomy_level,
            competence_level=competence_level,
            relatedness_level=relatedness_level,
            intrinsic_motivation_threats=intrinsic_threats,
            motivation_sustainability=sustainability,
            recommendations=recommendations
        )
    
    def _determine_motivation_type(self, autonomy: float, competence: float, 
                                 relatedness: float, context: Dict) -> MotivationType:
        """Determine primary motivation type"""
        
        # High autonomy, competence, and relatedness suggest intrinsic motivation
        if autonomy > 0.7 and competence > 0.7 and relatedness > 0.6:
            return MotivationType.INTRINSIC
        
        # High personal importance but external origin
        if context.get("personal_importance", 0) > 0.7:
            return MotivationType.IDENTIFIED
        
        # Some internalization but with pressure
        if context.get("guilt_shame_present", False):
            return MotivationType.INTROJECTED
        
        # Purely external drivers
        if context.get("external_drivers_only", False):
            return MotivationType.EXTERNAL
        
        # Lack of motivation
        if autonomy < 0.3 and competence < 0.3:
            return MotivationType.AMOTIVATED
        
        # Default to identified (moderate internalization)
        return MotivationType.IDENTIFIED
    
    def _generate_recommendations(self, motivation_type: MotivationType,
                                autonomy: float, competence: float, 
                                relatedness: float, threats: List[str]) -> List[str]:
        """Generate motivation support recommendations"""
        recommendations = []
        
        # Autonomy recommendations
        if autonomy < 0.5:
            recommendations.extend([
                "Increase your sense of choice in how you approach tasks",
                "Set some personal goals alongside any external requirements",
                "Find ways to have more control over your work methods"
            ])
        
        # Competence recommendations
        if competence < 0.5:
            recommendations.extend([
                "Break challenging tasks into smaller, achievable steps",
                "Seek feedback to understand your progress and growth",
                "Focus on learning rather than just performing"
            ])
        
        # Relatedness recommendations
        if relatedness < 0.5:
            recommendations.extend([
                "Connect with others who share similar goals or challenges",
                "Consider how your work contributes to something larger",
                "Seek opportunities for collaboration or support"
            ])
        
        # Threat-specific recommendations
        if threats:
            recommendations.append("Consider reducing external pressures that may be undermining your natural motivation")
        
        # Motivation type specific recommendations
        if motivation_type == MotivationType.AMOTIVATED:
            recommendations.extend([
                "Start with very small, achievable actions to rebuild confidence",
                "Reconnect with what originally interested you about this work",
                "Consider whether this work aligns with your values and goals"
            ])
        
        return recommendations


def create_sample_motivation_assessment() -> MotivationAssessment:
    """Create a sample motivation assessment for testing"""
    user_context = {
        "external_deadlines": 2,
        "feels_monitored": False,
        "self_set_goals": 3,
        "imposed_goals": 1,
        "choice_options": 4,
        "competence_feeling": 0.6,
        "connection_feeling": 0.7,
        "personal_importance": 0.8,
        "external_rewards_present": False,
        "monitoring_level": 0.3,
        "time_pressure": 0.4
    }
    
    task_context = {
        "task_type": "creative",
        "required_skills": ["design", "communication"],
        "larger_goal_connection": "Launch new product feature"
    }
    
    assessor = MotivationAssessor()
    return assessor.assess_overall_motivation(user_context, task_context)


if __name__ == "__main__":
    # Example usage
    assessment = create_sample_motivation_assessment()
    print(f"Motivation Type: {assessment.primary_motivation_type.value}")
    print(f"Autonomy Level: {assessment.autonomy_level:.2f}")
    print(f"Competence Level: {assessment.competence_level:.2f}")
    print(f"Relatedness Level: {assessment.relatedness_level:.2f}")
    print(f"Sustainability: {assessment.motivation_sustainability:.2f}")
    print(f"Recommendations: {assessment.recommendations}")

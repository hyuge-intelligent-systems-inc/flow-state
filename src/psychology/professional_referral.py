
"""
FlowState Professional Referral Module

Ethical system for identifying when users need professional mental health support
and connecting them with appropriate licensed professionals while maintaining
clear boundaries about what the app can and cannot provide.

Based on expert analysis emphasizing:
- Clear scope limitations and professional boundaries
- Licensed professional partnerships and oversight
- Crisis detection and management protocols
- User protection and ethical practice standards
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Tuple
from enum import Enum
import logging
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ProfessionalType(Enum):
    """Types of mental health professionals"""
    THERAPIST = "therapist"
    COUNSELOR = "counselor"
    PSYCHOLOGIST = "psychologist"
    PSYCHIATRIST = "psychiatrist"
    COACH = "coach"
    SOCIAL_WORKER = "social_worker"
    SUPPORT_GROUP = "support_group"


class UrgencyLevel(Enum):
    """Urgency levels for professional referral"""
    IMMEDIATE = "immediate"  # Crisis situation
    URGENT = "urgent"  # Within 24-48 hours
    SOON = "soon"  # Within 1-2 weeks
    ROUTINE = "routine"  # When convenient
    OPTIONAL = "optional"  # May be helpful


class ConcernCategory(Enum):
    """Categories of mental health concerns"""
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    ATTENTION = "attention"
    TRAUMA = "trauma"
    STRESS = "stress"
    GRIEF = "grief"
    ADDICTION = "addiction"
    RELATIONSHIP = "relationship"
    WORK_BURNOUT = "work_burnout"
    LIFE_TRANSITION = "life_transition"


class CrisisIndicator(Enum):
    """Indicators of potential crisis situations"""
    SELF_HARM_THOUGHTS = "self_harm_thoughts"
    SUICIDE_IDEATION = "suicide_ideation"
    SEVERE_DEPRESSION = "severe_depression"
    PANIC_ATTACKS = "panic_attacks"
    PSYCHOTIC_SYMPTOMS = "psychotic_symptoms"
    SUBSTANCE_ABUSE = "substance_abuse"
    EXTREME_ISOLATION = "extreme_isolation"


@dataclass
class ReferralCriteria:
    """Criteria that suggest professional help would be beneficial"""
    concern_category: ConcernCategory
    urgency_level: UrgencyLevel
    professional_type: ProfessionalType
    duration_threshold: timedelta  # How long issues should persist
    severity_threshold: float  # 0-1 scale
    description: str
    screening_questions: List[str]


@dataclass
class UserConcernProfile:
    """User's self-reported concerns and patterns"""
    user_id: str
    reported_concerns: List[str]
    concern_duration: Dict[str, timedelta]
    severity_ratings: Dict[str, float]  # 0-1 scale
    impact_on_daily_life: float  # 0-1 scale
    previous_professional_help: bool
    current_professional_help: bool
    support_system_quality: float  # 0-1 scale
    crisis_indicators: List[CrisisIndicator]


@dataclass
class ProfessionalResource:
    """Information about a mental health professional or resource"""
    resource_id: str
    name: str
    professional_type: ProfessionalType
    specialties: List[str]
    location: Optional[str]
    telehealth_available: bool
    insurance_accepted: List[str]
    sliding_scale: bool
    languages: List[str]
    cultural_specializations: List[str]
    contact_info: Dict[str, str]
    verified_credentials: bool


@dataclass
class ReferralRecommendation:
    """Recommendation for professional help"""
    urgency_level: UrgencyLevel
    recommended_professional_types: List[ProfessionalType]
    concern_categories: List[ConcernCategory]
    explanation: str
    immediate_steps: List[str]
    crisis_resources: List[str]
    local_resources: List[ProfessionalResource]
    online_resources: List[str]
    self_care_suggestions: List[str]
    follow_up_timeline: str


class ScopeOfPracticeBoundaries:
    """Defines clear boundaries of what the app can and cannot do"""
    
    def __init__(self):
        self.app_capabilities = [
            "Provide information about mental health resources",
            "Help users identify when professional help might be beneficial",
            "Offer general wellness and productivity support",
            "Connect users with licensed professionals",
            "Provide crisis hotline information"
        ]
        
        self.app_limitations = [
            "Cannot diagnose mental health conditions",
            "Cannot provide therapy or counseling",
            "Cannot prescribe medication",
            "Cannot replace professional mental health care",
            "Cannot provide crisis intervention"
        ]
        
        self.professional_only_activities = [
            "Mental health diagnosis",
            "Therapy and counseling sessions",
            "Medication management",
            "Crisis intervention",
            "Treatment planning",
            "Psychological testing"
        ]
    
    def assess_scope_appropriateness(self, requested_feature: str) -> Dict[str, Union[bool, str]]:
        """Assess whether a feature is within appropriate scope"""
        
        # Check if feature involves professional-only activities
        for activity in self.professional_only_activities:
            if activity.lower() in requested_feature.lower():
                return {
                    "appropriate": False,
                    "reason": f"This involves {activity}, which requires licensed professional",
                    "alternative": "We can help you find appropriate professional support"
                }
        
        # Check if feature aligns with app capabilities
        for capability in self.app_capabilities:
            if any(word in requested_feature.lower() for word in capability.lower().split()):
                return {
                    "appropriate": True,
                    "reason": f"This aligns with our capability to {capability.lower()}",
                    "implementation": "Can be implemented with appropriate safeguards"
                }
        
        return {
            "appropriate": False,
            "reason": "Feature scope unclear or potentially outside our boundaries",
            "recommendation": "Consult with licensed professionals for guidance"
        }
    
    def get_clear_disclaimers(self) -> Dict[str, str]:
        """Get clear disclaimers about app limitations"""
        return {
            "general": "FlowState is a productivity app and not a substitute for professional mental health care.",
            "crisis": "If you are experiencing a mental health crisis, please contact emergency services or a crisis hotline immediately.",
            "diagnosis": "FlowState cannot diagnose mental health conditions. Only licensed professionals can provide diagnosis.",
            "treatment": "Any suggestions provided are for general wellness and should not replace professional treatment.",
            "referral": "Professional referrals are provided for information only and do not constitute endorsement."
        }


class CrisisDetectionSystem:
    """System for detecting potential mental health crises"""
    
    def __init__(self):
        self.crisis_keywords = [
            "suicide", "kill myself", "end it all", "not worth living",
            "hurt myself", "self-harm", "cutting", "overdose",
            "hopeless", "can't go on", "nobody cares", "better off dead"
        ]
        
        self.crisis_patterns = [
            "sudden isolation from all activities",
            "dramatic mood changes",
            "giving away possessions",
            "substance abuse escalation",
            "extreme sleep disruption"
        ]
        
        self.emergency_resources = {
            "us": {
                "suicide_prevention": "988",
                "crisis_text": "Text HOME to 741741",
                "emergency": "911"
            },
            "international": {
                "international_association": "https://www.iasp.info/resources/Crisis_Centres/",
                "befrienders": "https://www.befrienders.org/"
            }
        }
    
    def assess_crisis_risk(self, user_input: str, user_profile: UserConcernProfile) -> Dict[str, Union[bool, str, List[str]]]:
        """Assess if user input indicates potential crisis"""
        
        crisis_indicators = []
        risk_level = "low"
        
        # Check for crisis keywords
        user_text = user_input.lower()
        for keyword in self.crisis_keywords:
            if keyword in user_text:
                crisis_indicators.append(f"Concerning language: {keyword}")
                risk_level = "high"
        
        # Check severity and duration
        if (user_profile.impact_on_daily_life > 0.8 and 
            any(duration > timedelta(weeks=2) for duration in user_profile.concern_duration.values())):
            crisis_indicators.append("Severe impact on daily functioning for extended period")
            risk_level = "moderate" if risk_level == "low" else "high"
        
        # Check for multiple crisis indicators in profile
        if len(user_profile.crisis_indicators) >= 2:
            crisis_indicators.append("Multiple crisis indicators present")
            risk_level = "high"
        
        return {
            "crisis_detected": len(crisis_indicators) > 0,
            "risk_level": risk_level,
            "indicators": crisis_indicators,
            "immediate_action_needed": risk_level == "high"
        }
    
    def get_crisis_response(self, risk_level: str, location: str = "us") -> Dict[str, List[str]]:
        """Get appropriate crisis response resources"""
        
        if risk_level == "high":
            response = {
                "immediate_message": [
                    "It sounds like you're going through a really difficult time.",
                    "Your safety and wellbeing are important.",
                    "Please consider reaching out for immediate professional support."
                ],
                "crisis_resources": [
                    f"Suicide Prevention Lifeline: {self.emergency_resources[location]['suicide_prevention']}",
                    f"Crisis Text Line: {self.emergency_resources[location]['crisis_text']}",
                    "Emergency Services: 911 (if in immediate danger)"
                ],
                "immediate_steps": [
                    "Reach out to a trusted friend, family member, or mental health professional",
                    "Remove any means of self-harm from your immediate environment",
                    "Create a safety plan with specific steps to take when feeling this way",
                    "Consider going to an emergency room if you feel unsafe"
                ]
            }
        else:
            response = {
                "supportive_message": [
                    "It sounds like you're dealing with some difficult challenges.",
                    "Professional support could be really helpful for what you're experiencing.",
                    "You don't have to go through this alone."
                ],
                "resources": [
                    "Consider scheduling an appointment with a mental health professional",
                    "Reach out to trusted friends or family for support",
                    "Look into local mental health resources in your community"
                ]
            }
        
        return response


class ProfessionalResourceDatabase:
    """Database of mental health professionals and resources"""
    
    def __init__(self):
        self.professionals = {}  # In real app, this would be a proper database
        self.resource_categories = {
            "individual_therapy": "One-on-one therapy sessions",
            "group_therapy": "Therapy in a group setting",
            "support_groups": "Peer support groups",
            "psychiatric_care": "Medication management and psychiatric evaluation",
            "crisis_services": "24/7 crisis intervention services",
            "specialized_programs": "Programs for specific conditions or populations"
        }
    
    def add_professional(self, professional: ProfessionalResource):
        """Add a professional to the database"""
        self.professionals[professional.resource_id] = professional
        logger.info(f"Added professional resource: {professional.name}")
    
    def find_professionals(self, 
                          concern_categories: List[ConcernCategory],
                          location: Optional[str] = None,
                          insurance: Optional[str] = None,
                          language: Optional[str] = None,
                          telehealth_only: bool = False) -> List[ProfessionalResource]:
        """Find professionals matching user criteria"""
        
        matching_professionals = []
        
        for professional in self.professionals.values():
            # Check specialties match concerns
            specialty_match = any(
                concern.value in [spec.lower() for spec in professional.specialties]
                for concern in concern_categories
            )
            
            # Check location
            location_match = (
                not location or 
                not professional.location or 
                location.lower() in professional.location.lower() or
                professional.telehealth_available
            )
            
            # Check insurance
            insurance_match = (
                not insurance or
                insurance in professional.insurance_accepted or
                professional.sliding_scale
            )
            
            # Check language
            language_match = (
                not language or
                language in professional.languages
            )
            
            # Check telehealth requirement
            telehealth_match = not telehealth_only or professional.telehealth_available
            
            if all([specialty_match, location_match, insurance_match, language_match, telehealth_match]):
                matching_professionals.append(professional)
        
        return matching_professionals
    
    def get_crisis_resources(self, location: str = "general") -> List[Dict[str, str]]:
        """Get crisis intervention resources"""
        crisis_resources = [
            {
                "name": "National Suicide Prevention Lifeline",
                "contact": "988",
                "description": "24/7 crisis support",
                "type": "phone"
            },
            {
                "name": "Crisis Text Line",
                "contact": "Text HOME to 741741",
                "description": "24/7 text-based crisis support",
                "type": "text"
            },
            {
                "name": "SAMHSA National Helpline",
                "contact": "1-800-662-4357",
                "description": "Treatment referral and information service",
                "type": "phone"
            }
        ]
        
        return crisis_resources


class ReferralRecommendationEngine:
    """Generates professional referral recommendations"""
    
    def __init__(self):
        self.scope_boundaries = ScopeOfPracticeBoundaries()
        self.crisis_detector = CrisisDetectionSystem()
        self.resource_db = ProfessionalResourceDatabase()
        
        # Define referral criteria
        self.referral_criteria = [
            ReferralCriteria(
                concern_category=ConcernCategory.ANXIETY,
                urgency_level=UrgencyLevel.SOON,
                professional_type=ProfessionalType.THERAPIST,
                duration_threshold=timedelta(weeks=2),
                severity_threshold=0.6,
                description="Persistent anxiety affecting daily functioning",
                screening_questions=[
                    "How long have you been experiencing anxiety?",
                    "How much does anxiety interfere with your daily activities?",
                    "Have you had panic attacks or severe anxiety episodes?"
                ]
            ),
            ReferralCriteria(
                concern_category=ConcernCategory.DEPRESSION,
                urgency_level=UrgencyLevel.URGENT,
                professional_type=ProfessionalType.THERAPIST,
                duration_threshold=timedelta(weeks=2),
                severity_threshold=0.7,
                description="Symptoms of depression lasting two weeks or more",
                screening_questions=[
                    "How long have you felt depressed or down?",
                    "Have you lost interest in activities you used to enjoy?",
                    "How is your sleep and appetite?"
                ]
            ),
            ReferralCriteria(
                concern_category=ConcernCategory.ATTENTION,
                urgency_level=UrgencyLevel.ROUTINE,
                professional_type=ProfessionalType.PSYCHOLOGIST,
                duration_threshold=timedelta(weeks=4),
                severity_threshold=0.5,
                description="Persistent attention and focus difficulties",
                screening_questions=[
                    "How long have you had trouble concentrating?",
                    "Do you have difficulty completing tasks?",
                    "Have these problems been present since childhood?"
                ]
            )
        ]
    
    def generate_referral_recommendation(self, 
                                       user_profile: UserConcernProfile,
                                       user_preferences: Dict[str, str]) -> ReferralRecommendation:
        """Generate comprehensive referral recommendation"""
        
        # Check for crisis first
        crisis_assessment = self.crisis_detector.assess_crisis_risk("", user_profile)
        
        if crisis_assessment["crisis_detected"]:
            return self._generate_crisis_referral(crisis_assessment, user_preferences)
        
        # Assess which criteria are met
        met_criteria = self._assess_referral_criteria(user_profile)
        
        if not met_criteria:
            return self._generate_optional_referral(user_profile, user_preferences)
        
        # Determine urgency and professional types
        urgency = max([criteria.urgency_level for criteria in met_criteria], 
                     key=lambda x: list(UrgencyLevel).index(x))
        
        professional_types = list(set([criteria.professional_type for criteria in met_criteria]))
        concern_categories = list(set([criteria.concern_category for criteria in met_criteria]))
        
        # Find matching professionals
        local_resources = self.resource_db.find_professionals(
            concern_categories=concern_categories,
            location=user_preferences.get("location"),
            insurance=user_preferences.get("insurance"),
            language=user_preferences.get("language"),
            telehealth_only=user_preferences.get("telehealth_only", False)
        )
        
        # Generate explanation
        explanation = self._generate_explanation(met_criteria, user_profile)
        
        # Generate immediate steps
        immediate_steps = self._generate_immediate_steps(urgency, concern_categories)
        
        return ReferralRecommendation(
            urgency_level=urgency,
            recommended_professional_types=professional_types,
            concern_categories=concern_categories,
            explanation=explanation,
            immediate_steps=immediate_steps,
            crisis_resources=[],
            local_resources=local_resources,
            online_resources=self._get_online_resources(concern_categories),
            self_care_suggestions=self._get_self_care_suggestions(concern_categories),
            follow_up_timeline=self._get_follow_up_timeline(urgency)
        )
    
    def _assess_referral_criteria(self, user_profile: UserConcernProfile) -> List[ReferralCriteria]:
        """Assess which referral criteria are met"""
        met_criteria = []
        
        for criteria in self.referral_criteria:
            concern_name = criteria.concern_category.value
            
            # Check if user has this concern
            if concern_name not in user_profile.reported_concerns:
                continue
            
            # Check duration
            duration = user_profile.concern_duration.get(concern_name, timedelta(0))
            if duration < criteria.duration_threshold:
                continue
            
            # Check severity
            severity = user_profile.severity_ratings.get(concern_name, 0.0)
            if severity < criteria.severity_threshold:
                continue
            
            met_criteria.append(criteria)
        
        return met_criteria
    
    def _generate_crisis_referral(self, crisis_assessment: Dict, 
                                user_preferences: Dict) -> ReferralRecommendation:
        """Generate referral for crisis situation"""
        crisis_response = self.crisis_detector.get_crisis_response(
            crisis_assessment["risk_level"],
            user_preferences.get("location", "us")
        )
        
        return ReferralRecommendation(
            urgency_level=UrgencyLevel.IMMEDIATE,
            recommended_professional_types=[ProfessionalType.THERAPIST, ProfessionalType.PSYCHIATRIST],
            concern_categories=[ConcernCategory.DEPRESSION],  # Assuming depression for crisis
            explanation="Based on your responses, you may be experiencing a mental health crisis. Immediate professional support is strongly recommended.",
            immediate_steps=crisis_response.get("immediate_steps", []),
            crisis_resources=crisis_response.get("crisis_resources", []),
            local_resources=[],
            online_resources=[],
            self_care_suggestions=[],
            follow_up_timeline="Immediately"
        )
    
    def _generate_optional_referral(self, user_profile: UserConcernProfile,
                                  user_preferences: Dict) -> ReferralRecommendation:
        """Generate optional referral when no criteria met"""
        return ReferralRecommendation(
            urgency_level=UrgencyLevel.OPTIONAL,
            recommended_professional_types=[ProfessionalType.THERAPIST, ProfessionalType.COACH],
            concern_categories=[],
            explanation="While you may not need immediate professional help, talking with a counselor or coach could provide valuable support for personal growth and stress management.",
            immediate_steps=[
                "Consider your goals for personal development",
                "Think about areas where you'd like additional support",
                "Research local mental health resources"
            ],
            crisis_resources=[],
            local_resources=[],
            online_resources=["Psychology Today", "BetterHelp", "Talkspace"],
            self_care_suggestions=[
                "Practice regular stress management techniques",
                "Maintain social connections",
                "Prioritize sleep and physical health"
            ],
            follow_up_timeline="When convenient"
        )
    
    def _generate_explanation(self, criteria: List[ReferralCriteria], 
                            user_profile: UserConcernProfile) -> str:
        """Generate explanation for referral recommendation"""
        if len(criteria) == 1:
            return f"Based on your reports of {criteria[0].concern_category.value}, professional support could be very helpful. {criteria[0].description}"
        else:
            concerns = [c.concern_category.value for c in criteria]
            return f"You've reported experiencing {', '.join(concerns)}, and professional support could help address these concerns effectively."
    
    def _generate_immediate_steps(self, urgency: UrgencyLevel, 
                                concerns: List[ConcernCategory]) -> List[str]:
        """Generate immediate steps based on urgency and concerns"""
        steps = []
        
        if urgency in [UrgencyLevel.URGENT, UrgencyLevel.SOON]:
            steps.extend([
                "Schedule an appointment with a mental health professional within the next week",
                "Reach out to trusted friends or family for support",
                "Consider calling a mental health helpline if you need immediate support"
            ])
        else:
            steps.extend([
                "Research mental health professionals in your area",
                "Consider what type of support would be most helpful",
                "Schedule an initial consultation when you're ready"
            ])
        
        return steps
    
    def _get_online_resources(self, concerns: List[ConcernCategory]) -> List[str]:
        """Get relevant online resources"""
        general_resources = [
            "Psychology Today - Find a therapist",
            "NAMI - National Alliance on Mental Illness",
            "Mental Health America"
        ]
        
        concern_specific = {
            ConcernCategory.ANXIETY: ["Anxiety and Depression Association of America"],
            ConcernCategory.DEPRESSION: ["Depression and Bipolar Support Alliance"],
            ConcernCategory.ATTENTION: ["CHADD - Children and Adults with ADHD"]
        }
        
        specific_resources = []
        for concern in concerns:
            specific_resources.extend(concern_specific.get(concern, []))
        
        return general_resources + specific_resources
    
    def _get_self_care_suggestions(self, concerns: List[ConcernCategory]) -> List[str]:
        """Get self-care suggestions while seeking professional help"""
        general_suggestions = [
            "Maintain regular sleep schedule",
            "Stay connected with supportive friends and family",
            "Engage in regular physical activity",
            "Practice stress management techniques"
        ]
        
        return general_suggestions
    
    def _get_follow_up_timeline(self, urgency: UrgencyLevel) -> str:
        """Get appropriate follow-up timeline"""
        timelines = {
            UrgencyLevel.IMMEDIATE: "Immediately",
            UrgencyLevel.URGENT: "Within 24-48 hours",
            UrgencyLevel.SOON: "Within 1-2 weeks",
            UrgencyLevel.ROUTINE: "Within 1-2 months",
            UrgencyLevel.OPTIONAL: "When convenient"
        }
        
        return timelines.get(urgency, "When convenient")


def create_sample_referral() -> ReferralRecommendation:
    """Create a sample referral recommendation for testing"""
    user_profile = UserConcernProfile(
        user_id="sample_user",
        reported_concerns=["anxiety", "stress"],
        concern_duration={"anxiety": timedelta(weeks=4), "stress": timedelta(weeks=6)},
        severity_ratings={"anxiety": 0.7, "stress": 0.6},
        impact_on_daily_life=0.6,
        previous_professional_help=False,
        current_professional_help=False,
        support_system_quality=0.5,
        crisis_indicators=[]
    )
    
    user_preferences = {
        "location": "New York",
        "insurance": "Blue Cross",
        "language": "English",
        "telehealth_only": False
    }
    
    engine = ReferralRecommendationEngine()
    return engine.generate_referral_recommendation(user_profile, user_preferences)


if __name__ == "__main__":
    # Example usage
    recommendation = create_sample_referral()
    print(f"Urgency: {recommendation.urgency_level.value}")
    print(f"Recommended professionals: {[p.value for p in recommendation.recommended_professional_types]}")
    print(f"Explanation: {recommendation.explanation}")
    print(f"Immediate steps: {recommendation.immediate_steps}")

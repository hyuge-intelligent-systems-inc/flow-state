

"""
FlowState Self-Discovery Psychology Module
Based on expert analysis: Ethical psychology support with professional boundaries

Key principles implemented:
- No psychological diagnosis or assessment by AI
- User-controlled self-reflection and discovery
- Professional referral when appropriate
- Transparent limitations and ethical boundaries
- Collaborative exploration, not AI judgment
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from ..core.pattern_analyzer import PatternInsight, ConfidenceLevel


class SupportLevel(Enum):
    """Levels of support complexity user can choose"""
    MINIMAL = "minimal"
    GUIDED = "guided"
    STRUCTURED = "structured"
    PROFESSIONAL_REFERRAL = "professional_referral"


class ReflectionCategory(Enum):
    """Categories for self-reflection"""
    PRODUCTIVITY_PATTERNS = "productivity_patterns"
    ENERGY_AWARENESS = "energy_awareness"
    MOTIVATION_UNDERSTANDING = "motivation_understanding"
    OBSTACLE_RECOGNITION = "obstacle_recognition"
    VALUES_ALIGNMENT = "values_alignment"
    GOAL_CLARITY = "goal_clarity"


@dataclass
class ReflectionPrompt:
    """Self-reflection prompt with user control"""
    category: ReflectionCategory
    question: str
    follow_up_questions: List[str]
    guidance_notes: str
    professional_boundary: str
    user_controlled: bool = True


@dataclass
class SelfDiscoverySession:
    """User-led self-discovery session"""
    session_id: str
    date: datetime
    category: ReflectionCategory
    user_responses: Dict[str, str]
    insights_noted: List[str]
    questions_raised: List[str]
    next_exploration_areas: List[str]
    professional_referral_needed: bool = False


class ProfessionalReferralAssessment:
    """Ethical assessment for professional support needs"""
    
    @staticmethod
    def assess_referral_indicators(user_responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify when professional support might be helpful
        Based on user self-reporting, not AI diagnosis
        """
        referral_indicators = {
            "complexity_level": "manageable",
            "duration_of_challenges": "short_term",
            "impact_on_daily_life": "minimal",
            "professional_support_recommended": False,
            "referral_urgency": "none",
            "user_expressed_interest": False
        }
        
        # Check for user-expressed interest in professional support
        if user_responses.get("interested_in_professional_help", False):
            referral_indicators["user_expressed_interest"] = True
            referral_indicators["professional_support_recommended"] = True
        
        # Check for self-reported complexity
        if user_responses.get("challenge_complexity", "") in ["very_complex", "overwhelming"]:
            referral_indicators["complexity_level"] = "high"
            referral_indicators["professional_support_recommended"] = True
        
        # Check for duration indicators
        duration = user_responses.get("challenge_duration", "")
        if duration in ["months", "years", "ongoing"]:
            referral_indicators["duration_of_challenges"] = "long_term"
            referral_indicators["professional_support_recommended"] = True
        
        # Check for impact level
        impact = user_responses.get("daily_life_impact", "")
        if impact in ["significant", "severe", "interfering"]:
            referral_indicators["impact_on_daily_life"] = "high"
            referral_indicators["professional_support_recommended"] = True
            referral_indicators["referral_urgency"] = "recommended"
        
        return referral_indicators


class SelfDiscoveryGuide:
    """
    Ethical self-discovery guide that empowers users to understand
    themselves without AI making psychological judgments
    """
    
    def __init__(self):
        self.professional_boundaries = {
            "scope": "Self-reflection support only, not psychological assessment",
            "limitations": "Cannot diagnose, treat, or provide therapy",
            "referral_threshold": "When users request or challenges exceed self-help scope",
            "data_use": "User controls all personal insights and interpretations"
        }
        
        self.reflection_prompts = self._initialize_reflection_prompts()
        self.discovery_sessions: List[SelfDiscoverySession] = []
    
    def _initialize_reflection_prompts(self) -> Dict[ReflectionCategory, List[ReflectionPrompt]]:
        """Initialize ethical self-reflection prompts"""
        return {
            ReflectionCategory.PRODUCTIVITY_PATTERNS: [
                ReflectionPrompt(
                    category=ReflectionCategory.PRODUCTIVITY_PATTERNS,
                    question="When you look at your productivity data, what patterns do you notice?",
                    follow_up_questions=[
                        "Which patterns feel natural to you?",
                        "Which patterns surprise you?",
                        "What might be causing the patterns you see?"
                    ],
                    guidance_notes="Focus on your own observations and feelings about the data",
                    professional_boundary="This is pattern observation, not psychological assessment"
                ),
                ReflectionPrompt(
                    category=ReflectionCategory.PRODUCTIVITY_PATTERNS,
                    question="How do external factors (sleep, stress, environment) seem to affect your productivity?",
                    follow_up_questions=[
                        "What external factors have the biggest impact?",
                        "Which factors can you influence?",
                        "Which factors are outside your control?"
                    ],
                    guidance_notes="Consider the full context of your life and work",
                    professional_boundary="Environmental factors may require practical, not psychological solutions"
                )
            ],
            
            ReflectionCategory.ENERGY_AWARENESS: [
                ReflectionPrompt(
                    category=ReflectionCategory.ENERGY_AWARENESS,
                    question="When do you naturally feel most energized and focused?",
                    follow_up_questions=[
                        "What activities give you energy vs. drain your energy?",
                        "How does your energy change throughout the day/week?",
                        "What helps you restore energy when it's low?"
                    ],
                    guidance_notes="Pay attention to your body's natural rhythms and signals",
                    professional_boundary="Persistent low energy may indicate health issues requiring medical consultation"
                ),
                ReflectionPrompt(
                    category=ReflectionCategory.ENERGY_AWARENESS,
                    question="How do you currently manage your energy throughout the day?",
                    follow_up_questions=[
                        "What energy management strategies work well for you?",
                        "What strategies have you tried that didn't work?",
                        "How do you balance energy-giving and energy-draining activities?"
                    ],
                    guidance_notes="Focus on practical strategies that fit your lifestyle",
                    professional_boundary="Chronic fatigue or energy issues may require medical evaluation"
                )
            ],
            
            ReflectionCategory.MOTIVATION_UNDERSTANDING: [
                ReflectionPrompt(
                    category=ReflectionCategory.MOTIVATION_UNDERSTANDING,
                    question="What types of work or activities naturally motivate you?",
                    follow_up_questions=[
                        "What makes certain tasks feel engaging vs. boring?",
                        "How does your motivation change based on the task, environment, or time?",
                        "What external factors help or hurt your motivation?"
                    ],
                    guidance_notes="Notice what genuinely interests and engages you",
                    professional_boundary="Persistent lack of motivation may indicate underlying issues requiring professional support"
                ),
                ReflectionPrompt(
                    category=ReflectionCategory.MOTIVATION_UNDERSTANDING,
                    question="How do you currently maintain motivation for important but challenging tasks?",
                    follow_up_questions=[
                        "What motivation strategies work best for you?",
                        "How do you handle tasks you don't enjoy but need to complete?",
                        "What role do goals, deadlines, and accountability play in your motivation?"
                    ],
                    guidance_notes="Reflect on your personal motivation patterns and preferences",
                    professional_boundary="Severe motivational challenges may require professional evaluation"
                )
            ],
            
            ReflectionCategory.OBSTACLE_RECOGNITION: [
                ReflectionPrompt(
                    category=ReflectionCategory.OBSTACLE_RECOGNITION,
                    question="What are the biggest obstacles to your productivity and well-being?",
                    follow_up_questions=[
                        "Which obstacles are within your control to change?",
                        "Which obstacles require external changes or support?",
                        "How do you currently cope with these obstacles?"
                    ],
                    guidance_notes="Distinguish between individual and systemic challenges",
                    professional_boundary="Some obstacles may require organizational, medical, or professional intervention"
                ),
                ReflectionPrompt(
                    category=ReflectionCategory.OBSTACLE_RECOGNITION,
                    question="When you avoid tasks or procrastinate, what usually happens?",
                    follow_up_questions=[
                        "What types of tasks do you tend to avoid?",
                        "What feelings or thoughts come up when you're avoiding something?",
                        "What helps you get back on track when you're stuck?"
                    ],
                    guidance_notes="Observe your patterns without judgment",
                    professional_boundary="Severe procrastination or avoidance may indicate anxiety, ADHD, or other conditions requiring professional assessment"
                )
            ],
            
            ReflectionCategory.VALUES_ALIGNMENT: [
                ReflectionPrompt(
                    category=ReflectionCategory.VALUES_ALIGNMENT,
                    question="How well does your current work align with what's important to you?",
                    follow_up_questions=[
                        "What values are most important to you in your work and life?",
                        "Where do you see alignment between your values and current activities?",
                        "Where do you notice misalignment?"
                    ],
                    guidance_notes="Consider your authentic values, not what you think you should value",
                    professional_boundary="Major life transitions and value conflicts may benefit from professional coaching or counseling"
                )
            ],
            
            ReflectionCategory.GOAL_CLARITY: [
                ReflectionPrompt(
                    category=ReflectionCategory.GOAL_CLARITY,
                    question="How clear are you about what you want to achieve in the short and long term?",
                    follow_up_questions=[
                        "Which goals feel truly important to you vs. imposed by others?",
                        "How do your daily activities connect to your larger goals?",
                        "What makes it easy or difficult to work toward your goals?"
                    ],
                    guidance_notes="Focus on goals that genuinely matter to you",
                    professional_boundary="Major life direction questions may benefit from professional coaching"
                )
            ]
        }
    
    def start_discovery_session(self, category: ReflectionCategory, 
                              support_level: SupportLevel = SupportLevel.GUIDED) -> str:
        """
        Start a user-controlled self-discovery session
        
        Args:
            category: Area of self-reflection
            support_level: Level of guidance user wants
            
        Returns:
            str: Session ID for tracking
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = SelfDiscoverySession(
            session_id=session_id,
            date=datetime.now(),
            category=category,
            user_responses={},
            insights_noted=[],
            questions_raised=[],
            next_exploration_areas=[]
        )
        
        self.discovery_sessions.append(session)
        return session_id
    
    def get_reflection_prompts(self, category: ReflectionCategory, 
                             support_level: SupportLevel) -> List[ReflectionPrompt]:
        """
        Get reflection prompts based on user's chosen category and support level
        """
        base_prompts = self.reflection_prompts.get(category, [])
        
        if support_level == SupportLevel.MINIMAL:
            return base_prompts[:1]  # Just basic prompts
        elif support_level == SupportLevel.GUIDED:
            return base_prompts[:2]  # More structured guidance
        else:  # STRUCTURED
            return base_prompts  # Full prompts with follow-ups
    
    def record_user_response(self, session_id: str, prompt_id: str, 
                           response: str) -> bool:
        """
        Record user's self-reflection response
        
        Args:
            session_id: Session identifier
            prompt_id: Prompt identifier
            response: User's response
            
        Returns:
            bool: Success status
        """
        session = self._find_session(session_id)
        if not session:
            return False
        
        session.user_responses[prompt_id] = response
        return True
    
    def add_user_insight(self, session_id: str, insight: str) -> bool:
        """
        Add user's own insight from reflection
        """
        session = self._find_session(session_id)
        if not session:
            return False
        
        session.insights_noted.append(insight)
        return True
    
    def add_user_question(self, session_id: str, question: str) -> bool:
        """
        Add question that arose during user's reflection
        """
        session = self._find_session(session_id)
        if not session:
            return False
        
        session.questions_raised.append(question)
        return True
    
    def suggest_next_exploration(self, session_id: str, 
                               current_insights: List[str]) -> List[str]:
        """
        Suggest areas for further self-exploration based on user's insights
        """
        session = self._find_session(session_id)
        if not session:
            return []
        
        suggestions = []
        
        # Based on user's own insights, suggest related areas to explore
        for insight in current_insights:
            if "energy" in insight.lower():
                suggestions.append("Explore your energy patterns in more detail")
            if "motivation" in insight.lower():
                suggestions.append("Examine what drives your motivation")
            if "stress" in insight.lower() or "overwhelm" in insight.lower():
                suggestions.append("Consider stress management strategies")
            if "time" in insight.lower():
                suggestions.append("Look at your relationship with time and deadlines")
        
        # Add general exploration suggestions
        suggestions.extend([
            "Try a personal productivity experiment based on your insights",
            "Discuss your observations with a trusted friend or colleague",
            "Keep a brief daily reflection journal for a week"
        ])
        
        session.next_exploration_areas = suggestions
        return suggestions
    
    def assess_professional_support_needs(self, session_id: str) -> Dict[str, Any]:
        """
        Assess if professional support might be helpful based on user responses
        """
        session = self._find_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        # Compile user responses for assessment
        assessment_data = {
            "user_responses": session.user_responses,
            "insights_noted": session.insights_noted,
            "questions_raised": session.questions_raised,
            "session_category": session.category.value
        }
        
        # Use ethical referral assessment
        referral_assessment = ProfessionalReferralAssessment.assess_referral_indicators(
            session.user_responses
        )
        
        if referral_assessment["professional_support_recommended"]:
            session.professional_referral_needed = True
        
        return {
            "assessment": referral_assessment,
            "referral_resources": self._get_referral_resources(referral_assessment),
            "important_note": "This assessment is based on your self-reported information, not professional diagnosis"
        }
    
    def _get_referral_resources(self, assessment: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Provide appropriate professional referral resources
        """
        resources = {
            "general_support": [
                "Licensed counselors or therapists for general life challenges",
                "Certified life coaches for goal-setting and motivation support",
                "Employee assistance programs if available through your workplace"
            ],
            "specific_areas": [],
            "crisis_resources": [
                "Crisis hotlines if you're experiencing thoughts of self-harm",
                "Emergency services (911) for immediate safety concerns"
            ]
        }
        
        if assessment.get("complexity_level") == "high":
            resources["specific_areas"].extend([
                "Psychologists for comprehensive assessment and treatment",
                "Psychiatrists if medication evaluation might be helpful"
            ])
        
        if assessment.get("duration_of_challenges") == "long_term":
            resources["specific_areas"].extend([
                "Therapists specializing in cognitive-behavioral therapy",
                "Support groups for ongoing challenges"
            ])
        
        return resources
    
    def _find_session(self, session_id: str) -> Optional[SelfDiscoverySession]:
        """Find session by ID"""
        for session in self.discovery_sessions:
            if session.session_id == session_id:
                return session
        return None
    
    def export_discovery_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Export user's self-discovery summary with full user control
        """
        session = self._find_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        return {
            "session_id": session_id,
            "date": session.date.isoformat(),
            "category": session.category.value,
            "your_responses": session.user_responses,
            "your_insights": session.insights_noted,
            "your_questions": session.questions_raised,
            "suggested_next_steps": session.next_exploration_areas,
            "professional_support_considered": session.professional_referral_needed,
            "important_notes": {
                "data_ownership": "This data belongs entirely to you",
                "privacy": "You control who sees this information",
                "limitations": "This is self-reflection, not professional assessment",
                "next_steps": "You decide how to use these insights"
            },
            "professional_boundaries": self.professional_boundaries
        }
    
    def get_user_controlled_insights(self, pattern_data: Dict[str, PatternInsight]) -> Dict[str, Any]:
        """
        Help users explore their patterns with self-discovery questions
        """
        exploration_questions = []
        
        for pattern_name, pattern in pattern_data.items():
            if pattern.confidence != ConfidenceLevel.UNCERTAIN:
                exploration_questions.extend([
                    f"What do you think about this {pattern_name} pattern?",
                    f"Does this {pattern_name} pattern feel accurate to your experience?",
                    f"What might be causing this {pattern_name} pattern?",
                    f"How might you use this {pattern_name} information?"
                ])
        
        return {
            "pattern_exploration_questions": exploration_questions,
            "self_reflection_guidance": [
                "Take time to consider what these patterns mean to you",
                "Think about whether the patterns align with your experience",
                "Consider what external factors might influence these patterns",
                "Decide which patterns are worth exploring further"
            ],
            "user_control_notes": [
                "You are the expert on your own productivity",
                "These patterns are observations, not prescriptions",
                "You decide what to do with this information",
                "Professional support is available if you want additional perspectives"
            ]
        }
    
    def clear_user_data(self, user_confirmation: bool = False) -> bool:
        """
        Clear all user data with explicit confirmation
        """
        if not user_confirmation:
            return False
        
        self.discovery_sessions.clear()
        return True


# Example usage and testing
if __name__ == "__main__":
    # Create self-discovery guide
    guide = SelfDiscoveryGuide()
    
    # Start a discovery session
    session_id = guide.start_discovery_session(
        category=ReflectionCategory.PRODUCTIVITY_PATTERNS,
        support_level=SupportLevel.GUIDED
    )
    
    print(f"Started session: {session_id}")
    
    # Get prompts for user
    prompts = guide.get_reflection_prompts(
        ReflectionCategory.PRODUCTIVITY_PATTERNS,
        SupportLevel.GUIDED
    )
    
    print("\nSelf-reflection prompts:")
    for i, prompt in enumerate(prompts):
        print(f"{i+1}. {prompt.question}")
        print(f"   Guidance: {prompt.guidance_notes}")
        print(f"   Boundary: {prompt.professional_boundary}\n")
    
    # Example: user records insight
    guide.add_user_insight(session_id, "I notice I'm most productive in the morning when I haven't checked email yet")
    
    # Get exploration suggestions
    suggestions = guide.suggest_next_exploration(session_id, 
        ["I work better with fewer interruptions"])
    
    print("Suggested exploration areas:")
    for suggestion in suggestions:
        print(f"- {suggestion}")
    
    # Export user's discovery summary
    summary = guide.export_discovery_summary(session_id)
    print("\nUser Discovery Summary:")
    print(json.dumps(summary, indent=2))

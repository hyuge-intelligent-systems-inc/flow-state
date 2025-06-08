

"""
FlowState Core Productivity Engine
Orchestrates all modules with user agency and realistic limitations

Key principles implemented:
- User agency preserved across all interactions
- Honest limitations and graceful degradation
- Evidence-based recommendations with transparency
- Individual differences accommodation
- Systemic problem recognition
- Progressive complexity based on user engagement
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from .time_tracker import TimeTracker, TimeEntry, ConfidenceLevel
from .pattern_analyzer import PatternAnalyzer, PatternInsight
from ..psychology.self_discovery import SelfDiscoveryGuide, ReflectionCategory, SupportLevel
from ..ai.honest_tracking import HonestAITracker, AIPrediction, AIInsight
from ..ui.progressive_complexity import ProgressiveComplexityManager, ComplexityLevel
from ..workplace.team_optimization import TeamOptimizer, SharingLevel, TeamRole


class ProductivityMode(Enum):
    """Different productivity support modes based on user needs"""
    SURVIVAL = "survival"           # Essential tasks only, minimal cognitive load
    MAINTENANCE = "maintenance"     # Keeping up with regular responsibilities  
    GROWTH = "growth"               # Actively improving and optimizing
    MASTERY = "mastery"            # Advanced productivity practices and teaching others


class SystemStatus(Enum):
    """Overall system health and reliability"""
    OPTIMAL = "optimal"
    GOOD = "good"
    DEGRADED = "degraded"
    MINIMAL = "minimal"


@dataclass
class ProductivityRecommendation:
    """A productivity recommendation with full transparency"""
    recommendation_id: str
    title: str
    description: str
    rationale: str
    confidence: ConfidenceLevel
    source_module: str
    user_control: str  # How user can accept/modify/reject
    evidence: List[str]
    limitations: str
    alternative_approaches: List[str]
    estimated_impact: str
    effort_required: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProductivityInsight:
    """Aggregated insight from multiple sources"""
    insight_id: str
    insight_type: str
    summary: str
    confidence: ConfidenceLevel
    supporting_sources: List[str]
    contradicting_sources: List[str]
    user_interpretation_guidance: str
    next_steps: List[str]
    professional_referral_suggested: bool = False


class ProductivityEngine:
    """
    Core orchestrator that integrates all FlowState modules while
    preserving user agency and providing honest limitations
    """
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        
        # Initialize all modules
        self.time_tracker = TimeTracker(user_id)
        self.pattern_analyzer = PatternAnalyzer()
        self.self_discovery = SelfDiscoveryGuide()
        self.ai_tracker = HonestAITracker(user_id)
        self.ui_manager = ProgressiveComplexityManager(user_id)
        self.team_optimizer = TeamOptimizer()
        
        # System state
        self.current_mode = ProductivityMode.GROWTH
        self.system_status = SystemStatus.OPTIMAL
        self.user_preferences = self._initialize_user_preferences()
        self.active_recommendations: List[ProductivityRecommendation] = []
        self.user_feedback_history: List[Dict] = []
        
        # Integration settings
        self.module_weights = {
            "time_tracker": 1.0,      # Always trusted
            "pattern_analyzer": 0.8,   # High trust for user-interpreted patterns
            "ai_tracker": 0.6,         # Moderate trust for AI suggestions
            "self_discovery": 0.9,     # High trust for user insights
            "team_optimizer": 0.7      # Good trust for team insights
        }
        
    def _initialize_user_preferences(self) -> Dict[str, Any]:
        """Initialize user preferences with sensible defaults"""
        return {
            "productivity_philosophy": "balanced",  # balanced, efficiency_focused, well_being_focused
            "ai_assistance_level": "moderate",      # minimal, moderate, maximum
            "complexity_preference": "earned",      # minimal, earned, immediate
            "feedback_frequency": "weekly",         # daily, weekly, monthly
            "systemic_vs_individual_focus": "balanced",  # individual, balanced, systemic
            "privacy_level": "moderate",            # high, moderate, collaborative
            "intervention_style": "gentle",         # minimal, gentle, proactive
            "goal_orientation": "improvement",      # maintenance, improvement, optimization
        }
    
    def start_productivity_session(self, task_description: str = "", 
                                 category: str = "work", 
                                 estimated_minutes: Optional[int] = None,
                                 context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Start a productivity session with intelligent support
        
        Args:
            task_description: What the user plans to work on
            category: Task category
            estimated_minutes: User's time estimate
            context: Additional context (energy level, goals, etc.)
            
        Returns:
            Session start confirmation with supportive guidance
        """
        # Start core time tracking
        entry = self.time_tracker.start_timer(task_description, category, estimated_minutes)
        
        # Generate supportive guidance based on available data
        guidance = self._generate_session_guidance(task_description, category, context or {})
        
        # Update UI based on session start
        ui_config = self.ui_manager.get_current_ui_config()
        
        # Record session start for learning
        self._record_session_event("session_started", {
            "task": task_description,
            "category": category,
            "estimated_duration": estimated_minutes,
            "guidance_provided": len(guidance.get("suggestions", []))
        })
        
        return {
            "session_started": True,
            "entry_id": entry.start_time.isoformat(),
            "guidance": guidance,
            "ui_config": ui_config,
            "user_control": {
                "modify_estimate": "Available anytime during session",
                "change_category": "Available anytime",
                "disable_guidance": "All suggestions can be ignored",
                "stop_early": "No minimum session length required"
            },
            "system_status": self.system_status.value
        }
    
    def _generate_session_guidance(self, task_description: str, category: str, 
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate helpful session guidance from multiple sources"""
        guidance = {
            "suggestions": [],
            "insights": [],
            "warnings": [],
            "confidence_notes": []
        }
        
        # Get AI suggestions if user wants them
        if self.user_preferences.get("ai_assistance_level") != "minimal":
            ai_prediction = self.ai_tracker.predict_optimal_work_time(
                self.time_tracker.entries, datetime.now()
            )
            
            if ai_prediction and ai_prediction.confidence != ConfidenceLevel.UNCERTAIN:
                guidance["suggestions"].append({
                    "source": "AI analysis",
                    "suggestion": ai_prediction.reasoning,
                    "confidence": ai_prediction.confidence.value,
                    "user_control": "You can ignore this suggestion"
                })
        
        # Get duration suggestion based on historical data
        if len(self.time_tracker.entries) >= 5:
            similar_tasks = [
                e for e in self.time_tracker.entries 
                if e.category == category and e.is_complete()
            ]
            
            if len(similar_tasks) >= 3:
                durations = [e.duration_minutes() for e in similar_tasks if e.duration_minutes()]
                if durations:
                    avg_duration = sum(durations) / len(durations)
                    guidance["insights"].append({
                        "source": "Your historical data",
                        "insight": f"Your {category} tasks typically take {avg_duration:.0f} minutes",
                        "confidence": "moderate",
                        "sample_size": len(durations)
                    })
        
        # Check for potential issues
        current_hour = datetime.now().hour
        if current_hour >= 18 and context.get("energy_level", 3) < 3:
            guidance["warnings"].append({
                "source": "Time and energy awareness",
                "warning": "Late day work with low energy - consider shorter session or easier tasks",
                "suggestion": "This is just a gentle reminder - you know your situation best"
            })
        
        # Add confidence notes about guidance quality
        if len(self.time_tracker.entries) < 10:
            guidance["confidence_notes"].append(
                "Guidance will improve as you use FlowState more - early suggestions are limited"
            )
        
        return guidance
    
    def end_productivity_session(self, user_notes: str = "", energy_level: int = 3,
                               focus_quality: int = 3, interruptions: int = 0,
                               satisfaction: int = 3) -> Dict[str, Any]:
        """
        End productivity session with comprehensive wrap-up
        
        Args:
            user_notes: User's reflection on the session
            energy_level: Self-reported energy (1-5)
            focus_quality: Self-reported focus (1-5)
            interruptions: Number of interruptions
            satisfaction: Session satisfaction (1-5)
            
        Returns:
            Session summary with insights and next steps
        """
        # End time tracking
        completed_entry = self.time_tracker.stop_timer(
            user_notes, energy_level, focus_quality, interruptions
        )
        
        if not completed_entry:
            return {"error": "No active session to end"}
        
        # Generate session analysis
        session_analysis = self._analyze_completed_session(completed_entry, satisfaction)
        
        # Update patterns if enough data
        if len(self.time_tracker.entries) >= 5:
            patterns = self.pattern_analyzer.analyze_time_patterns(
                self.time_tracker.entries, timeframe_days=30
            )
            session_analysis["patterns_updated"] = len(patterns)
        
        # Check for UI progression
        usage_data = self._get_usage_data_for_ui()
        metrics = self.ui_manager.calculate_usage_metrics(usage_data)
        eligible_features = self.ui_manager.check_unlock_eligibility(metrics)
        
        if eligible_features:
            unlocked = self.ui_manager.unlock_features(eligible_features)
            session_analysis["features_unlocked"] = unlocked
        
        # Generate recommendations for next session
        next_session_recs = self._generate_next_session_recommendations(completed_entry)
        session_analysis["next_session_recommendations"] = next_session_recs
        
        # Record session completion
        self._record_session_event("session_completed", {
            "duration": completed_entry.duration_minutes(),
            "satisfaction": satisfaction,
            "focus_quality": focus_quality,
            "energy_level": energy_level,
            "interruptions": interruptions
        })
        
        return session_analysis
    
    def _analyze_completed_session(self, entry: TimeEntry, satisfaction: int) -> Dict[str, Any]:
        """Analyze completed session for insights"""
        analysis = {
            "session_summary": {
                "task": entry.task_description,
                "category": entry.category,
                "duration_minutes": entry.duration_minutes(),
                "focus_quality": entry.focus_quality,
                "energy_level": entry.energy_level,
                "interruptions": entry.interruptions,
                "satisfaction": satisfaction
            },
            "insights": [],
            "areas_for_reflection": [],
            "positive_observations": []
        }
        
        # Analyze session quality
        if entry.focus_quality >= 4 and entry.energy_level >= 4:
            analysis["positive_observations"].append(
                "High focus and energy - great conditions for productive work"
            )
        
        if entry.interruptions == 0:
            analysis["positive_observations"].append(
                "Uninterrupted session - protected focus time was successful"
            )
        
        if satisfaction >= 4:
            analysis["positive_observations"].append(
                "High satisfaction with session - approach is working well"
            )
        
        # Identify areas for reflection
        if entry.focus_quality <= 2:
            analysis["areas_for_reflection"].append(
                "Low focus quality - what factors might have contributed?"
            )
        
        if entry.interruptions >= 5:
            analysis["areas_for_reflection"].append(
                "High interruption count - are there patterns or sources to address?"
            )
        
        if satisfaction <= 2:
            analysis["areas_for_reflection"].append(
                "Low satisfaction - what would make work sessions more satisfying?"
            )
        
        return analysis
    
    def get_daily_productivity_summary(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Generate comprehensive daily productivity summary
        
        Args:
            date: Date to summarize (defaults to today)
            
        Returns:
            Multi-module productivity summary with insights
        """
        if date is None:
            date = datetime.now()
        
        # Get core time tracking summary
        daily_summary = self.time_tracker.get_daily_summary(date)
        
        # Add pattern insights if available
        if len(self.time_tracker.entries) >= 10:
            patterns = self.pattern_analyzer.analyze_time_patterns(
                self.time_tracker.entries, timeframe_days=7
            )
            daily_summary["pattern_insights"] = {
                name: {
                    "description": pattern.description,
                    "confidence": pattern.confidence.value,
                    "user_interpretation_needed": pattern.user_interpretation_needed
                }
                for name, pattern in patterns.items()
            }
        
        # Add AI insights if user wants them
        if self.user_preferences.get("ai_assistance_level") != "minimal":
            ai_insights = self.ai_tracker.analyze_productivity_patterns(self.time_tracker.entries)
            daily_summary["ai_insights"] = [
                {
                    "description": insight.description,
                    "confidence": insight.confidence.value,
                    "limitations": insight.limitations,
                    "supporting_evidence": insight.supporting_evidence[:2],  # Limit for readability
                }
                for insight in ai_insights[:3]  # Top 3 insights only
            ]
        
        # Add self-discovery prompts
        if len(self.time_tracker.entries) >= 5:
            reflection_prompts = self._generate_daily_reflection_prompts(daily_summary)
            daily_summary["reflection_opportunities"] = reflection_prompts
        
        # Add system health and recommendations
        daily_summary["system_status"] = self._assess_system_health()
        daily_summary["recommendations"] = self._generate_daily_recommendations(daily_summary)
        
        return daily_summary
    
    def _generate_daily_reflection_prompts(self, daily_summary: Dict[str, Any]) -> List[str]:
        """Generate thoughtful reflection prompts based on daily data"""
        prompts = []
        
        # Based on productivity level
        if daily_summary.get("total_minutes", 0) > 0:
            prompts.append("What contributed to your productivity today?")
            
            if daily_summary.get("average_focus", 0) >= 4:
                prompts.append("Your focus was high today - what conditions supported that?")
            elif daily_summary.get("average_focus", 0) <= 2:
                prompts.append("Focus was challenging today - what factors might have influenced that?")
        
        # Based on interruptions
        if daily_summary.get("total_interruptions", 0) > 10:
            prompts.append("You had many interruptions today - are there patterns or sources to consider?")
        
        # Based on energy
        if daily_summary.get("average_energy", 0) >= 4:
            prompts.append("Your energy was good today - what supported that?")
        elif daily_summary.get("average_energy", 0) <= 2:
            prompts.append("Energy was low today - what might help restore it?")
        
        # General reflection
        prompts.append("What did you learn about your work patterns today?")
        
        return prompts[:3]  # Limit to avoid overwhelm
    
    def _generate_daily_recommendations(self, daily_summary: Dict[str, Any]) -> List[ProductivityRecommendation]:
        """Generate evidence-based daily recommendations"""
        recommendations = []
        
        # Recommendation based on estimation accuracy
        estimation_accuracy = self.time_tracker.get_estimation_accuracy()
        if (estimation_accuracy.get("accuracy") == "needs_improvement" and 
            estimation_accuracy.get("sample_size", 0) >= 5):
            
            recommendations.append(ProductivityRecommendation(
                recommendation_id=f"estimation_improvement_{datetime.now().strftime('%Y%m%d')}",
                title="Time Estimation Practice",
                description="Consider tracking your time estimates vs. actual time to improve planning",
                rationale=f"Your current estimation accuracy could be improved (avg error: {estimation_accuracy.get('average_error_percent', 0):.0f}%)",
                confidence=ConfidenceLevel.MODERATE,
                source_module="time_tracker",
                user_control="You can ignore this or try it for just a few tasks",
                evidence=[f"Based on {estimation_accuracy.get('sample_size')} completed tasks"],
                limitations="Estimation accuracy varies by task type and external factors",
                alternative_approaches=[
                    "Focus on task completion rather than time estimation",
                    "Use time ranges instead of specific estimates",
                    "Break large tasks into smaller, more predictable pieces"
                ],
                estimated_impact="Better planning and reduced time pressure",
                effort_required="Low - just note estimates before starting tasks"
            ))
        
        # Recommendation based on focus quality patterns
        if daily_summary.get("average_focus", 0) < 3 and daily_summary.get("total_interruptions", 0) > 8:
            recommendations.append(ProductivityRecommendation(
                recommendation_id=f"focus_protection_{datetime.now().strftime('%Y%m%d')}",
                title="Focus Protection Experiment",
                description="Try protecting one work session from interruptions tomorrow",
                rationale="Today's data suggests interruptions may be affecting focus quality",
                confidence=ConfidenceLevel.LOW,  # Honest about correlation vs causation
                source_module="pattern_analyzer",
                user_control="This is just a suggestion - experiment if it interests you",
                evidence=[
                    f"Focus quality: {daily_summary.get('average_focus', 0):.1f}/5",
                    f"Interruptions: {daily_summary.get('total_interruptions', 0)}"
                ],
                limitations="Correlation between interruptions and focus, causation not established",
                alternative_approaches=[
                    "Accept interruptions as part of your work reality",
                    "Focus on shorter work sessions",
                    "Work on interruption-friendly tasks"
                ],
                estimated_impact="Potentially improved focus during protected time",
                effort_required="Low - just try protecting one session"
            ))
        
        return recommendations[:2]  # Limit to avoid overwhelm
    
    def start_self_discovery_session(self, category: ReflectionCategory, 
                                   support_level: SupportLevel = SupportLevel.GUIDED) -> Dict[str, Any]:
        """
        Start a self-discovery session integrating patterns from all modules
        """
        # Start discovery session
        session_id = self.self_discovery.start_discovery_session(category, support_level)
        
        # Provide relevant patterns for user interpretation
        context_data = self._gather_discovery_context(category)
        
        # Get appropriate prompts
        prompts = self.self_discovery.get_reflection_prompts(category, support_level)
        
        return {
            "session_id": session_id,
            "category": category.value,
            "support_level": support_level.value,
            "prompts": [
                {
                    "question": prompt.question,
                    "follow_ups": prompt.follow_up_questions,
                    "guidance": prompt.guidance_notes,
                    "boundaries": prompt.professional_boundary
                }
                for prompt in prompts
            ],
            "context_data": context_data,
            "user_control": {
                "skip_questions": "You can skip any questions that don't resonate",
                "modify_approach": "Change support level anytime",
                "stop_session": "End session whenever you want",
                "data_privacy": "All insights remain private to you"
            }
        }
    
    def _gather_discovery_context(self, category: ReflectionCategory) -> Dict[str, Any]:
        """Gather relevant data for self-discovery context"""
        context = {}
        
        if category == ReflectionCategory.PRODUCTIVITY_PATTERNS:
            # Provide pattern data for user interpretation
            if len(self.time_tracker.entries) >= 10:
                patterns = self.pattern_analyzer.analyze_time_patterns(self.time_tracker.entries)
                context["patterns_for_reflection"] = {
                    name: {
                        "observations": pattern.supporting_data.get("observations", []),
                        "confidence": pattern.confidence.value,
                        "your_interpretation_needed": True
                    }
                    for name, pattern in patterns.items()
                }
        
        elif category == ReflectionCategory.ENERGY_AWARENESS:
            # Provide energy-related insights
            recent_entries = [
                e for e in self.time_tracker.entries[-20:] 
                if e.energy_level and e.is_complete()
            ]
            
            if recent_entries:
                energy_data = {
                    "recent_energy_levels": [e.energy_level for e in recent_entries],
                    "energy_by_time": {},
                    "energy_by_category": {}
                }
                
                # Group by time of day
                for entry in recent_entries:
                    hour = entry.start_time.hour
                    if hour not in energy_data["energy_by_time"]:
                        energy_data["energy_by_time"][hour] = []
                    energy_data["energy_by_time"][hour].append(entry.energy_level)
                
                context["energy_data_for_reflection"] = energy_data
        
        return context
    
    def get_comprehensive_insights(self, timeframe_days: int = 30) -> Dict[str, Any]:
        """
        Generate comprehensive insights from all modules with proper attribution
        """
        insights = {
            "summary": {
                "timeframe_days": timeframe_days,
                "data_sources": [],
                "confidence_levels": {},
                "user_interpretation_guidance": ""
            },
            "time_tracking_insights": {},
            "pattern_insights": {},
            "ai_insights": [],
            "integration_insights": [],
            "next_steps": [],
            "limitations": []
        }
        
        # Time tracking insights
        daily_summaries = []
        for i in range(min(timeframe_days, 30)):  # Limit to avoid overwhelming
            date = datetime.now().date() - timedelta(days=i)
            summary = self.time_tracker.get_daily_summary(datetime.combine(date, datetime.min.time()))
            if summary.get("entries_count", 0) > 0:
                daily_summaries.append(summary)
        
        if daily_summaries:
            insights["time_tracking_insights"] = {
                "active_days": len(daily_summaries),
                "total_tracked_time": sum(s.get("total_minutes", 0) for s in daily_summaries),
                "average_daily_time": sum(s.get("total_minutes", 0) for s in daily_summaries) / len(daily_summaries),
                "confidence": "high",
                "source": "Your direct time tracking data"
            }
            insights["summary"]["data_sources"].append("time_tracking")
        
        # Pattern analysis insights
        if len(self.time_tracker.entries) >= 10:
            patterns = self.pattern_analyzer.analyze_time_patterns(
                self.time_tracker.entries, timeframe_days
            )
            insights["pattern_insights"] = {
                name: {
                    "description": pattern.description,
                    "confidence": pattern.confidence.value,
                    "sample_size": pattern.sample_size,
                    "limitations": pattern.limitations,
                    "user_interpretation_required": pattern.user_interpretation_required
                }
                for name, pattern in patterns.items()
            }
            insights["summary"]["data_sources"].append("pattern_analysis")
        
        # AI insights (if user wants them)
        if self.user_preferences.get("ai_assistance_level") != "minimal":
            ai_insights = self.ai_tracker.analyze_productivity_patterns(self.time_tracker.entries)
            insights["ai_insights"] = [
                {
                    "description": insight.description,
                    "confidence": insight.confidence.value,
                    "supporting_evidence": insight.supporting_evidence,
                    "contradicting_evidence": insight.contradicting_evidence,
                    "limitations": insight.limitations,
                    "alternative_explanations": insight.alternative_explanations
                }
                for insight in ai_insights
            ]
            if ai_insights:
                insights["summary"]["data_sources"].append("ai_analysis")
        
        # Integration insights (cross-module observations)
        integration_insights = self._generate_integration_insights(insights)
        insights["integration_insights"] = integration_insights
        
        # Next steps and recommendations
        insights["next_steps"] = self._generate_comprehensive_next_steps(insights)
        
        # Overall limitations
        insights["limitations"] = [
            "All insights based on available data and may not capture your full productivity picture",
            "Patterns may change with life circumstances, work changes, or personal growth",
            "Individual context and external factors not fully captured in data",
            "You are the expert on your own productivity - use insights as starting points for reflection"
        ]
        
        insights["summary"]["user_interpretation_guidance"] = (
            "These insights are observations from your data, not prescriptions. "
            "Consider what resonates with your experience and what you'd like to explore further."
        )
        
        return insights
    
    def _generate_integration_insights(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights that combine data from multiple modules"""
        integration_insights = []
        
        # Check for consistency across modules
        if ("pattern_insights" in insights and "ai_insights" in insights and 
            insights["pattern_insights"] and insights["ai_insights"]):
            
            integration_insights.append({
                "type": "cross_validation",
                "description": "Both pattern analysis and AI observations available for comparison",
                "guidance": "Look for insights that appear in both analyses - these may be more reliable",
                "user_action": "Compare different sources and see what aligns with your experience"
            })
        
        # Check for sufficient data quality
        time_tracking = insights.get("time_tracking_insights", {})
        if time_tracking.get("active_days", 0) >= 14:
            integration_insights.append({
                "type": "data_maturity",
                "description": f"Good data foundation with {time_tracking.get('active_days')} active days",
                "guidance": "Insights are becoming more reliable with consistent tracking",
                "user_action": "Consider which patterns feel most accurate to your experience"
            })
        
        return integration_insights
    
    def _generate_comprehensive_next_steps(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate thoughtful next steps based on comprehensive insights"""
        next_steps = []
        
        # Self-discovery recommendation
        next_steps.append({
            "category": "self_reflection",
            "title": "Reflect on Your Patterns",
            "description": "Use the self-discovery tools to explore what these patterns mean to you",
            "rationale": "You're the expert on your own productivity - external data is just one input",
            "action": "Start a reflection session in an area that interests you"
        })
        
        # Experimentation recommendation
        if len(insights.get("pattern_insights", {})) > 0:
            next_steps.append({
                "category": "experimentation",
                "title": "Try a Personal Productivity Experiment",
                "description": "Test one insight that resonates with you",
                "rationale": "Small experiments help you discover what actually works for your situation",
                "action": "Choose one pattern to explore through a week-long experiment"
            })
        
        # System optimization if appropriate
        time_tracking = insights.get("time_tracking_insights", {})
        if time_tracking.get("active_days", 0) >= 21:
            next_steps.append({
                "category": "system_optimization",
                "title": "Consider Advanced Features",
                "description": "You've built a solid foundation - explore additional FlowState features",
                "rationale": "Consistent usage suggests you're ready for more sophisticated tools",
                "action": "Review available features and unlock ones that interest you"
            })
        
        return next_steps
    
    def _assess_system_health(self) -> Dict[str, Any]:
        """Assess overall system health and reliability"""
        health_metrics = {
            "data_quality": "good",
            "module_status": {},
            "recommendations": [],
            "user_action_needed": False
        }
        
        # Check each module's health
        entry_count = len(self.time_tracker.entries)
        health_metrics["module_status"]["time_tracker"] = {
            "status": "good" if entry_count >= 5 else "building",
            "data_points": entry_count
        }
        
        # Check AI module health
        ai_accuracy = self.ai_tracker.get_ai_track_record()
        ai_status = "good" if ai_accuracy.get("prediction_accuracy", {}).get("accuracy_rate", 0) > 0.6 else "learning"
        health_metrics["module_status"]["ai_tracker"] = {
            "status": ai_status,
            "accuracy": ai_accuracy.get("prediction_accuracy", {})
        }
        
        # Overall assessment
        if entry_count < 5:
            health_metrics["data_quality"] = "building"
            health_metrics["recommendations"].append(
                "Continue tracking time to improve insight quality"
            )
        
        return health_metrics
    
    def _get_usage_data_for_ui(self) -> Dict[str, Any]:
        """Generate usage data for UI progression calculations"""
        first_entry = min(self.time_tracker.entries, key=lambda e: e.start_time) if self.time_tracker.entries else None
        
        return {
            "first_use_date": first_entry.start_time.isoformat() if first_entry else datetime.now().isoformat(),
            "total_sessions": len([e for e in self.time_tracker.entries if e.is_complete()]),
            "total_time_entries": len(self.time_tracker.entries),
            "features_used": ["basic_timer", "time_logging", "daily_summary"],  # Would track actual usage
            "sessions_last_14_days": [1] * 14,  # Simplified - would track actual daily usage
            "satisfaction_rating": 4.0  # Would come from user feedback
        }
    
    def _record_session_event(self, event_type: str, data: Dict[str, Any]):
        """Record events for learning and improvement"""
        self.user_feedback_history.append({
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data,
            "user_id": self.user_id
        })
    
    def provide_user_feedback(self, feedback_type: str, rating: int, 
                            comments: str = "", specific_feature: str = "") -> bool:
        """
        Allow users to provide feedback on system performance
        
        Args:
            feedback_type: Type of feedback (recommendation, insight, feature, overall)
            rating: Rating from 1-5
            comments: Optional user comments
            specific_feature: Specific feature being rated
            
        Returns:
            bool: Feedback recorded successfully
        """
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "type": feedback_type,
            "rating": rating,
            "comments": comments,
            "specific_feature": specific_feature,
            "system_status": self.system_status.value
        }
        
        self.user_feedback_history.append(feedback)
        
        # Adjust system behavior based on feedback
        if rating <= 2 and feedback_type == "recommendation":
            # Reduce recommendation frequency for low ratings
            self.user_preferences["intervention_style"] = "minimal"
        
        return True
    
    def export_complete_user_data(self) -> Dict[str, Any]:
        """
        Export all user data across modules with full transparency
        """
        return {
            "user_id": self.user_id,
            "export_timestamp": datetime.now().isoformat(),
            "productivity_engine": {
                "current_mode": self.current_mode.value,
                "user_preferences": self.user_preferences,
                "system_status": self.system_status.value,
                "feedback_history": self.user_feedback_history
            },
            "time_tracking_data": self.time_tracker.export_data(),
            "ai_data": self.ai_tracker.export_ai_data(),
            "ui_progression": self.ui_manager.export_progression_data(),
            "self_discovery_sessions": [
                self.self_discovery.export_discovery_summary(session.session_id)
                for session in self.self_discovery.discovery_sessions
            ],
            "data_ownership_statement": {
                "ownership": "All data belongs entirely to the user",
                "control": "User has complete control over data use and sharing",
                "deletion": "Complete data deletion available at any time",
                "privacy": "No data is shared without explicit user consent"
            }
        }
    
    def reset_all_data(self, user_confirmation: str = "") -> bool:
        """
        Complete data reset with explicit confirmation
        
        Args:
            user_confirmation: Must be "CONFIRM_RESET_ALL_DATA"
            
        Returns:
            bool: Reset successful
        """
        if user_confirmation != "CONFIRM_RESET_ALL_DATA":
            return False
        
        # Reset all modules
        self.time_tracker.clear_data()
        self.ai_tracker = HonestAITracker(self.user_id)
        self.ui_manager.reset_to_minimal(user_confirmation=True)
        self.self_discovery.clear_user_data(user_confirmation=True)
        
        # Reset engine state
        self.current_mode = ProductivityMode.GROWTH
        self.system_status = SystemStatus.OPTIMAL
        self.active_recommendations.clear()
        self.user_feedback_history.clear()
        
        return True


# Example usage and testing
if __name__ == "__main__":
    # Create productivity engine
    engine = ProductivityEngine("user_123")
    
    # Start a productivity session
    session_start = engine.start_productivity_session(
        "Writing project documentation", 
        "work", 
        estimated_minutes=60,
        context={"energy_level": 4, "goal": "complete_outline"}
    )
    
    print("Session Started:")
    print(json.dumps(session_start, indent=2))
    
    # Simulate session end
    session_end = engine.end_productivity_session(
        user_notes="Completed outline and first two sections",
        energy_level=3,
        focus_quality=4,
        interruptions=2,
        satisfaction=4
    )
    
    print("\nSession Completed:")
    print(json.dumps(session_end, indent=2))
    
    # Get daily summary
    daily_summary = engine.get_daily_productivity_summary()
    print("\nDaily Summary:")
    print(json.dumps(daily_summary, indent=2))

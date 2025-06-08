

"""
FlowState Honest AI Tracking Module
Based on expert analysis: Pragmatic AI with realistic limitations and transparent uncertainty

Key principles implemented:
- Honest about AI limitations and uncertainty
- User agency preserved over all AI suggestions
- Graceful degradation when AI is uncertain
- Evidence-based methods with confidence scoring
- No overpromising or "revolutionary" AI claims
"""

import json
import random
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque

from ..core.time_tracker import TimeEntry, ConfidenceLevel
from ..core.pattern_analyzer import PatternInsight


class AIConfidenceLevel(Enum):
    """Honest AI confidence levels"""
    HIGH = "high"           # >80% historical accuracy on similar predictions
    MODERATE = "moderate"   # 60-80% historical accuracy
    LOW = "low"            # 40-60% historical accuracy  
    UNCERTAIN = "uncertain" # <40% accuracy or insufficient data
    NO_PREDICTION = "no_prediction"  # AI chooses not to predict


class PredictionType(Enum):
    """Types of predictions AI can attempt"""
    PRODUCTIVITY_TIMING = "productivity_timing"
    TASK_DURATION = "task_duration"
    INTERRUPTION_LIKELIHOOD = "interruption_likelihood"
    ENERGY_LEVEL = "energy_level"
    FOCUS_QUALITY = "focus_quality"


@dataclass
class AIPrediction:
    """AI prediction with honest limitations"""
    prediction_type: PredictionType
    prediction_value: Any
    confidence: AIConfidenceLevel
    reasoning: str
    limitations: str
    historical_accuracy: Optional[float]
    sample_size: int
    user_override_available: bool = True
    expires_at: Optional[datetime] = None


@dataclass
class AIInsight:
    """AI-generated insight with transparent uncertainty"""
    insight_type: str
    description: str
    confidence: AIConfidenceLevel
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    limitations: str
    user_interpretation_needed: bool = True
    alternative_explanations: List[str] = None


class SimpleRuleEngine:
    """
    Simple rule-based logic disguised as AI for reliability
    90% of "AI" decisions come from deterministic rules
    """
    
    def __init__(self):
        self.rules = {
            "productivity_timing": [
                {
                    "condition": lambda data: self._check_morning_productivity(data),
                    "prediction": "morning_productivity_likely",
                    "confidence": AIConfidenceLevel.MODERATE,
                    "reasoning": "Historical data shows higher morning productivity"
                },
                {
                    "condition": lambda data: self._check_afternoon_energy_drop(data),
                    "prediction": "afternoon_energy_drop_likely", 
                    "confidence": AIConfidenceLevel.MODERATE,
                    "reasoning": "Pattern of lower afternoon energy detected"
                }
            ],
            "interruption_patterns": [
                {
                    "condition": lambda data: self._check_high_interruption_period(data),
                    "prediction": "high_interruption_risk",
                    "confidence": AIConfidenceLevel.LOW,
                    "reasoning": "Historical interruption frequency suggests higher risk"
                }
            ]
        }
    
    def _check_morning_productivity(self, data: List[TimeEntry]) -> bool:
        """Simple rule: check if morning sessions tend to be more productive"""
        morning_focus = [e.focus_quality for e in data if 6 <= e.start_time.hour <= 11]
        other_focus = [e.focus_quality for e in data if e.start_time.hour < 6 or e.start_time.hour > 11]
        
        if len(morning_focus) < 3 or len(other_focus) < 3:
            return False
        
        return statistics.mean(morning_focus) > statistics.mean(other_focus)
    
    def _check_afternoon_energy_drop(self, data: List[TimeEntry]) -> bool:
        """Simple rule: check for afternoon energy patterns"""
        afternoon_energy = [e.energy_level for e in data if 13 <= e.start_time.hour <= 16]
        morning_energy = [e.energy_level for e in data if 8 <= e.start_time.hour <= 11]
        
        if len(afternoon_energy) < 3 or len(morning_energy) < 3:
            return False
        
        return statistics.mean(afternoon_energy) < statistics.mean(morning_energy) - 0.5
    
    def _check_high_interruption_period(self, data: List[TimeEntry]) -> bool:
        """Simple rule: check for high interruption times"""
        current_hour = datetime.now().hour
        hour_interruptions = [e.interruptions for e in data if e.start_time.hour == current_hour]
        
        if len(hour_interruptions) < 3:
            return False
        
        return statistics.mean(hour_interruptions) > 2
    
    def evaluate_rules(self, prediction_type: str, data: List[TimeEntry]) -> List[Dict]:
        """Evaluate rules for given prediction type"""
        if prediction_type not in self.rules:
            return []
        
        results = []
        for rule in self.rules[prediction_type]:
            if rule["condition"](data):
                results.append({
                    "prediction": rule["prediction"],
                    "confidence": rule["confidence"],
                    "reasoning": rule["reasoning"]
                })
        
        return results


class AccuracyTracker:
    """Track AI prediction accuracy honestly"""
    
    def __init__(self):
        self.prediction_history: List[Dict] = []
        self.accuracy_by_type: Dict[PredictionType, List[bool]] = defaultdict(list)
        
    def record_prediction(self, prediction: AIPrediction, prediction_id: str):
        """Record a prediction for later accuracy tracking"""
        self.prediction_history.append({
            "id": prediction_id,
            "type": prediction.prediction_type,
            "predicted_value": prediction.prediction_value,
            "confidence": prediction.confidence,
            "timestamp": datetime.now(),
            "actual_outcome": None,
            "accuracy": None
        })
    
    def record_outcome(self, prediction_id: str, actual_outcome: Any) -> bool:
        """Record actual outcome for accuracy calculation"""
        for record in self.prediction_history:
            if record["id"] == prediction_id:
                record["actual_outcome"] = actual_outcome
                record["accuracy"] = self._calculate_accuracy(
                    record["predicted_value"], 
                    actual_outcome, 
                    record["type"]
                )
                
                # Update type-specific accuracy tracking
                self.accuracy_by_type[record["type"]].append(record["accuracy"])
                return True
        return False
    
    def _calculate_accuracy(self, predicted: Any, actual: Any, 
                          prediction_type: PredictionType) -> bool:
        """Calculate if prediction was accurate"""
        if prediction_type == PredictionType.TASK_DURATION:
            # Within 25% is considered accurate for duration
            if actual == 0:
                return predicted < 10  # Reasonable for very short tasks
            return abs(predicted - actual) / actual <= 0.25
        
        elif prediction_type == PredictionType.ENERGY_LEVEL:
            # Within 1 point on 1-5 scale
            return abs(predicted - actual) <= 1
        
        elif prediction_type == PredictionType.FOCUS_QUALITY:
            # Within 1 point on 1-5 scale
            return abs(predicted - actual) <= 1
        
        else:
            # Exact match for categorical predictions
            return predicted == actual
    
    def get_accuracy_stats(self, prediction_type: PredictionType = None) -> Dict[str, Any]:
        """Get honest accuracy statistics"""
        if prediction_type:
            accuracies = self.accuracy_by_type[prediction_type]
        else:
            accuracies = [record["accuracy"] for record in self.prediction_history 
                         if record["accuracy"] is not None]
        
        if len(accuracies) < 3:
            return {
                "accuracy": "insufficient_data",
                "sample_size": len(accuracies),
                "message": "Need at least 3 verified predictions for accuracy calculation",
                "confidence": AIConfidenceLevel.UNCERTAIN.value
            }
        
        accuracy_rate = sum(accuracies) / len(accuracies)
        
        return {
            "accuracy_rate": round(accuracy_rate, 3),
            "sample_size": len(accuracies),
            "confidence_assessment": self._assess_confidence(accuracy_rate),
            "limitations": "Based on limited sample and may not reflect future performance"
        }
    
    def _assess_confidence(self, accuracy_rate: float) -> AIConfidenceLevel:
        """Convert accuracy rate to confidence level"""
        if accuracy_rate >= 0.8:
            return AIConfidenceLevel.HIGH
        elif accuracy_rate >= 0.6:
            return AIConfidenceLevel.MODERATE
        elif accuracy_rate >= 0.4:
            return AIConfidenceLevel.LOW
        else:
            return AIConfidenceLevel.UNCERTAIN


class HonestAITracker:
    """
    AI system that's honest about its limitations and preserves user agency
    """
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.rule_engine = SimpleRuleEngine()
        self.accuracy_tracker = AccuracyTracker()
        self.recent_predictions: deque = deque(maxlen=50)  # Keep recent predictions
        self.user_overrides: List[Dict] = []  # Track when users override AI
        
        # Conservative thresholds
        self.minimum_sample_size = 10
        self.confidence_threshold = 0.6
        self.max_predictions_per_day = 5  # Don't overwhelm users
        
    def analyze_productivity_patterns(self, entries: List[TimeEntry]) -> List[AIInsight]:
        """
        Generate honest AI insights about productivity patterns
        """
        if len(entries) < self.minimum_sample_size:
            return [AIInsight(
                insight_type="insufficient_data",
                description=f"Only {len(entries)} entries available for analysis",
                confidence=AIConfidenceLevel.UNCERTAIN,
                supporting_evidence=[],
                contradicting_evidence=[],
                limitations=f"Need at least {self.minimum_sample_size} entries for reliable analysis",
                user_interpretation_needed=True,
                alternative_explanations=["More data collection needed"]
            )]
        
        insights = []
        
        # Rule-based pattern detection
        timing_rules = self.rule_engine.evaluate_rules("productivity_timing", entries)
        for rule_result in timing_rules:
            insights.append(AIInsight(
                insight_type="timing_pattern",
                description=rule_result["reasoning"],
                confidence=rule_result["confidence"],
                supporting_evidence=self._gather_supporting_evidence(entries, rule_result),
                contradicting_evidence=self._gather_contradicting_evidence(entries, rule_result),
                limitations="Based on simple pattern matching, may miss complex factors",
                user_interpretation_needed=True,
                alternative_explanations=["External factors not captured", "Sample size limitations", "Correlation not causation"]
            ))
        
        # Energy pattern analysis with uncertainty
        energy_insight = self._analyze_energy_patterns(entries)
        if energy_insight:
            insights.append(energy_insight)
        
        # Focus quality analysis
        focus_insight = self._analyze_focus_patterns(entries)
        if focus_insight:
            insights.append(focus_insight)
        
        return insights
    
    def predict_optimal_work_time(self, entries: List[TimeEntry], 
                                target_date: datetime) -> Optional[AIPrediction]:
        """
        Predict optimal work time with honest uncertainty
        """
        if len(entries) < self.minimum_sample_size:
            return None
        
        # Simple rule-based prediction
        hourly_productivity = defaultdict(list)
        for entry in entries:
            if entry.focus_quality and entry.energy_level:
                productivity_score = (entry.focus_quality + entry.energy_level) / 2
                hourly_productivity[entry.start_time.hour].append(productivity_score)
        
        if not hourly_productivity:
            return None
        
        # Find best hour with enough data
        best_hour = None
        best_score = 0
        best_sample_size = 0
        
        for hour, scores in hourly_productivity.items():
            if len(scores) >= 3:  # Need minimum sample
                avg_score = statistics.mean(scores)
                if avg_score > best_score:
                    best_hour = hour
                    best_score = avg_score
                    best_sample_size = len(scores)
        
        if not best_hour:
            return AIPrediction(
                prediction_type=PredictionType.PRODUCTIVITY_TIMING,
                prediction_value=None,
                confidence=AIConfidenceLevel.UNCERTAIN,
                reasoning="Insufficient data for reliable time prediction",
                limitations="Need more sessions at consistent times",
                historical_accuracy=None,
                sample_size=len(entries)
            )
        
        # Assess confidence based on data quality
        confidence = AIConfidenceLevel.MODERATE if best_sample_size >= 5 else AIConfidenceLevel.LOW
        
        return AIPrediction(
            prediction_type=PredictionType.PRODUCTIVITY_TIMING,
            prediction_value=f"{best_hour:02d}:00",
            confidence=confidence,
            reasoning=f"Hour {best_hour:02d}:00 shows highest average productivity score ({best_score:.1f}/5)",
            limitations=f"Based on {best_sample_size} sessions. External factors not considered.",
            historical_accuracy=self.accuracy_tracker.get_accuracy_stats(
                PredictionType.PRODUCTIVITY_TIMING
            ).get("accuracy_rate"),
            sample_size=best_sample_size,
            expires_at=datetime.now() + timedelta(days=7)  # Predictions expire
        )
    
    def predict_task_duration(self, task_description: str, 
                            category: str, entries: List[TimeEntry]) -> Optional[AIPrediction]:
        """
        Predict task duration with honest uncertainty
        """
        # Find similar tasks
        similar_tasks = [
            entry for entry in entries 
            if (entry.category == category and 
                entry.is_complete() and 
                entry.duration_minutes())
        ]
        
        if len(similar_tasks) < 3:
            return AIPrediction(
                prediction_type=PredictionType.TASK_DURATION,
                prediction_value=None,
                confidence=AIConfidenceLevel.UNCERTAIN,
                reasoning=f"Only {len(similar_tasks)} similar tasks found",
                limitations="Need at least 3 similar completed tasks for duration prediction",
                historical_accuracy=None,
                sample_size=len(similar_tasks)
            )
        
        # Simple duration prediction
        durations = [task.duration_minutes() for task in similar_tasks]
        avg_duration = statistics.mean(durations)
        duration_std = statistics.stdev(durations) if len(durations) > 1 else 0
        
        # Assess confidence based on variability
        if duration_std / avg_duration > 0.5:  # High variability
            confidence = AIConfidenceLevel.LOW
        else:
            confidence = AIConfidenceLevel.MODERATE
        
        return AIPrediction(
            prediction_type=PredictionType.TASK_DURATION,
            prediction_value=int(avg_duration),
            confidence=confidence,
            reasoning=f"Based on {len(similar_tasks)} similar {category} tasks averaging {avg_duration:.0f} minutes",
            limitations=f"High variability ({duration_std:.0f}min std dev). Task complexity not considered.",
            historical_accuracy=self.accuracy_tracker.get_accuracy_stats(
                PredictionType.TASK_DURATION
            ).get("accuracy_rate"),
            sample_size=len(similar_tasks)
        )
    
    def suggest_break_timing(self, current_session_start: datetime, 
                           entries: List[TimeEntry]) -> Optional[AIPrediction]:
        """
        Suggest when to take a break with honest limitations
        """
        current_duration = (datetime.now() - current_session_start).total_seconds() / 60
        
        # Find user's typical session patterns
        completed_sessions = [
            entry.duration_minutes() for entry in entries 
            if entry.is_complete() and entry.duration_minutes()
        ]
        
        if len(completed_sessions) < 5:
            return None
        
        # Simple rule: suggest break around user's typical session length
        typical_duration = statistics.median(completed_sessions)
        
        if current_duration >= typical_duration * 0.8:
            confidence = AIConfidenceLevel.MODERATE
            reasoning = f"Current session ({current_duration:.0f}min) approaching your typical length ({typical_duration:.0f}min)"
        else:
            confidence = AIConfidenceLevel.LOW
            reasoning = f"Based on typical session pattern, break suggested in {(typical_duration - current_duration):.0f} minutes"
        
        return AIPrediction(
            prediction_type=PredictionType.PRODUCTIVITY_TIMING,
            prediction_value="break_suggested",
            confidence=confidence,
            reasoning=reasoning,
            limitations="Based on duration patterns only. Energy and task state not considered.",
            historical_accuracy=None,
            sample_size=len(completed_sessions)
        )
    
    def _analyze_energy_patterns(self, entries: List[TimeEntry]) -> Optional[AIInsight]:
        """Analyze energy patterns with honest uncertainty"""
        energy_data = [(e.energy_level, e.start_time.hour) for e in entries if e.energy_level]
        
        if len(energy_data) < self.minimum_sample_size:
            return None
        
        # Group by time periods
        morning_energy = [e for e, h in energy_data if 6 <= h < 12]
        afternoon_energy = [e for e, h in energy_data if 12 <= h < 18]
        
        if len(morning_energy) < 3 or len(afternoon_energy) < 3:
            return None
        
        morning_avg = statistics.mean(morning_energy)
        afternoon_avg = statistics.mean(afternoon_energy)
        
        if abs(morning_avg - afternoon_avg) < 0.3:  # No significant difference
            return None
        
        supporting_evidence = [
            f"Morning energy average: {morning_avg:.1f}/5 ({len(morning_energy)} sessions)",
            f"Afternoon energy average: {afternoon_avg:.1f}/5 ({len(afternoon_energy)} sessions)"
        ]
        
        contradicting_evidence = [
            "Energy levels are self-reported and subjective",
            "External factors (sleep, caffeine, stress) not captured",
            "Small sample sizes may not be representative"
        ]
        
        return AIInsight(
            insight_type="energy_pattern",
            description=f"Energy appears {'higher' if morning_avg > afternoon_avg else 'lower'} in morning vs afternoon",
            confidence=AIConfidenceLevel.LOW,  # Conservative confidence
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence,
            limitations="Based on subjective self-reports. Individual daily variation not captured.",
            user_interpretation_needed=True,
            alternative_explanations=[
                "External factors (sleep, meals, stress)",
                "Work schedule effects",
                "Sample size limitations",
                "Reporting bias"
            ]
        )
    
    def _analyze_focus_patterns(self, entries: List[TimeEntry]) -> Optional[AIInsight]:
        """Analyze focus quality patterns with uncertainty"""
        focus_data = [
            (e.focus_quality, e.interruptions, e.duration_minutes()) 
            for e in entries 
            if e.focus_quality and e.duration_minutes()
        ]
        
        if len(focus_data) < self.minimum_sample_size:
            return None
        
        # Simple correlation analysis
        low_interruption_focus = [f for f, i, d in focus_data if i <= 1]
        high_interruption_focus = [f for f, i, d in focus_data if i >= 3]
        
        if len(low_interruption_focus) < 3 or len(high_interruption_focus) < 3:
            return None
        
        low_avg = statistics.mean(low_interruption_focus)
        high_avg = statistics.mean(high_interruption_focus)
        
        if abs(low_avg - high_avg) < 0.5:  # No significant difference
            return None
        
        return AIInsight(
            insight_type="focus_interruption_correlation",
            description=f"Focus quality appears {'lower' if high_avg < low_avg else 'higher'} during sessions with more interruptions",
            confidence=AIConfidenceLevel.LOW,
            supporting_evidence=[
                f"Low interruption sessions (≤1): {low_avg:.1f}/5 focus ({len(low_interruption_focus)} sessions)",
                f"High interruption sessions (≥3): {high_avg:.1f}/5 focus ({len(high_interruption_focus)} sessions)"
            ],
            contradicting_evidence=[
                "Correlation does not imply causation",
                "Self-reported focus quality is subjective",
                "Interruption types and contexts vary"
            ],
            limitations="Simple correlation analysis. Causation not established.",
            user_interpretation_needed=True,
            alternative_explanations=[
                "Difficult tasks naturally attract more interruptions",
                "Personal interruption tolerance varies",
                "External factors affecting both variables"
            ]
        )
    
    def _gather_supporting_evidence(self, entries: List[TimeEntry], 
                                   rule_result: Dict) -> List[str]:
        """Gather evidence supporting a rule-based conclusion"""
        evidence = []
        
        if "morning_productivity" in rule_result["prediction"]:
            morning_sessions = [e for e in entries if 6 <= e.start_time.hour <= 11]
            if morning_sessions:
                avg_focus = statistics.mean([e.focus_quality for e in morning_sessions if e.focus_quality])
                evidence.append(f"Morning sessions average {avg_focus:.1f}/5 focus quality")
        
        return evidence
    
    def _gather_contradicting_evidence(self, entries: List[TimeEntry], 
                                     rule_result: Dict) -> List[str]:
        """Gather evidence that contradicts or limits the conclusion"""
        return [
            "Small sample size may not be representative",
            "External factors not considered in analysis",
            "Individual daily variation not captured",
            "Self-reported metrics have inherent bias"
        ]
    
    def record_user_override(self, prediction_id: str, user_choice: str, 
                           reasoning: str = "") -> bool:
        """
        Record when user overrides AI suggestion to improve future recommendations
        """
        self.user_overrides.append({
            "prediction_id": prediction_id,
            "user_choice": user_choice,
            "user_reasoning": reasoning,
            "timestamp": datetime.now()
        })
        return True
    
    def get_ai_track_record(self) -> Dict[str, Any]:
        """
        Provide honest assessment of AI performance
        """
        accuracy_stats = self.accuracy_tracker.get_accuracy_stats()
        override_rate = len(self.user_overrides) / max(len(self.recent_predictions), 1)
        
        return {
            "prediction_accuracy": accuracy_stats,
            "user_override_rate": round(override_rate, 3),
            "total_predictions_made": len(self.recent_predictions),
            "limitations": [
                "AI predictions based on limited personal data",
                "External factors not captured in analysis", 
                "Individual context varies daily",
                "Correlation patterns may not indicate causation"
            ],
            "recommendation": "Use AI suggestions as starting points, not definitive answers",
            "user_control": "You can always override AI suggestions based on your judgment"
        }
    
    def should_make_prediction(self, prediction_type: PredictionType) -> bool:
        """
        Conservative decision about whether AI should attempt prediction
        """
        # Check daily prediction limit
        today_predictions = [
            p for p in self.recent_predictions 
            if p.get("timestamp", datetime.min).date() == datetime.now().date()
        ]
        
        if len(today_predictions) >= self.max_predictions_per_day:
            return False
        
        # Check historical accuracy for this type
        accuracy_stats = self.accuracy_tracker.get_accuracy_stats(prediction_type)
        if (accuracy_stats.get("accuracy_rate", 0) < self.confidence_threshold and 
            accuracy_stats.get("sample_size", 0) >= 5):
            return False
        
        return True
    
    def export_ai_data(self) -> Dict[str, Any]:
        """Export AI data with full transparency"""
        return {
            "user_id": self.user_id,
            "export_date": datetime.now().isoformat(),
            "prediction_history": [asdict(p) for p in self.recent_predictions],
            "accuracy_tracking": self.accuracy_tracker.get_accuracy_stats(),
            "user_overrides": self.user_overrides,
            "ai_limitations": {
                "minimum_sample_size": self.minimum_sample_size,
                "confidence_threshold": self.confidence_threshold,
                "prediction_types_supported": [t.value for t in PredictionType],
                "prediction_expiration": "7 days maximum"
            },
            "important_notes": {
                "data_ownership": "All data belongs to user",
                "ai_transparency": "AI methods are rule-based with simple statistics",
                "user_control": "Users can override any AI suggestion",
                "limitations": "AI cannot capture full context of human productivity"
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # Create honest AI tracker
    ai_tracker = HonestAITracker("user_123")
    
    # Example: analyze patterns (would use real TimeEntry data)
    insights = ai_tracker.analyze_productivity_patterns([])
    
    print("AI Insights (with limitations):")
    for insight in insights:
        print(f"- {insight.description}")
        print(f"  Confidence: {insight.confidence.value}")
        print(f"  Limitations: {insight.limitations}")
        print(f"  User interpretation needed: {insight.user_interpretation_needed}\n")
    
    # Get AI track record
    track_record = ai_tracker.get_ai_track_record()
    print("AI Track Record:")
    print(json.dumps(track_record, indent=2))

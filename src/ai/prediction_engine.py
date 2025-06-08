
"""
FlowState Prediction Engine
Honest AI Predictions with Uncertainty Quantification

This module provides productivity predictions while being transparent about
limitations, uncertainty, and the difference between correlation and causation.

Core Principles:
- Honest uncertainty - always show confidence intervals and alternatives
- Baseline comparisons - predictions vs random chance and simple heuristics
- User interpretation - AI provides data, users make decisions
- Failure transparency - track and report prediction accuracy
- Conservative predictions - avoid overconfident forecasts
- Explainable logic - users understand how predictions are made
"""

import json
import logging
import statistics
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any, Tuple, NamedTuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path
import math
from collections import defaultdict, deque
import random


class PredictionType(Enum):
    """Types of predictions the system can make"""
    PRODUCTIVITY_LEVEL = "productivity_level"     # How productive next session will be
    SESSION_DURATION = "session_duration"       # How long work session will last
    TASK_COMPLETION = "task_completion"         # Whether task will be completed
    BREAK_TIMING = "break_timing"              # When user will need a break
    FOCUS_QUALITY = "focus_quality"            # Quality of upcoming focus session
    ENERGY_LEVEL = "energy_level"              # Predicted energy level


class PredictionHorizon(Enum):
    """Time horizons for predictions"""
    IMMEDIATE = "immediate"     # Next 1-2 hours
    TODAY = "today"            # Rest of today
    TOMORROW = "tomorrow"      # Next day
    THIS_WEEK = "this_week"    # Next 7 days


class ConfidenceLevel(Enum):
    """Honest confidence levels with specific meanings"""
    VERY_LOW = "very_low"      # 20-40% - barely better than random
    LOW = "low"                # 40-60% - slightly better than random
    MODERATE = "moderate"      # 60-75% - useful but uncertain
    HIGH = "high"              # 75-85% - reliable for planning
    VERY_HIGH = "very_high"    # 85%+ - high confidence


@dataclass
class PredictionUncertainty:
    """Comprehensive uncertainty information"""
    confidence_interval: Tuple[float, float]  # Lower and upper bounds
    standard_error: float
    sample_size: int
    historical_accuracy: float
    baseline_comparison: str  # How much better than simple baseline
    alternative_scenarios: List[str]
    confounding_factors: List[str]
    data_limitations: List[str]


@dataclass
class Prediction:
    """Complete prediction with transparency"""
    prediction_id: str
    prediction_type: PredictionType
    horizon: PredictionHorizon
    predicted_value: float
    confidence: ConfidenceLevel
    uncertainty: PredictionUncertainty
    
    # Explainability
    reasoning: str
    key_factors: List[str]
    similar_past_situations: List[str]
    
    # Tracking
    created_at: datetime
    actual_outcome: Optional[float] = None
    accuracy_when_resolved: Optional[float] = None
    user_feedback: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'prediction_id': self.prediction_id,
            'prediction_type': self.prediction_type.value,
            'horizon': self.horizon.value,
            'predicted_value': self.predicted_value,
            'confidence': self.confidence.value,
            'uncertainty': asdict(self.uncertainty),
            'reasoning': self.reasoning,
            'key_factors': self.key_factors,
            'similar_past_situations': self.similar_past_situations,
            'created_at': self.created_at.isoformat(),
            'actual_outcome': self.actual_outcome,
            'accuracy_when_resolved': self.accuracy_when_resolved,
            'user_feedback': self.user_feedback
        }


class PredictionEngine:
    """
    Honest prediction engine with uncertainty quantification
    
    Makes productivity predictions while being transparent about limitations,
    uncertainty, and the risk of overconfident forecasting.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Conservative prediction parameters
        self.min_data_points = 20           # Minimum data for any prediction
        self.confidence_cap = 0.85          # Maximum confidence (85%)
        self.baseline_threshold = 0.1       # Must beat baseline by 10%
        self.uncertainty_inflation = 1.2    # Inflate uncertainty by 20%
        
        # Prediction tracking
        self.prediction_history = deque(maxlen=1000)
        self.accuracy_by_type = defaultdict(list)
        
        # Database setup
        self.db_path = self.data_dir / 'predictions.db'
        self._initialize_database()
        
        # Logging
        self.logger = logging.getLogger(__name__)
    
    def _initialize_database(self):
        """Initialize prediction tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id TEXT PRIMARY KEY,
                prediction_type TEXT NOT NULL,
                horizon TEXT NOT NULL,
                predicted_value REAL NOT NULL,
                confidence TEXT NOT NULL,
                uncertainty_data TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                key_factors TEXT NOT NULL,
                similar_situations TEXT NOT NULL,
                created_at TEXT NOT NULL,
                actual_outcome REAL,
                accuracy_when_resolved REAL,
                user_feedback TEXT
            )
        ''')
        
        # Prediction accuracy tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prediction_accuracy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_type TEXT NOT NULL,
                horizon TEXT NOT NULL,
                predicted_value REAL NOT NULL,
                actual_value REAL NOT NULL,
                absolute_error REAL NOT NULL,
                relative_error REAL NOT NULL,
                confidence_level TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def predict_productivity_level(self, context: Dict[str, Any], 
                                 historical_data: List[Dict[str, Any]]) -> Optional[Prediction]:
        """
        Predict productivity level for upcoming session
        
        Args:
            context: Current context (time, energy, environment, etc.)
            historical_data: Past productivity sessions
            
        Returns:
            Prediction with uncertainty or None if insufficient data
        """
        if len(historical_data) < self.min_data_points:
            return self._create_insufficient_data_prediction(
                PredictionType.PRODUCTIVITY_LEVEL, len(historical_data)
            )
        
        # Extract relevant historical patterns
        similar_sessions = self._find_similar_sessions(context, historical_data)
        
        if len(similar_sessions) < 5:
            return self._create_low_confidence_prediction(
                PredictionType.PRODUCTIVITY_LEVEL, 
                "Too few similar past situations for reliable prediction"
            )
        
        # Calculate prediction
        productivity_scores = [session['productivity_score'] for session in similar_sessions]
        predicted_value = statistics.mean(productivity_scores)
        
        # Calculate uncertainty
        std_dev = statistics.stdev(productivity_scores) if len(productivity_scores) > 1 else 1.0
        standard_error = std_dev / math.sqrt(len(productivity_scores))
        
        # Confidence interval (inflated for conservatism)
        margin_of_error = standard_error * 2 * self.uncertainty_inflation
        confidence_interval = (
            max(1.0, predicted_value - margin_of_error),
            min(5.0, predicted_value + margin_of_error)
        )
        
        # Compare to baseline (overall average)
        all_scores = [session['productivity_score'] for session in historical_data]
        baseline_prediction = statistics.mean(all_scores)
        improvement_over_baseline = abs(predicted_value - baseline_prediction) / baseline_prediction
        
        # Only make prediction if significantly better than baseline
        if improvement_over_baseline < self.baseline_threshold:
            return self._create_low_confidence_prediction(
                PredictionType.PRODUCTIVITY_LEVEL,
                f"Prediction ({predicted_value:.1f}) not significantly better than baseline ({baseline_prediction:.1f})"
            )
        
        # Calculate confidence level
        confidence_score = self._calculate_confidence(
            std_dev, len(similar_sessions), improvement_over_baseline
        )
        confidence_level = self._score_to_confidence(confidence_score)
        
        # Get historical accuracy for this prediction type
        historical_accuracy = self._get_historical_accuracy(PredictionType.PRODUCTIVITY_LEVEL)
        
        # Create uncertainty information
        uncertainty = PredictionUncertainty(
            confidence_interval=confidence_interval,
            standard_error=standard_error,
            sample_size=len(similar_sessions),
            historical_accuracy=historical_accuracy,
            baseline_comparison=f"{improvement_over_baseline:.1%} better than baseline average",
            alternative_scenarios=[
                f"If context factors change, could be {confidence_interval[0]:.1f}-{confidence_interval[1]:.1f}",
                "Unexpected interruptions could reduce productivity significantly",
                "High-energy periods might exceed prediction by 0.5-1.0 points"
            ],
            confounding_factors=self._identify_confounding_factors(context),
            data_limitations=[
                f"Based on only {len(similar_sessions)} similar past sessions",
                "Context matching may miss important factors",
                "Past performance doesn't guarantee future results"
            ]
        )
        
        # Generate reasoning
        reasoning = self._generate_productivity_reasoning(
            context, similar_sessions, predicted_value, baseline_prediction
        )
        
        # Create prediction
        prediction_id = f"productivity_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prediction = Prediction(
            prediction_id=prediction_id,
            prediction_type=PredictionType.PRODUCTIVITY_LEVEL,
            horizon=PredictionHorizon.IMMEDIATE,
            predicted_value=predicted_value,
            confidence=confidence_level,
            uncertainty=uncertainty,
            reasoning=reasoning,
            key_factors=self._extract_key_factors(context, similar_sessions),
            similar_past_situations=self._describe_similar_situations(similar_sessions),
            created_at=datetime.now()
        )
        
        # Store prediction
        self._store_prediction(prediction)
        
        return prediction
    
    def predict_session_duration(self, context: Dict[str, Any], 
                                historical_data: List[Dict[str, Any]]) -> Optional[Prediction]:
        """
        Predict how long upcoming work session will last
        
        Args:
            context: Current context
            historical_data: Past session durations
            
        Returns:
            Duration prediction with uncertainty
        """
        if len(historical_data) < self.min_data_points:
            return self._create_insufficient_data_prediction(
                PredictionType.SESSION_DURATION, len(historical_data)
            )
        
        # Find similar sessions
        similar_sessions = self._find_similar_sessions(context, historical_data)
        
        if len(similar_sessions) < 5:
            return self._create_low_confidence_prediction(
                PredictionType.SESSION_DURATION,
                "Insufficient similar sessions for duration prediction"
            )
        
        # Calculate duration prediction
        durations = [session.get('duration_minutes', 30) for session in similar_sessions]
        predicted_duration = statistics.median(durations)  # Use median for robustness
        
        # Calculate uncertainty
        duration_std = statistics.stdev(durations) if len(durations) > 1 else 15.0
        standard_error = duration_std / math.sqrt(len(durations))
        
        # Conservative confidence interval
        margin = standard_error * 2 * self.uncertainty_inflation
        confidence_interval = (
            max(5.0, predicted_duration - margin),
            predicted_duration + margin
        )
        
        # Compare to simple baseline (user's average session length)
        all_durations = [s.get('duration_minutes', 30) for s in historical_data]
        baseline_duration = statistics.median(all_durations)
        
        # Calculate confidence
        relative_error = duration_std / predicted_duration if predicted_duration > 0 else 1.0
        confidence_score = max(0.2, 1.0 - relative_error)  # Lower confidence for high variability
        confidence_level = self._score_to_confidence(confidence_score)
        
        # Historical accuracy
        historical_accuracy = self._get_historical_accuracy(PredictionType.SESSION_DURATION)
        
        # Create uncertainty information
        uncertainty = PredictionUncertainty(
            confidence_interval=confidence_interval,
            standard_error=standard_error,
            sample_size=len(similar_sessions),
            historical_accuracy=historical_accuracy,
            baseline_comparison=f"Baseline duration: {baseline_duration:.0f} minutes",
            alternative_scenarios=[
                f"Could range from {confidence_interval[0]:.0f} to {confidence_interval[1]:.0f} minutes",
                "Interruptions could significantly shorten session",
                "High engagement might extend session beyond prediction"
            ],
            confounding_factors=[
                "Interruption frequency", "Task complexity", "Energy levels",
                "Meeting schedule", "Deadline pressure"
            ],
            data_limitations=[
                f"Based on {len(similar_sessions)} similar sessions",
                "Duration variability is naturally high",
                "External factors not fully predictable"
            ]
        )
        
        # Generate reasoning
        reasoning = f"Based on {len(similar_sessions)} similar sessions, you typically work for " \
                   f"{predicted_duration:.0f} minutes in this context. Your sessions in similar " \
                   f"situations have ranged from {min(durations):.0f} to {max(durations):.0f} minutes."
        
        # Create prediction
        prediction_id = f"duration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prediction = Prediction(
            prediction_id=prediction_id,
            prediction_type=PredictionType.SESSION_DURATION,
            horizon=PredictionHorizon.IMMEDIATE,
            predicted_value=predicted_duration,
            confidence=confidence_level,
            uncertainty=uncertainty,
            reasoning=reasoning,
            key_factors=self._extract_duration_factors(context, similar_sessions),
            similar_past_situations=self._describe_similar_situations(similar_sessions),
            created_at=datetime.now()
        )
        
        self._store_prediction(prediction)
        return prediction
    
    def predict_task_completion(self, task_info: Dict[str, Any], 
                               historical_data: List[Dict[str, Any]]) -> Optional[Prediction]:
        """
        Predict probability of completing a specific task
        
        Args:
            task_info: Information about the task
            historical_data: Past task completion data
            
        Returns:
            Completion probability prediction
        """
        if len(historical_data) < self.min_data_points:
            return self._create_insufficient_data_prediction(
                PredictionType.TASK_COMPLETION, len(historical_data)
            )
        
        # Find similar tasks
        similar_tasks = self._find_similar_tasks(task_info, historical_data)
        
        if len(similar_tasks) < 3:
            return self._create_low_confidence_prediction(
                PredictionType.TASK_COMPLETION,
                "Too few similar tasks for reliable completion prediction"
            )
        
        # Calculate completion probability
        completed_tasks = sum(1 for task in similar_tasks if task.get('completed', False))
        completion_probability = completed_tasks / len(similar_tasks)
        
        # Calculate uncertainty using binomial distribution
        n = len(similar_tasks)
        p = completion_probability
        standard_error = math.sqrt(p * (1 - p) / n) if n > 0 else 0.5
        
        # Confidence interval for probability
        margin = standard_error * 2 * self.uncertainty_inflation
        confidence_interval = (
            max(0.0, completion_probability - margin),
            min(1.0, completion_probability + margin)
        )
        
        # Compare to baseline (overall completion rate)
        all_completions = [task.get('completed', False) for task in historical_data]
        baseline_rate = sum(all_completions) / len(all_completions)
        
        # Calculate confidence based on sample size and difference from baseline
        confidence_score = self._calculate_binomial_confidence(n, abs(completion_probability - baseline_rate))
        confidence_level = self._score_to_confidence(confidence_score)
        
        # Historical accuracy
        historical_accuracy = self._get_historical_accuracy(PredictionType.TASK_COMPLETION)
        
        # Create uncertainty information
        uncertainty = PredictionUncertainty(
            confidence_interval=confidence_interval,
            standard_error=standard_error,
            sample_size=len(similar_tasks),
            historical_accuracy=historical_accuracy,
            baseline_comparison=f"Overall completion rate: {baseline_rate:.1%}",
            alternative_scenarios=[
                f"Completion probability could be {confidence_interval[0]:.1%} to {confidence_interval[1]:.1%}",
                "Unexpected obstacles could reduce completion chance",
                "Additional time/resources could improve completion odds"
            ],
            confounding_factors=[
                "Task complexity variation", "Available time", "Competing priorities",
                "Energy levels", "External interruptions", "Resource availability"
            ],
            data_limitations=[
                f"Based on only {len(similar_tasks)} similar tasks",
                "Task similarity matching may miss important differences",
                "External factors can override historical patterns"
            ]
        )
        
        # Generate reasoning
        reasoning = f"Based on {len(similar_tasks)} similar tasks, you have a " \
                   f"{completion_probability:.1%} completion rate in comparable situations. " \
                   f"Your overall task completion rate is {baseline_rate:.1%}."
        
        # Create prediction
        prediction_id = f"completion_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prediction = Prediction(
            prediction_id=prediction_id,
            prediction_type=PredictionType.TASK_COMPLETION,
            horizon=PredictionHorizon.TODAY,
            predicted_value=completion_probability,
            confidence=confidence_level,
            uncertainty=uncertainty,
            reasoning=reasoning,
            key_factors=self._extract_completion_factors(task_info, similar_tasks),
            similar_past_situations=self._describe_similar_tasks(similar_tasks),
            created_at=datetime.now()
        )
        
        self._store_prediction(prediction)
        return prediction
    
    def _find_similar_sessions(self, context: Dict[str, Any], 
                              historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find historically similar work sessions"""
        similar_sessions = []
        
        for session in historical_data:
            similarity_score = 0.0
            factors_compared = 0
            
            # Time of day similarity
            if 'time_of_day' in context and 'timestamp' in session:
                try:
                    session_time = datetime.fromisoformat(session['timestamp']).hour
                    context_time = context.get('time_of_day', 12)
                    time_diff = abs(session_time - context_time)
                    time_similarity = max(0, 1 - time_diff / 12)  # Scale 0-1
                    similarity_score += time_similarity
                    factors_compared += 1
                except (ValueError, TypeError):
                    pass
            
            # Day of week similarity
            if 'day_of_week' in context and 'timestamp' in session:
                try:
                    session_day = datetime.fromisoformat(session['timestamp']).weekday()
                    context_day = context.get('day_of_week', 0)
                    day_similarity = 1.0 if session_day == context_day else 0.3
                    similarity_score += day_similarity
                    factors_compared += 1
                except (ValueError, TypeError):
                    pass
            
            # Task type similarity
            if 'task_type' in context and 'task_type' in session:
                type_similarity = 1.0 if session['task_type'] == context['task_type'] else 0.2
                similarity_score += type_similarity
                factors_compared += 1
            
            # Energy level similarity
            if 'energy_level' in context and 'energy_level' in session:
                energy_diff = abs(context['energy_level'] - session.get('energy_level', 3))
                energy_similarity = max(0, 1 - energy_diff / 4)
                similarity_score += energy_similarity
                factors_compared += 1
            
            # Overall similarity threshold
            if factors_compared > 0:
                avg_similarity = similarity_score / factors_compared
                if avg_similarity >= 0.6:  # 60% similarity threshold
                    similar_sessions.append(session)
        
        return similar_sessions
    
    def _find_similar_tasks(self, task_info: Dict[str, Any], 
                           historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find historically similar tasks"""
        similar_tasks = []
        
        for task in historical_data:
            similarity_score = 0.0
            factors_compared = 0
            
            # Task category similarity
            if 'category' in task_info and 'category' in task:
                category_similarity = 1.0 if task['category'] == task_info['category'] else 0.2
                similarity_score += category_similarity
                factors_compared += 1
            
            # Estimated duration similarity
            if 'estimated_duration' in task_info and 'estimated_duration' in task:
                duration_diff = abs(task_info['estimated_duration'] - task['estimated_duration'])
                max_duration = max(task_info['estimated_duration'], task['estimated_duration'])
                duration_similarity = max(0, 1 - duration_diff / max_duration) if max_duration > 0 else 0
                similarity_score += duration_similarity
                factors_compared += 1
            
            # Complexity similarity
            if 'complexity' in task_info and 'complexity' in task:
                complexity_diff = abs(task_info['complexity'] - task['complexity'])
                complexity_similarity = max(0, 1 - complexity_diff / 4)  # Assuming 1-5 scale
                similarity_score += complexity_similarity
                factors_compared += 1
            
            if factors_compared > 0:
                avg_similarity = similarity_score / factors_compared
                if avg_similarity >= 0.5:  # 50% similarity threshold for tasks
                    similar_tasks.append(task)
        
        return similar_tasks
    
    def _calculate_confidence(self, std_dev: float, sample_size: int, 
                            baseline_improvement: float) -> float:
        """Calculate confidence score based on data quality"""
        # Base confidence from sample size
        size_confidence = min(0.8, sample_size / 50)  # Cap at 80% for sample size
        
        # Reduce confidence for high variability
        variability_penalty = min(0.3, std_dev / 2)  # Assuming 1-5 scale
        
        # Boost confidence for beating baseline
        baseline_bonus = min(0.2, baseline_improvement)
        
        confidence = size_confidence - variability_penalty + baseline_bonus
        return max(0.2, min(self.confidence_cap, confidence))
    
    def _calculate_binomial_confidence(self, sample_size: int, effect_size: float) -> float:
        """Calculate confidence for binomial predictions (completion rates)"""
        # Base confidence from sample size
        size_confidence = min(0.7, sample_size / 20)
        
        # Boost for larger effect sizes
        effect_bonus = min(0.2, effect_size * 2)
        
        confidence = size_confidence + effect_bonus
        return max(0.2, min(self.confidence_cap, confidence))
    
    def _score_to_confidence(self, score: float) -> ConfidenceLevel:
        """Convert numerical confidence to categorical level"""
        if score < 0.4:
            return ConfidenceLevel.VERY_LOW
        elif score < 0.6:
            return ConfidenceLevel.LOW
        elif score < 0.75:
            return ConfidenceLevel.MODERATE
        elif score < 0.85:
            return ConfidenceLevel.HIGH
        else:
            return ConfidenceLevel.VERY_HIGH
    
    def _identify_confounding_factors(self, context: Dict[str, Any]) -> List[str]:
        """Identify factors that could affect prediction accuracy"""
        factors = [
            "Unexpected interruptions or urgent tasks",
            "Changes in energy levels throughout the day",
            "Environmental factors (noise, lighting, temperature)",
            "Social interactions and team dynamics"
        ]
        
        # Add context-specific factors
        if context.get('time_of_day') in ['early_morning', 'late_evening']:
            factors.append("Time of day effects on cognitive performance")
        
        if context.get('day_of_week') in ['monday', 'friday']:
            factors.append("Beginning/end of week motivation effects")
        
        if context.get('task_type') == 'creative':
            factors.append("Creative work variability and inspiration factors")
        
        return factors
    
    def _generate_productivity_reasoning(self, context: Dict[str, Any], 
                                       similar_sessions: List[Dict[str, Any]], 
                                       predicted_value: float, 
                                       baseline_prediction: float) -> str:
        """Generate human-readable reasoning for productivity prediction"""
        session_count = len(similar_sessions)
        scores = [s['productivity_score'] for s in similar_sessions]
        score_range = f"{min(scores):.1f} to {max(scores):.1f}"
        
        reasoning = f"Based on {session_count} similar past sessions, your productivity "
        reasoning += f"in this context typically ranges from {score_range} (average: {predicted_value:.1f}). "
        
        if predicted_value > baseline_prediction:
            reasoning += f"This is {predicted_value - baseline_prediction:.1f} points higher than your overall average "
            reasoning += f"({baseline_prediction:.1f}), suggesting favorable conditions."
        else:
            reasoning += f"This is {baseline_prediction - predicted_value:.1f} points below your overall average "
            reasoning += f"({baseline_prediction:.1f}), suggesting some challenges in this context."
        
        return reasoning
    
    def _extract_key_factors(self, context: Dict[str, Any], 
                           similar_sessions: List[Dict[str, Any]]) -> List[str]:
        """Extract key factors influencing the prediction"""
        factors = []
        
        if 'time_of_day' in context:
            factors.append(f"Time of day: {context['time_of_day']}")
        
        if 'task_type' in context:
            factors.append(f"Task type: {context['task_type']}")
        
        if 'energy_level' in context:
            factors.append(f"Energy level: {context['energy_level']}/5")
        
        # Add factors from analysis of similar sessions
        if similar_sessions:
            avg_duration = statistics.mean([s.get('duration_minutes', 30) for s in similar_sessions])
            factors.append(f"Typical session length in this context: {avg_duration:.0f} minutes")
        
        return factors
    
    def _extract_duration_factors(self, context: Dict[str, Any], 
                                 similar_sessions: List[Dict[str, Any]]) -> List[str]:
        """Extract factors affecting session duration"""
        factors = []
        
        if context.get('available_time'):
            factors.append(f"Available time: {context['available_time']} minutes")
        
        if context.get('task_complexity'):
            factors.append(f"Task complexity: {context['task_complexity']}/5")
        
        if similar_sessions:
            durations = [s.get('duration_minutes', 30) for s in similar_sessions]
            avg_duration = statistics.mean(durations)
            factors.append(f"Your average in similar contexts: {avg_duration:.0f} minutes")
            
            if len(durations) > 1:
                duration_consistency = 1 - (statistics.stdev(durations) / avg_duration)
                if duration_consistency > 0.7:
                    factors.append("You're quite consistent in similar situations")
                else:
                    factors.append("Duration varies significantly in similar situations")
        
        return factors
    
    def _extract_completion_factors(self, task_info: Dict[str, Any], 
                                   similar_tasks: List[Dict[str, Any]]) -> List[str]:
        """Extract factors affecting task completion"""
        factors = []
        
        if 'estimated_duration' in task_info:
            factors.append(f"Estimated duration: {task_info['estimated_duration']} minutes")
        
        if 'complexity' in task_info:
            factors.append(f"Task complexity: {task_info['complexity']}/5")
        
        if 'priority' in task_info:
            factors.append(f"Priority level: {task_info['priority']}")
        
        if similar_tasks:
            completion_rate = sum(1 for t in similar_tasks if t.get('completed', False)) / len(similar_tasks)
            factors.append(f"Completion rate for similar tasks: {completion_rate:.1%}")
        
        return factors
    
    def _describe_similar_situations(self, similar_data: List[Dict[str, Any]]) -> List[str]:
        """Describe the similar past situations used for prediction"""
        if not similar_data:
            return ["No similar past situations found"]
        
        descriptions = []
        
        # Group by common characteristics
        time_groups = defaultdict(int)
        for item in similar_data:
            if 'timestamp' in item:
                try:
                    hour = datetime.fromisoformat(item['timestamp']).hour
                    if 6 <= hour < 12:
                        time_groups['morning'] += 1
                    elif 12 <= hour < 17:
                        time_groups['afternoon'] += 1
                    elif 17 <= hour < 22:
                        time_groups['evening'] += 1
                    else:
                        time_groups['night'] += 1
                except (ValueError, TypeError):
                    pass
        
        if time_groups:
            most_common_time = max(time_groups, key=time_groups.get)
            descriptions.append(f"Most similar sessions were in the {most_common_time}")
        
        # Add task type info if available
        task_types = [item.get('task_type') for item in similar_data if 'task_type' in item]
        if task_types:
            most_common_type = max(set(task_types), key=task_types.count)
            descriptions.append(f"Similar tasks were mostly {most_common_type} work")
        
        descriptions.append(f"Based on {len(similar_data)} similar past situations")
        
        return descriptions
    
    def _describe_similar_tasks(self, similar_tasks: List[Dict[str, Any]]) -> List[str]:
        """Describe similar tasks used for completion prediction"""
        if not similar_tasks:
            return ["No similar tasks found"]
        
        descriptions = []
        
        # Completion rate
        completed = sum(1 for task in similar_tasks if task.get('completed', False))
        total = len(similar_tasks)
        descriptions.append(f"{completed} of {total} similar tasks were completed")
        
        # Common categories
        categories = [task.get('category') for task in similar_tasks if 'category' in task]
        if categories:
            most_common_category = max(set(categories), key=categories.count)
            descriptions.append(f"Most were {most_common_category} tasks")
        
        return descriptions
    
    def _create_insufficient_data_prediction(self, prediction_type: PredictionType, 
                                           current_data: int) -> Prediction:
        """Create prediction explaining insufficient data"""
        prediction_id = f"insufficient_{prediction_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        uncertainty = PredictionUncertainty(
            confidence_interval=(0.0, 1.0),
            standard_error=1.0,
            sample_size=current_data,
            historical_accuracy=0.0,
            baseline_comparison="Cannot compare - insufficient data",
            alternative_scenarios=["Any outcome possible with limited data"],
            confounding_factors=["All factors unknown with insufficient data"],
            data_limitations=[f"Only {current_data} data points available, need {self.min_data_points}"]
        )
        
        return Prediction(
            prediction_id=prediction_id,
            prediction_type=prediction_type,
            horizon=PredictionHorizon.IMMEDIATE,
            predicted_value=0.0,
            confidence=ConfidenceLevel.VERY_LOW,
            uncertainty=uncertainty,
            reasoning=f"Cannot make reliable {prediction_type.value} prediction with only "
                     f"{current_data} data points. Need at least {self.min_data_points} for basic predictions.",
            key_factors=[f"Insufficient data: {current_data}/{self.min_data_points} required"],
            similar_past_situations=["No prediction possible yet"],
            created_at=datetime.now()
        )
    
    def _create_low_confidence_prediction(self, prediction_type: PredictionType, 
                                        reason: str) -> Prediction:
        """Create low-confidence prediction with explanation"""
        prediction_id = f"low_conf_{prediction_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        uncertainty = PredictionUncertainty(
            confidence_interval=(0.0, 1.0),
            standard_error=0.5,
            sample_size=0,
            historical_accuracy=0.0,
            baseline_comparison="Similar to random chance",
            alternative_scenarios=["Wide range of outcomes possible"],
            confounding_factors=["Multiple unknown factors"],
            data_limitations=[reason]
        )
        
        return Prediction(
            prediction_id=prediction_id,
            prediction_type=prediction_type,
            horizon=PredictionHorizon.IMMEDIATE,
            predicted_value=0.5,  # Neutral prediction
            confidence=ConfidenceLevel.VERY_LOW,
            uncertainty=uncertainty,
            reasoning=f"Cannot make confident {prediction_type.value} prediction: {reason}",
            key_factors=["Insufficient similar data"],
            similar_past_situations=["Not enough similar situations"],
            created_at=datetime.now()
        )
    
    def _get_historical_accuracy(self, prediction_type: PredictionType) -> float:
        """Get historical accuracy for this prediction type"""
        if prediction_type not in self.accuracy_by_type:
            return 0.0
        
        accuracies = self.accuracy_by_type[prediction_type]
        if not accuracies:
            return 0.0
        
        return statistics.mean(accuracies[-20:])  # Last 20 predictions
    
    def _store_prediction(self, prediction: Prediction):
        """Store prediction in database for tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions 
                (prediction_id, prediction_type, horizon, predicted_value, confidence,
                 uncertainty_data, reasoning, key_factors, similar_situations, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prediction.prediction_id,
                prediction.prediction_type.value,
                prediction.horizon.value,
                prediction.predicted_value,
                prediction.confidence.value,
                json.dumps(asdict(prediction.uncertainty)),
                prediction.reasoning,
                json.dumps(prediction.key_factors),
                json.dumps(prediction.similar_past_situations),
                prediction.created_at.isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            # Add to in-memory tracking
            self.prediction_history.append(prediction)
            
            self.logger.info(f"Stored prediction: {prediction.prediction_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to store prediction: {e}")
    
    def resolve_prediction(self, prediction_id: str, actual_outcome: float, 
                          user_feedback: str = "") -> bool:
        """
        Resolve prediction with actual outcome to track accuracy
        
        Args:
            prediction_id: ID of prediction to resolve
            actual_outcome: What actually happened
            user_feedback: User's assessment of prediction quality
            
        Returns:
            True if resolved successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get original prediction
            cursor.execute('''
                SELECT predicted_value, prediction_type, confidence 
                FROM predictions WHERE prediction_id = ?
            ''', (prediction_id,))
            
            result = cursor.fetchone()
            if not result:
                return False
            
            predicted_value, prediction_type, confidence = result
            
            # Calculate accuracy
            absolute_error = abs(predicted_value - actual_outcome)
            relative_error = absolute_error / max(abs(actual_outcome), 1.0)  # Avoid division by zero
            accuracy = max(0.0, 1.0 - relative_error)
            
            # Update prediction record
            cursor.execute('''
                UPDATE predictions 
                SET actual_outcome = ?, accuracy_when_resolved = ?, user_feedback = ?
                WHERE prediction_id = ?
            ''', (actual_outcome, accuracy, user_feedback, prediction_id))
            
            # Store in accuracy tracking
            cursor.execute('''
                INSERT INTO prediction_accuracy
                (prediction_type, horizon, predicted_value, actual_value, 
                 absolute_error, relative_error, confidence_level, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prediction_type, 'immediate', predicted_value, actual_outcome,
                absolute_error, relative_error, confidence, datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            # Update in-memory accuracy tracking
            self.accuracy_by_type[PredictionType(prediction_type)].append(accuracy)
            
            self.logger.info(f"Resolved prediction {prediction_id} with accuracy {accuracy:.2f}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to resolve prediction: {e}")
            return False
    
    def get_prediction_accuracy_report(self) -> Dict[str, Any]:
        """Get comprehensive accuracy report for all prediction types"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get accuracy by prediction type
        cursor.execute('''
            SELECT prediction_type, AVG(1.0 - relative_error) as avg_accuracy,
                   COUNT(*) as prediction_count,
                   AVG(absolute_error) as avg_absolute_error
            FROM prediction_accuracy
            GROUP BY prediction_type
        ''')
        
        type_accuracies = cursor.fetchall()
        
        # Get recent accuracy trends
        cursor.execute('''
            SELECT prediction_type, created_at, (1.0 - relative_error) as accuracy
            FROM prediction_accuracy
            WHERE created_at > date('now', '-30 days')
            ORDER BY created_at DESC
        ''')
        
        recent_accuracies = cursor.fetchall()
        conn.close()
        
        # Build report
        report = {
            'overall_summary': {
                'total_resolved_predictions': sum(row[2] for row in type_accuracies),
                'average_accuracy_all_types': 0.0,
                'prediction_types_tracked': len(type_accuracies)
            },
            'accuracy_by_type': {},
            'recent_trends': {},
            'honest_assessment': ""
        }
        
        # Calculate overall accuracy
        if type_accuracies:
            total_predictions = sum(row[2] for row in type_accuracies)
            weighted_accuracy = sum(row[1] * row[2] for row in type_accuracies) / total_predictions
            report['overall_summary']['average_accuracy_all_types'] = round(weighted_accuracy, 3)
        
        # Accuracy by type
        for pred_type, accuracy, count, abs_error in type_accuracies:
            report['accuracy_by_type'][pred_type] = {
                'average_accuracy': round(accuracy, 3),
                'prediction_count': count,
                'average_absolute_error': round(abs_error, 3),
                'reliability_assessment': self._assess_reliability(accuracy, count)
            }
        
        # Generate honest assessment
        report['honest_assessment'] = self._generate_accuracy_assessment(report)
        
        return report
    
    def _assess_reliability(self, accuracy: float, count: int) -> str:
        """Assess reliability of prediction type"""
        if count < 5:
            return "Too few predictions to assess reliability"
        elif accuracy < 0.4:
            return "Poor - not significantly better than random"
        elif accuracy < 0.6:
            return "Fair - somewhat better than random"
        elif accuracy < 0.75:
            return "Good - useful for planning"
        elif accuracy < 0.85:
            return "Very good - reliable for decision making"
        else:
            return "Excellent - highly reliable"
    
    def _generate_accuracy_assessment(self, report: Dict[str, Any]) -> str:
        """Generate honest assessment of prediction accuracy"""
        overall_accuracy = report['overall_summary']['average_accuracy_all_types']
        total_predictions = report['overall_summary']['total_resolved_predictions']
        
        if total_predictions < 10:
            return f"Too few predictions ({total_predictions}) to make reliable accuracy claims. " \
                   f"Continue using predictions and providing feedback to improve accuracy assessment."
        
        assessment = f"Based on {total_predictions} resolved predictions, "
        
        if overall_accuracy < 0.5:
            assessment += f"prediction accuracy ({overall_accuracy:.1%}) is not significantly better than random chance. "
            assessment += "Consider using predictions only as rough estimates."
        elif overall_accuracy < 0.7:
            assessment += f"prediction accuracy ({overall_accuracy:.1%}) is moderately better than random. "
            assessment += "Predictions provide some value but should be used cautiously."
        elif overall_accuracy < 0.85:
            assessment += f"prediction accuracy ({overall_accuracy:.1%}) is good and useful for planning. "
            assessment += "Predictions are reliable enough for most decision-making."
        else:
            assessment += f"prediction accuracy ({overall_accuracy:.1%}) is very good. "
            assessment += "Predictions are reliable for planning and decision-making."
        
        assessment += " Remember: individual predictions may still be wrong, even with good overall accuracy."
        
        return assessment
    
    def get_prediction_explanation(self, prediction_id: str) -> Dict[str, Any]:
        """Get detailed explanation of how a prediction was made"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM predictions WHERE prediction_id = ?
        ''', (prediction_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {'error': 'Prediction not found'}
        
        # Unpack prediction data
        (pred_id, pred_type, horizon, predicted_value, confidence, uncertainty_data,
         reasoning, key_factors, similar_situations, created_at, actual_outcome,
         accuracy, user_feedback) = result
        
        uncertainty = json.loads(uncertainty_data)
        
        explanation = {
            'prediction_summary': {
                'type': pred_type,
                'predicted_value': predicted_value,
                'confidence_level': confidence,
                'created_at': created_at
            },
            'how_it_was_calculated': {
                'data_used': f"{uncertainty['sample_size']} similar past situations",
                'method': "Statistical analysis of historical patterns",
                'baseline_comparison': uncertainty['baseline_comparison'],
                'confidence_interval': f"{uncertainty['confidence_interval'][0]:.2f} to {uncertainty['confidence_interval'][1]:.2f}"
            },
            'reasoning': reasoning,
            'key_factors_considered': json.loads(key_factors),
            'similar_past_situations': json.loads(similar_situations),
            'uncertainty_factors': {
                'standard_error': uncertainty['standard_error'],
                'alternative_scenarios': uncertainty['alternative_scenarios'],
                'confounding_factors': uncertainty['confounding_factors'],
                'data_limitations': uncertainty['data_limitations']
            },
            'accuracy_if_resolved': {
                'actual_outcome': actual_outcome,
                'accuracy_score': accuracy,
                'user_feedback': user_feedback
            } if actual_outcome is not None else None,
            'interpretation_guidance': [
                "This prediction is based on statistical patterns in your past data",
                "Individual predictions can be wrong even with good overall accuracy",
                "Consider the confidence level and uncertainty factors",
                "Use predictions as one input among many for decision-making",
                "Provide feedback on accuracy to improve future predictions"
            ]
        }
        
        return explanation


# Example usage
if __name__ == "__main__":
    # Example usage
    engine = PredictionEngine('./data')
    
    # Example context for prediction
    context = {
        'time_of_day': 9,  # 9 AM
        'day_of_week': 1,  # Tuesday
        'task_type': 'coding',
        'energy_level': 4,
        'available_time': 120  # 2 hours
    }
    
    # Example historical data
    historical_data = [
        {
            'timestamp': '2024-01-15T09:00:00',
            'task_type': 'coding',
            'productivity_score': 4.2,
            'duration_minutes': 90,
            'energy_level': 4
        },
        # ... more historical data
    ]
    
    # Make productivity prediction
    prediction = engine.predict_productivity_level(context, historical_data)
    
    if prediction:
        print(f"Prediction: {prediction.predicted_value:.1f}")
        print(f"Confidence: {prediction.confidence.value}")
        print(f"Reasoning: {prediction.reasoning}")
        print(f"Uncertainty: {prediction.uncertainty.confidence_interval}")
    else:
        print("Could not make prediction - insufficient data")
    
    # Resolve prediction later with actual outcome
    # engine.resolve_prediction(prediction.prediction_id, actual_outcome=4.1, 
    #                          user_feedback="Pretty accurate prediction!")

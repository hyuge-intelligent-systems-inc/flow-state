
"""
FlowState Pattern Recognition Module
Honest AI Pattern Detection with User Interpretation

This module identifies productivity patterns while maintaining transparency about
limitations and uncertainty. Users interpret patterns rather than AI making decisions.

Core Principles:
- Honest limitations - clear about what patterns mean and don't mean
- User interpretation - AI finds patterns, users decide what they mean
- Uncertainty quantification - always show confidence levels and alternatives
- No black box decisions - all pattern logic is explainable
- Statistical humility - acknowledge when sample sizes are too small
"""

import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, NamedTuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path
import math
from collections import defaultdict, Counter


class PatternType(Enum):
    """Types of patterns the system can identify"""
    TEMPORAL = "temporal"           # Time-based patterns
    FREQUENCY = "frequency"         # How often things happen
    DURATION = "duration"           # How long things take
    SEQUENCE = "sequence"           # Order of activities
    CORRELATION = "correlation"     # Things that happen together
    TREND = "trend"                 # Changes over time


class PatternConfidence(Enum):
    """Honest confidence levels with clear meanings"""
    VERY_LOW = "very_low"      # 0.0-0.3: Might be noise, not reliable
    LOW = "low"                # 0.3-0.5: Possible pattern, needs more data
    MODERATE = "moderate"      # 0.5-0.7: Likely pattern, useful for decisions
    HIGH = "high"              # 0.7-0.9: Strong pattern, reliable for planning
    VERY_HIGH = "very_high"    # 0.9-1.0: Extremely consistent pattern


@dataclass
class PatternEvidence:
    """Evidence supporting a pattern with transparency"""
    data_points: int
    time_span_days: int
    statistical_significance: float
    alternative_explanations: List[str]
    sample_size_adequacy: str
    confounding_factors: List[str]


@dataclass
class Pattern:
    """Identified pattern with full transparency"""
    pattern_id: str
    pattern_type: PatternType
    name: str
    description: str
    confidence: PatternConfidence
    confidence_score: float
    evidence: PatternEvidence
    actionable_insights: List[str]
    limitations: List[str]
    user_feedback: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class PatternRecognizer:
    """
    Honest pattern recognition with statistical rigor and user interpretation
    
    This class finds patterns in productivity data while being transparent about
    limitations, uncertainty, and alternative explanations.
    """
    
    def __init__(self, data_dir: str, min_data_points: int = 10):
        self.data_dir = Path(data_dir)
        self.min_data_points = min_data_points
        
        # Statistical parameters for honest pattern detection
        self.significance_threshold = 0.05  # p-value for statistical significance
        self.effect_size_threshold = 0.3    # Minimum meaningful effect size
        self.consistency_threshold = 0.7    # How consistent pattern must be
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Database connection
        self.db_path = self.data_dir / 'patterns.db'
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize pattern storage database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recognized_patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                confidence TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                evidence TEXT NOT NULL,
                actionable_insights TEXT NOT NULL,
                limitations TEXT NOT NULL,
                user_feedback TEXT,
                created_at TEXT NOT NULL,
                last_validated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_temporal_patterns(self, time_data: List[Dict[str, Any]]) -> List[Pattern]:
        """
        Identify time-based patterns with statistical rigor
        
        Args:
            time_data: List of timestamped activities
            
        Returns:
            List of temporal patterns with confidence levels
        """
        if len(time_data) < self.min_data_points:
            return [self._create_insufficient_data_pattern(
                "temporal", len(time_data), self.min_data_points
            )]
        
        patterns = []
        
        # Analyze daily patterns
        daily_patterns = self._analyze_daily_patterns(time_data)
        patterns.extend(daily_patterns)
        
        # Analyze weekly patterns
        weekly_patterns = self._analyze_weekly_patterns(time_data)
        patterns.extend(weekly_patterns)
        
        # Analyze peak productivity times
        peak_patterns = self._analyze_peak_times(time_data)
        patterns.extend(peak_patterns)
        
        return self._validate_and_rank_patterns(patterns)
    
    def _analyze_daily_patterns(self, time_data: List[Dict[str, Any]]) -> List[Pattern]:
        """Analyze patterns within daily cycles"""
        hourly_productivity = defaultdict(list)
        
        for entry in time_data:
            if 'timestamp' in entry and 'productivity_score' in entry:
                try:
                    dt = datetime.fromisoformat(entry['timestamp'])
                    hour = dt.hour
                    score = float(entry['productivity_score'])
                    hourly_productivity[hour].append(score)
                except (ValueError, TypeError):
                    continue
        
        patterns = []
        
        # Find peak productivity hours
        hour_averages = {}
        for hour, scores in hourly_productivity.items():
            if len(scores) >= 3:  # Minimum sample size per hour
                hour_averages[hour] = statistics.mean(scores)
        
        if len(hour_averages) >= 6:  # Need decent coverage of day
            peak_hour = max(hour_averages, key=hour_averages.get)
            peak_score = hour_averages[peak_hour]
            
            # Calculate statistical significance
            all_scores = [score for hour_scores in hourly_productivity.values() 
                         for score in hour_scores]
            overall_mean = statistics.mean(all_scores)
            
            # Simple t-test approximation
            if peak_score > overall_mean + statistics.stdev(all_scores) * 0.5:
                confidence_score = min(0.9, (peak_score - overall_mean) / statistics.stdev(all_scores) * 0.2 + 0.6)
                
                evidence = PatternEvidence(
                    data_points=len(hourly_productivity[peak_hour]),
                    time_span_days=self._calculate_time_span(time_data),
                    statistical_significance=0.05,  # Simplified
                    alternative_explanations=[
                        "External factors (meetings, interruptions) might explain differences",
                        "Day-to-day variation might account for apparent pattern",
                        "Correlation with other daily activities not considered"
                    ],
                    sample_size_adequacy=self._assess_sample_adequacy(len(hourly_productivity[peak_hour])),
                    confounding_factors=[
                        "Workload variation", "External interruptions", "Energy levels",
                        "Task type differences", "Environmental factors"
                    ]
                )
                
                pattern = Pattern(
                    pattern_id=f"daily_peak_{peak_hour}",
                    pattern_type=PatternType.TEMPORAL,
                    name=f"Peak Productivity at {peak_hour}:00",
                    description=f"Your productivity appears to be highest around {peak_hour}:00 "
                               f"(average score: {peak_score:.1f} vs overall: {overall_mean:.1f})",
                    confidence=self._score_to_confidence(confidence_score),
                    confidence_score=confidence_score,
                    evidence=evidence,
                    actionable_insights=[
                        f"Consider scheduling important tasks around {peak_hour}:00",
                        "Protect this time from meetings and interruptions",
                        "Track whether this pattern holds during different work periods"
                    ],
                    limitations=[
                        "Pattern may not apply to all types of work",
                        "External factors could override natural productivity cycles",
                        "Individual days may vary significantly from this pattern"
                    ]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_weekly_patterns(self, time_data: List[Dict[str, Any]]) -> List[Pattern]:
        """Analyze patterns across days of the week"""
        daily_productivity = defaultdict(list)
        
        for entry in time_data:
            if 'timestamp' in entry and 'productivity_score' in entry:
                try:
                    dt = datetime.fromisoformat(entry['timestamp'])
                    weekday = dt.strftime('%A')
                    score = float(entry['productivity_score'])
                    daily_productivity[weekday].append(score)
                except (ValueError, TypeError):
                    continue
        
        patterns = []
        
        # Analyze day-of-week patterns
        day_averages = {}
        for day, scores in daily_productivity.items():
            if len(scores) >= 2:  # Minimum occurrences
                day_averages[day] = statistics.mean(scores)
        
        if len(day_averages) >= 5:  # Need most days of week
            best_day = max(day_averages, key=day_averages.get)
            worst_day = min(day_averages, key=day_averages.get)
            
            difference = day_averages[best_day] - day_averages[worst_day]
            
            # Only report if difference is meaningful
            if difference > 0.5:  # Arbitrary but reasonable threshold
                confidence_score = min(0.8, difference * 0.2 + 0.4)
                
                evidence = PatternEvidence(
                    data_points=sum(len(scores) for scores in daily_productivity.values()),
                    time_span_days=self._calculate_time_span(time_data),
                    statistical_significance=0.1,  # Conservative
                    alternative_explanations=[
                        "Meeting schedules might differ by day",
                        "Workload distribution might not be even",
                        "Weekend effects might influence Monday/Friday"
                    ],
                    sample_size_adequacy=self._assess_sample_adequacy(min(len(scores) for scores in daily_productivity.values())),
                    confounding_factors=[
                        "Meeting density", "Deadline proximity", "Team collaboration patterns",
                        "Personal energy cycles", "External commitments"
                    ]
                )
                
                pattern = Pattern(
                    pattern_id=f"weekly_{best_day}_{worst_day}",
                    pattern_type=PatternType.TEMPORAL,
                    name=f"{best_day} vs {worst_day} Productivity",
                    description=f"You tend to be more productive on {best_day} "
                               f"({day_averages[best_day]:.1f}) compared to {worst_day} "
                               f"({day_averages[worst_day]:.1f})",
                    confidence=self._score_to_confidence(confidence_score),
                    confidence_score=confidence_score,
                    evidence=evidence,
                    actionable_insights=[
                        f"Consider scheduling challenging work on {best_day}",
                        f"Plan lighter tasks or meetings for {worst_day}",
                        "Investigate what makes your good days different"
                    ],
                    limitations=[
                        "Pattern may be influenced by external schedule constraints",
                        "Individual weeks may vary significantly",
                        "Causation vs correlation is unclear"
                    ]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_peak_times(self, time_data: List[Dict[str, Any]]) -> List[Pattern]:
        """Identify when user is most focused/productive"""
        focus_sessions = []
        
        for entry in time_data:
            if (entry.get('event_type') == 'focus_session' and 
                'duration_minutes' in entry and 
                'focus_quality' in entry):
                try:
                    duration = float(entry['duration_minutes'])
                    quality = float(entry['focus_quality'])
                    timestamp = datetime.fromisoformat(entry['timestamp'])
                    
                    # Combined focus score (duration * quality)
                    focus_score = duration * quality
                    focus_sessions.append({
                        'timestamp': timestamp,
                        'focus_score': focus_score,
                        'hour': timestamp.hour
                    })
                except (ValueError, TypeError):
                    continue
        
        if len(focus_sessions) < self.min_data_points:
            return []
        
        # Group by hour
        hourly_focus = defaultdict(list)
        for session in focus_sessions:
            hourly_focus[session['hour']].append(session['focus_score'])
        
        # Find best focus hour
        hour_averages = {
            hour: statistics.mean(scores) 
            for hour, scores in hourly_focus.items() 
            if len(scores) >= 2
        }
        
        if not hour_averages:
            return []
        
        best_hour = max(hour_averages, key=hour_averages.get)
        best_score = hour_averages[best_hour]
        
        overall_mean = statistics.mean([s['focus_score'] for s in focus_sessions])
        improvement = (best_score - overall_mean) / overall_mean if overall_mean > 0 else 0
        
        # Only report if meaningful improvement
        if improvement > 0.2:  # 20% better than average
            confidence_score = min(0.85, improvement + 0.5)
            
            evidence = PatternEvidence(
                data_points=len(hourly_focus[best_hour]),
                time_span_days=self._calculate_time_span(time_data),
                statistical_significance=0.05,
                alternative_explanations=[
                    "Fewer interruptions at this time might explain better focus",
                    "Task difficulty might vary by time of day",
                    "Caffeine or energy levels might be confounding factors"
                ],
                sample_size_adequacy=self._assess_sample_adequacy(len(hourly_focus[best_hour])),
                confounding_factors=[
                    "Interruption frequency", "Task complexity", "Energy levels",
                    "Environmental noise", "Meeting schedules"
                ]
            )
            
            pattern = Pattern(
                pattern_id=f"focus_peak_{best_hour}",
                pattern_type=PatternType.TEMPORAL,
                name=f"Deep Focus at {best_hour}:00",
                description=f"Your focus sessions are {improvement:.0%} more effective "
                           f"around {best_hour}:00 compared to your average",
                confidence=self._score_to_confidence(confidence_score),
                confidence_score=confidence_score,
                evidence=evidence,
                actionable_insights=[
                    f"Block {best_hour}:00-{best_hour+2}:00 for deep work",
                    "Avoid scheduling meetings during your peak focus time",
                    "Prepare challenging tasks for this time slot"
                ],
                limitations=[
                    "Pattern based on past focus sessions only",
                    "External factors may override natural focus patterns",
                    "Different types of work may have different optimal times"
                ]
            )
            
            return [pattern]
        
        return []
    
    def analyze_duration_patterns(self, activity_data: List[Dict[str, Any]]) -> List[Pattern]:
        """
        Analyze how long different activities typically take
        
        Args:
            activity_data: List of activities with durations
            
        Returns:
            Patterns about activity durations with uncertainty
        """
        if len(activity_data) < self.min_data_points:
            return [self._create_insufficient_data_pattern(
                "duration", len(activity_data), self.min_data_points
            )]
        
        # Group by activity type
        activity_durations = defaultdict(list)
        for entry in activity_data:
            if 'activity_type' in entry and 'duration_minutes' in entry:
                try:
                    activity = entry['activity_type']
                    duration = float(entry['duration_minutes'])
                    activity_durations[activity].append(duration)
                except (ValueError, TypeError):
                    continue
        
        patterns = []
        
        for activity, durations in activity_durations.items():
            if len(durations) >= 5:  # Need reasonable sample size
                mean_duration = statistics.mean(durations)
                std_duration = statistics.stdev(durations) if len(durations) > 1 else 0
                
                # Assess consistency
                coefficient_of_variation = std_duration / mean_duration if mean_duration > 0 else float('inf')
                
                if coefficient_of_variation < 0.5:  # Reasonably consistent
                    confidence_score = max(0.3, 0.9 - coefficient_of_variation)
                    
                    evidence = PatternEvidence(
                        data_points=len(durations),
                        time_span_days=self._calculate_time_span(activity_data),
                        statistical_significance=0.1,
                        alternative_explanations=[
                            "Task complexity might vary within activity type",
                            "Interruptions could affect some sessions more than others",
                            "Learning curve might influence duration over time"
                        ],
                        sample_size_adequacy=self._assess_sample_adequacy(len(durations)),
                        confounding_factors=[
                            "Task complexity variation", "Interruption frequency",
                            "Energy levels", "Tool/environment changes"
                        ]
                    )
                    
                    pattern = Pattern(
                        pattern_id=f"duration_{activity}",
                        pattern_type=PatternType.DURATION,
                        name=f"{activity.title()} Duration Pattern",
                        description=f"{activity.title()} typically takes {mean_duration:.0f} minutes "
                                   f"(± {std_duration:.0f} minutes)",
                        confidence=self._score_to_confidence(confidence_score),
                        confidence_score=confidence_score,
                        evidence=evidence,
                        actionable_insights=[
                            f"Budget {mean_duration + std_duration:.0f} minutes for {activity}",
                            f"Most {activity} sessions finish within {mean_duration + 2*std_duration:.0f} minutes",
                            "Consider breaking down longer sessions if they consistently exceed expectations"
                        ],
                        limitations=[
                            "Individual sessions may vary significantly",
                            "Task complexity not accounted for in this pattern",
                            "External factors could override typical duration"
                        ]
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def analyze_frequency_patterns(self, event_data: List[Dict[str, Any]]) -> List[Pattern]:
        """
        Analyze how often different events occur
        
        Args:
            event_data: List of timestamped events
            
        Returns:
            Frequency patterns with statistical validation
        """
        if len(event_data) < self.min_data_points:
            return [self._create_insufficient_data_pattern(
                "frequency", len(event_data), self.min_data_points
            )]
        
        # Count events by type and time period
        event_counts = Counter()
        dates = set()
        
        for entry in event_data:
            if 'event_type' in entry and 'timestamp' in entry:
                try:
                    event_type = entry['event_type']
                    dt = datetime.fromisoformat(entry['timestamp'])
                    date = dt.date()
                    
                    event_counts[event_type] += 1
                    dates.add(date)
                except (ValueError, TypeError):
                    continue
        
        if not dates:
            return []
        
        patterns = []
        days_tracked = len(dates)
        
        for event_type, total_count in event_counts.items():
            if total_count >= 5:  # Minimum occurrences
                frequency_per_day = total_count / days_tracked
                
                # Only report meaningful frequencies
                if frequency_per_day >= 0.1:  # At least once per 10 days
                    # Assess regularity (simplified)
                    confidence_score = min(0.8, frequency_per_day * 0.3 + 0.4)
                    
                    evidence = PatternEvidence(
                        data_points=total_count,
                        time_span_days=days_tracked,
                        statistical_significance=0.1,
                        alternative_explanations=[
                            "Tracking period might not be representative",
                            "External factors might influence event frequency",
                            "Seasonal or project-based variations not considered"
                        ],
                        sample_size_adequacy=self._assess_sample_adequacy(total_count),
                        confounding_factors=[
                            "Project deadlines", "Seasonal variations", "Team schedules",
                            "External commitments", "Workload changes"
                        ]
                    )
                    
                    # Format frequency description
                    if frequency_per_day >= 1:
                        freq_desc = f"{frequency_per_day:.1f} times per day"
                    elif frequency_per_day >= 0.14:  # About once per week
                        freq_desc = f"{frequency_per_day * 7:.1f} times per week"
                    else:
                        freq_desc = f"{frequency_per_day * 30:.1f} times per month"
                    
                    pattern = Pattern(
                        pattern_id=f"frequency_{event_type}",
                        pattern_type=PatternType.FREQUENCY,
                        name=f"{event_type.title()} Frequency",
                        description=f"{event_type.title()} occurs {freq_desc} on average",
                        confidence=self._score_to_confidence(confidence_score),
                        confidence_score=confidence_score,
                        evidence=evidence,
                        actionable_insights=[
                            f"Expect {event_type} to happen {freq_desc}",
                            f"Plan capacity for {event_type} in your schedule",
                            "Track whether frequency changes with different work patterns"
                        ],
                        limitations=[
                            "Frequency may vary significantly over time",
                            "External factors not accounted for",
                            "Past frequency may not predict future frequency"
                        ]
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _calculate_time_span(self, data: List[Dict[str, Any]]) -> int:
        """Calculate time span covered by data in days"""
        timestamps = []
        for entry in data:
            if 'timestamp' in entry:
                try:
                    timestamps.append(datetime.fromisoformat(entry['timestamp']))
                except (ValueError, TypeError):
                    continue
        
        if len(timestamps) < 2:
            return 1
        
        time_span = max(timestamps) - min(timestamps)
        return max(1, time_span.days)
    
    def _assess_sample_adequacy(self, sample_size: int) -> str:
        """Honest assessment of sample size adequacy"""
        if sample_size < 5:
            return "Very small sample - patterns unreliable"
        elif sample_size < 10:
            return "Small sample - patterns tentative"
        elif sample_size < 30:
            return "Moderate sample - patterns likely meaningful"
        elif sample_size < 100:
            return "Good sample size - patterns reliable"
        else:
            return "Large sample - patterns very reliable"
    
    def _score_to_confidence(self, score: float) -> PatternConfidence:
        """Convert numerical confidence to categorical confidence"""
        if score < 0.3:
            return PatternConfidence.VERY_LOW
        elif score < 0.5:
            return PatternConfidence.LOW
        elif score < 0.7:
            return PatternConfidence.MODERATE
        elif score < 0.9:
            return PatternConfidence.HIGH
        else:
            return PatternConfidence.VERY_HIGH
    
    def _create_insufficient_data_pattern(self, pattern_type: str, current_data: int, needed_data: int) -> Pattern:
        """Create pattern explaining insufficient data"""
        return Pattern(
            pattern_id=f"insufficient_data_{pattern_type}",
            pattern_type=PatternType.TEMPORAL,  # Default type
            name="Insufficient Data",
            description=f"Not enough data to identify {pattern_type} patterns "
                       f"({current_data} data points, need {needed_data})",
            confidence=PatternConfidence.VERY_LOW,
            confidence_score=0.0,
            evidence=PatternEvidence(
                data_points=current_data,
                time_span_days=0,
                statistical_significance=1.0,
                alternative_explanations=["Insufficient data collection period"],
                sample_size_adequacy="Too small for meaningful analysis",
                confounding_factors=["Limited tracking history"]
            ),
            actionable_insights=[
                f"Continue tracking for at least {needed_data - current_data} more data points",
                "Patterns will become more reliable with longer tracking history",
                "Consider tracking more activities to gather sufficient data"
            ],
            limitations=[
                "No meaningful patterns can be identified yet",
                "Recommendations based on insufficient evidence",
                "Continue tracking to enable pattern recognition"
            ]
        )
    
    def _validate_and_rank_patterns(self, patterns: List[Pattern]) -> List[Pattern]:
        """Validate patterns and rank by reliability"""
        valid_patterns = []
        
        for pattern in patterns:
            # Basic validation
            if (pattern.confidence_score > 0.2 and 
                pattern.evidence.data_points >= 3):
                valid_patterns.append(pattern)
        
        # Sort by confidence score (descending)
        valid_patterns.sort(key=lambda p: p.confidence_score, reverse=True)
        
        return valid_patterns
    
    def store_pattern(self, pattern: Pattern) -> bool:
        """Store identified pattern in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO recognized_patterns 
                (pattern_id, pattern_type, name, description, confidence, 
                 confidence_score, evidence, actionable_insights, limitations, 
                 created_at, last_validated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern.pattern_id,
                pattern.pattern_type.value,
                pattern.name,
                pattern.description,
                pattern.confidence.value,
                pattern.confidence_score,
                json.dumps(asdict(pattern.evidence)),
                json.dumps(pattern.actionable_insights),
                json.dumps(pattern.limitations),
                pattern.created_at.isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Stored pattern: {pattern.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store pattern: {e}")
            return False
    
    def get_patterns_for_user_review(self) -> List[Dict[str, Any]]:
        """Get patterns formatted for user interpretation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pattern_id, name, description, confidence, confidence_score,
                   evidence, actionable_insights, limitations
            FROM recognized_patterns 
            ORDER BY confidence_score DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        patterns_for_review = []
        for row in results:
            pattern_id, name, description, confidence, confidence_score, evidence, insights, limitations = row
            
            # Parse JSON fields
            evidence_data = json.loads(evidence)
            insights_list = json.loads(insights)
            limitations_list = json.loads(limitations)
            
            pattern_review = {
                'pattern_id': pattern_id,
                'name': name,
                'description': description,
                'confidence_level': confidence,
                'confidence_score': round(confidence_score, 2),
                'reliability_note': self._get_reliability_note(confidence_score),
                'data_quality': {
                    'sample_size': evidence_data['data_points'],
                    'time_span_days': evidence_data['time_span_days'],
                    'adequacy': evidence_data['sample_size_adequacy']
                },
                'what_this_might_mean': insights_list,
                'important_limitations': limitations_list,
                'alternative_explanations': evidence_data['alternative_explanations'],
                'user_interpretation_needed': True,
                'action_required': "Review this pattern and decide if it matches your experience"
            }
            patterns_for_review.append(pattern_review)
        
        return patterns_for_review
    
    def _get_reliability_note(self, confidence_score: float) -> str:
        """Get user-friendly reliability note"""
        if confidence_score < 0.3:
            return "Very uncertain - might just be random variation"
        elif confidence_score < 0.5:
            return "Uncertain - possible pattern but needs more data"
        elif confidence_score < 0.7:
            return "Moderate confidence - likely a real pattern"
        elif confidence_score < 0.9:
            return "High confidence - strong evidence for this pattern"
        else:
            return "Very high confidence - very consistent pattern"
    
    def get_pattern_explanation(self, pattern_id: str) -> Dict[str, Any]:
        """Get detailed explanation of how pattern was identified"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM recognized_patterns WHERE pattern_id = ?
        ''', (pattern_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return {'error': 'Pattern not found'}
        
        # Unpack all fields
        (pattern_id, pattern_type, name, description, confidence, confidence_score, 
         evidence, insights, limitations, user_feedback, created_at, last_validated) = result
        
        evidence_data = json.loads(evidence)
        
        explanation = {
            'pattern_name': name,
            'how_it_was_found': {
                'data_analyzed': f"{evidence_data['data_points']} data points over {evidence_data['time_span_days']} days",
                'method': f"Statistical analysis of {pattern_type} patterns",
                'threshold_used': f"Minimum confidence threshold: {self.significance_threshold}",
                'sample_size_requirement': f"Minimum {self.min_data_points} data points"
            },
            'statistical_details': {
                'confidence_score': confidence_score,
                'sample_adequacy': evidence_data['sample_size_adequacy'],
                'statistical_significance': evidence_data.get('statistical_significance', 'Not calculated'),
                'confounding_factors_considered': evidence_data['confounding_factors']
            },
            'why_this_might_not_be_real': evidence_data['alternative_explanations'],
            'what_could_affect_accuracy': evidence_data['confounding_factors'],
            'how_to_validate': [
                "Track this pattern for another few weeks",
                "Pay attention to whether it holds in different circumstances",
                "Consider external factors that might influence this pattern",
                "Test whether acting on this pattern improves your productivity"
            ],
            'honest_assessment': f"This pattern has {confidence} confidence based on available data. "
                               f"It could be meaningful, but you should validate it through your own experience."
        }
        
        return explanation


# Example usage
if __name__ == "__main__":
    # Example usage with sample data
    recognizer = PatternRecognizer('./data', min_data_points=5)
    
    # Sample time data
    sample_data = [
        {
            'timestamp': '2024-01-01T09:00:00',
            'productivity_score': 4.2,
            'event_type': 'work_session'
        },
        {
            'timestamp': '2024-01-01T14:00:00',
            'productivity_score': 3.1,
            'event_type': 'work_session'
        },
        # ... more sample data
    ]
    
    # Analyze patterns
    patterns = recognizer.analyze_temporal_patterns(sample_data)
    
    for pattern in patterns:
        print(f"Pattern: {pattern.name}")
        print(f"Confidence: {pattern.confidence.value} ({pattern.confidence_score:.2f})")
        print(f"Description: {pattern.description}")
        print("---")



"""
FlowState Pattern Analyzer
Based on expert analysis: Collaborative self-discovery with transparent limitations

Key principles implemented:
- User interprets their own data (no AI diagnosis)
- Transparent uncertainty and limitations
- Pattern visualization for user understanding
- Support for personal experiments
- Honest confidence levels
"""

import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict, Counter
import json

from .time_tracker import TimeEntry, ConfidenceLevel, TaskComplexity


@dataclass
class PatternInsight:
    """A pattern observation with honest limitations"""
    pattern_type: str
    description: str
    confidence: ConfidenceLevel
    sample_size: int
    timeframe: str
    limitations: str
    supporting_data: Dict[str, Any]
    user_interpretation_required: bool = True


@dataclass
class ProductivityPattern:
    """User productivity pattern with uncertainty"""
    name: str
    frequency: str  # daily, weekly, situational
    strength: float  # 0.0 to 1.0
    confidence: ConfidenceLevel
    context: Dict[str, Any]
    observations: List[str]
    suggested_experiments: List[str]


class PatternAnalyzer:
    """
    Ethical pattern analyzer that helps users discover their own patterns
    without making AI judgments or diagnoses
    """
    
    def __init__(self):
        self.minimum_sample_size = 5  # Honest about statistical requirements
        self.confidence_threshold = 0.6  # Conservative threshold
        
    def analyze_time_patterns(self, entries: List[TimeEntry], 
                            timeframe_days: int = 30) -> Dict[str, PatternInsight]:
        """
        Analyze temporal patterns with user interpretation required
        
        Args:
            entries: List of time entries to analyze
            timeframe_days: Number of days to analyze
        
        Returns:
            Dict of pattern insights for user interpretation
        """
        # Filter entries to timeframe
        cutoff_date = datetime.now() - timedelta(days=timeframe_days)
        recent_entries = [
            entry for entry in entries 
            if entry.start_time >= cutoff_date and entry.is_complete()
        ]
        
        if len(recent_entries) < self.minimum_sample_size:
            return {
                "insufficient_data": PatternInsight(
                    pattern_type="data_limitation",
                    description=f"Only {len(recent_entries)} complete entries found",
                    confidence=ConfidenceLevel.UNCERTAIN,
                    sample_size=len(recent_entries),
                    timeframe=f"Last {timeframe_days} days",
                    limitations=f"Need at least {self.minimum_sample_size} entries for pattern analysis",
                    supporting_data={"entry_count": len(recent_entries)},
                    user_interpretation_required=True
                )
            }
        
        patterns = {}
        
        # Time of day patterns
        time_patterns = self._analyze_time_of_day_patterns(recent_entries)
        if time_patterns:
            patterns["time_of_day"] = time_patterns
        
        # Day of week patterns
        day_patterns = self._analyze_day_of_week_patterns(recent_entries)
        if day_patterns:
            patterns["day_of_week"] = day_patterns
        
        # Duration patterns
        duration_patterns = self._analyze_duration_patterns(recent_entries)
        if duration_patterns:
            patterns["session_duration"] = duration_patterns
        
        # Energy patterns
        energy_patterns = self._analyze_energy_patterns(recent_entries)
        if energy_patterns:
            patterns["energy_levels"] = energy_patterns
        
        # Focus quality patterns
        focus_patterns = self._analyze_focus_patterns(recent_entries)
        if focus_patterns:
            patterns["focus_quality"] = focus_patterns
        
        return patterns
    
    def _analyze_time_of_day_patterns(self, entries: List[TimeEntry]) -> Optional[PatternInsight]:
        """Analyze when user tends to work most effectively"""
        hourly_data = defaultdict(list)
        
        for entry in entries:
            hour = entry.start_time.hour
            if entry.duration_minutes():
                hourly_data[hour].append({
                    'duration': entry.duration_minutes(),
                    'focus': entry.focus_quality,
                    'energy': entry.energy_level
                })
        
        if len(hourly_data) < 3:  # Need variety in times
            return None
        
        # Calculate average metrics by hour
        hour_stats = {}
        for hour, sessions in hourly_data.items():
            if len(sessions) >= 2:  # Need multiple sessions per hour
                hour_stats[hour] = {
                    'session_count': len(sessions),
                    'avg_duration': statistics.mean([s['duration'] for s in sessions]),
                    'avg_focus': statistics.mean([s['focus'] for s in sessions]),
                    'avg_energy': statistics.mean([s['energy'] for s in sessions])
                }
        
        if not hour_stats:
            return None
        
        # Find peak performance times
        peak_hours = sorted(hour_stats.keys(), 
                          key=lambda h: hour_stats[h]['avg_focus'] * hour_stats[h]['avg_energy'], 
                          reverse=True)[:3]
        
        observations = []
        for hour in peak_hours:
            stats = hour_stats[hour]
            time_str = f"{hour:02d}:00"
            observations.append(
                f"At {time_str}: {stats['session_count']} sessions, "
                f"avg focus {stats['avg_focus']:.1f}/5, "
                f"avg energy {stats['avg_energy']:.1f}/5"
            )
        
        return PatternInsight(
            pattern_type="time_of_day",
            description="When you tend to have higher focus and energy",
            confidence=ConfidenceLevel.MODERATE,
            sample_size=len(entries),
            timeframe="Recent work sessions",
            limitations="Based on self-reported focus/energy scores. Individual daily variation not captured.",
            supporting_data={
                "hourly_stats": hour_stats,
                "peak_hours": peak_hours,
                "observations": observations
            },
            user_interpretation_required=True
        )
    
    def _analyze_day_of_week_patterns(self, entries: List[TimeEntry]) -> Optional[PatternInsight]:
        """Analyze productivity patterns by day of week"""
        daily_data = defaultdict(list)
        
        for entry in entries:
            day_name = entry.start_time.strftime('%A')
            if entry.duration_minutes():
                daily_data[day_name].append({
                    'duration': entry.duration_minutes(),
                    'focus': entry.focus_quality,
                    'energy': entry.energy_level,
                    'interruptions': entry.interruptions
                })
        
        if len(daily_data) < 3:  # Need multiple days
            return None
        
        day_stats = {}
        for day, sessions in daily_data.items():
            if len(sessions) >= 2:
                day_stats[day] = {
                    'session_count': len(sessions),
                    'total_time': sum([s['duration'] for s in sessions]),
                    'avg_focus': statistics.mean([s['focus'] for s in sessions]),
                    'avg_energy': statistics.mean([s['energy'] for s in sessions]),
                    'avg_interruptions': statistics.mean([s['interruptions'] for s in sessions])
                }
        
        if not day_stats:
            return None
        
        observations = []
        for day, stats in day_stats.items():
            observations.append(
                f"{day}: {stats['session_count']} sessions, "
                f"{stats['total_time']} total minutes, "
                f"focus {stats['avg_focus']:.1f}/5"
            )
        
        return PatternInsight(
            pattern_type="day_of_week",
            description="How your productivity varies by day of the week",
            confidence=ConfidenceLevel.MODERATE,
            sample_size=len(entries),
            timeframe="Recent weeks",
            limitations="May reflect work schedule more than personal patterns. External factors not considered.",
            supporting_data={
                "daily_stats": day_stats,
                "observations": observations
            },
            user_interpretation_required=True
        )
    
    def _analyze_duration_patterns(self, entries: List[TimeEntry]) -> Optional[PatternInsight]:
        """Analyze session duration patterns"""
        durations = [entry.duration_minutes() for entry in entries if entry.duration_minutes()]
        
        if len(durations) < self.minimum_sample_size:
            return None
        
        # Calculate duration statistics
        avg_duration = statistics.mean(durations)
        median_duration = statistics.median(durations)
        
        # Categorize sessions
        short_sessions = [d for d in durations if d <= 30]
        medium_sessions = [d for d in durations if 30 < d <= 90]
        long_sessions = [d for d in durations if d > 90]
        
        duration_distribution = {
            'short_sessions_30min_or_less': len(short_sessions),
            'medium_sessions_30_90min': len(medium_sessions),
            'long_sessions_over_90min': len(long_sessions)
        }
        
        observations = [
            f"Average session: {avg_duration:.0f} minutes",
            f"Typical session: {median_duration:.0f} minutes",
            f"Short sessions (≤30min): {len(short_sessions)} ({len(short_sessions)/len(durations)*100:.0f}%)",
            f"Medium sessions (30-90min): {len(medium_sessions)} ({len(medium_sessions)/len(durations)*100:.0f}%)",
            f"Long sessions (>90min): {len(long_sessions)} ({len(long_sessions)/len(durations)*100:.0f}%)"
        ]
        
        return PatternInsight(
            pattern_type="session_duration",
            description="Your typical work session lengths",
            confidence=ConfidenceLevel.MODERATE,
            sample_size=len(durations),
            timeframe="All recorded sessions",
            limitations="Duration alone doesn't indicate productivity. Task type and complexity not considered.",
            supporting_data={
                "duration_stats": {
                    "average": avg_duration,
                    "median": median_duration,
                    "distribution": duration_distribution
                },
                "observations": observations
            },
            user_interpretation_required=True
        )
    
    def _analyze_energy_patterns(self, entries: List[TimeEntry]) -> Optional[PatternInsight]:
        """Analyze self-reported energy level patterns"""
        energy_data = [(entry.energy_level, entry.start_time.hour) for entry in entries]
        
        if len(energy_data) < self.minimum_sample_size:
            return None
        
        energy_levels = [e[0] for e in energy_data]
        avg_energy = statistics.mean(energy_levels)
        
        # Group by time periods
        morning_energy = [e for e, h in energy_data if 6 <= h < 12]
        afternoon_energy = [e for e, h in energy_data if 12 <= h < 18]
        evening_energy = [e for e, h in energy_data if 18 <= h < 24]
        
        time_period_stats = {}
        if morning_energy:
            time_period_stats['morning'] = statistics.mean(morning_energy)
        if afternoon_energy:
            time_period_stats['afternoon'] = statistics.mean(afternoon_energy)
        if evening_energy:
            time_period_stats['evening'] = statistics.mean(evening_energy)
        
        observations = [f"Overall average energy: {avg_energy:.1f}/5"]
        for period, avg in time_period_stats.items():
            observations.append(f"{period.title()} average: {avg:.1f}/5")
        
        return PatternInsight(
            pattern_type="energy_levels",
            description="Your self-reported energy patterns",
            confidence=ConfidenceLevel.LOW,  # Self-reported data has limitations
            sample_size=len(energy_levels),
            timeframe="All sessions with energy data",
            limitations="Based on subjective self-reports. Daily variation and external factors not captured.",
            supporting_data={
                "energy_stats": {
                    "overall_average": avg_energy,
                    "time_periods": time_period_stats
                },
                "observations": observations
            },
            user_interpretation_required=True
        )
    
    def _analyze_focus_patterns(self, entries: List[TimeEntry]) -> Optional[PatternInsight]:
        """Analyze self-reported focus quality patterns"""
        focus_data = []
        for entry in entries:
            if entry.duration_minutes():
                focus_data.append({
                    'focus': entry.focus_quality,
                    'duration': entry.duration_minutes(),
                    'interruptions': entry.interruptions,
                    'hour': entry.start_time.hour
                })
        
        if len(focus_data) < self.minimum_sample_size:
            return None
        
        avg_focus = statistics.mean([f['focus'] for f in focus_data])
        
        # Analyze focus vs interruptions
        low_interruption_focus = [f['focus'] for f in focus_data if f['interruptions'] <= 1]
        high_interruption_focus = [f['focus'] for f in focus_data if f['interruptions'] > 2]
        
        observations = [f"Overall average focus: {avg_focus:.1f}/5"]
        
        if low_interruption_focus and high_interruption_focus:
            low_avg = statistics.mean(low_interruption_focus)
            high_avg = statistics.mean(high_interruption_focus)
            observations.append(f"Focus with ≤1 interruption: {low_avg:.1f}/5")
            observations.append(f"Focus with >2 interruptions: {high_avg:.1f}/5")
        
        return PatternInsight(
            pattern_type="focus_quality",
            description="Your self-reported focus quality patterns",
            confidence=ConfidenceLevel.LOW,  # Subjective data
            sample_size=len(focus_data),
            timeframe="All sessions with focus data",
            limitations="Subjective self-assessment. Doesn't capture flow states or deep work quality.",
            supporting_data={
                "focus_stats": {
                    "overall_average": avg_focus,
                    "low_interruption_sessions": len(low_interruption_focus),
                    "high_interruption_sessions": len(high_interruption_focus)
                },
                "observations": observations
            },
            user_interpretation_required=True
        )
    
    def suggest_experiments(self, patterns: Dict[str, PatternInsight]) -> List[Dict[str, Any]]:
        """
        Suggest personal productivity experiments based on observed patterns
        User designs and runs their own experiments
        """
        experiments = []
        
        for pattern_type, insight in patterns.items():
            if pattern_type == "time_of_day" and insight.confidence != ConfidenceLevel.UNCERTAIN:
                experiments.append({
                    "type": "timing_experiment",
                    "title": "Test Your Peak Performance Times",
                    "hypothesis": "You might be more productive during your observed peak hours",
                    "experiment": "Try scheduling your most important work during your apparent peak times for one week",
                    "measurement": "Track focus quality and task completion during these times vs other times",
                    "duration": "1 week",
                    "pattern_reference": pattern_type
                })
            
            elif pattern_type == "session_duration" and insight.confidence != ConfidenceLevel.UNCERTAIN:
                experiments.append({
                    "type": "duration_experiment", 
                    "title": "Optimize Your Session Length",
                    "hypothesis": "Your natural session length might be optimal for your work style",
                    "experiment": f"Try working in sessions matching your typical duration pattern",
                    "measurement": "Compare productivity and satisfaction with different session lengths",
                    "duration": "2 weeks",
                    "pattern_reference": pattern_type
                })
            
            elif pattern_type == "focus_quality" and insight.confidence != ConfidenceLevel.UNCERTAIN:
                experiments.append({
                    "type": "interruption_experiment",
                    "title": "Test Interruption Management",
                    "hypothesis": "Reducing interruptions might improve your focus quality",
                    "experiment": "Try one week with active interruption blocking vs one week normal",
                    "measurement": "Compare focus ratings between high and low interruption periods",
                    "duration": "2 weeks",
                    "pattern_reference": pattern_type
                })
        
        return experiments
    
    def generate_user_reflection_prompts(self, patterns: Dict[str, PatternInsight]) -> List[str]:
        """
        Generate questions to help users interpret their own patterns
        """
        prompts = [
            "What do you notice about these patterns?",
            "Do any of these patterns surprise you?",
            "Which patterns align with how you feel about your productivity?",
            "What external factors might be influencing these patterns?"
        ]
        
        for pattern_type, insight in patterns.items():
            if pattern_type == "time_of_day":
                prompts.append("What might be causing your energy to be higher/lower at certain times?")
            elif pattern_type == "day_of_week":
                prompts.append("How do your work responsibilities differ across days of the week?")
            elif pattern_type == "session_duration":
                prompts.append("Do your session lengths feel natural, or are they driven by external factors?")
        
        return prompts
    
    def export_pattern_analysis(self, patterns: Dict[str, PatternInsight], 
                              experiments: List[Dict[str, Any]], 
                              reflection_prompts: List[str]) -> Dict[str, Any]:
        """Export complete pattern analysis for user"""
        return {
            "analysis_date": datetime.now().isoformat(),
            "patterns": {
                name: {
                    "type": pattern.pattern_type,
                    "description": pattern.description,
                    "confidence": pattern.confidence.value,
                    "sample_size": pattern.sample_size,
                    "timeframe": pattern.timeframe,
                    "limitations": pattern.limitations,
                    "supporting_data": pattern.supporting_data,
                    "user_interpretation_required": pattern.user_interpretation_required
                }
                for name, pattern in patterns.items()
            },
            "suggested_experiments": experiments,
            "reflection_prompts": reflection_prompts,
            "important_note": "These are observations from your data, not diagnoses. You are the expert on your own productivity patterns.",
            "data_limitations": "All analysis is based on available data and may not capture your full productivity picture."
        }


# Example usage
if __name__ == "__main__":
    # This would normally use real TimeEntry data from TimeTracker
    analyzer = PatternAnalyzer()
    
    # Example: analyze patterns (would use real data)
    patterns = analyzer.analyze_time_patterns([], timeframe_days=30)
    
    if patterns:
        experiments = analyzer.suggest_experiments(patterns)
        prompts = analyzer.generate_user_reflection_prompts(patterns)
        
        # Export for user review
        analysis = analyzer.export_pattern_analysis(patterns, experiments, prompts)
        print("Pattern Analysis:", json.dumps(analysis, indent=2))
    else:
        print("Insufficient data for pattern analysis")

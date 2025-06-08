
"""
FlowState Habit Formation Module
Evidence-Based Habit Support with Realistic Expectations

This module supports habit formation using proven behavioral science while being
honest about the complexity and individual variation in habit development.

Core Principles:
- Realistic expectations - habit formation takes 18-254 days, not 21
- Individual variation - different approaches for different people
- Failure planning - lapses are normal and expected
- Context dependency - habits are tied to specific environments
- User agency - users design their own habit experiments
- Evidence-based - uses actual habit formation research
"""

import json
import logging
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any, Tuple, NamedTuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from pathlib import Path
import statistics
from collections import defaultdict


class HabitComplexity(Enum):
    """Habit complexity levels based on research"""
    MICRO = "micro"           # <2 minutes, very simple
    SIMPLE = "simple"         # 2-15 minutes, single action
    MODERATE = "moderate"     # 15-45 minutes, multiple steps
    COMPLEX = "complex"       # 45+ minutes, many components


class HabitType(Enum):
    """Types of habits based on behavioral science"""
    IMPLEMENTATION_INTENTION = "implementation"  # If-then habits
    HABIT_STACKING = "stacking"                 # After existing habit
    ENVIRONMENT_DESIGN = "environment"          # Context-triggered
    IDENTITY_BASED = "identity"                 # Based on desired identity


class HabitStage(Enum):
    """Stages of habit formation"""
    DESIGNED = "designed"         # Habit designed but not started
    INITIATING = "initiating"     # First 2 weeks
    DEVELOPING = "developing"     # Weeks 3-8
    STABILIZING = "stabilizing"   # Weeks 9-20
    AUTOMATIC = "automatic"       # 20+ weeks, mostly automatic
    DISRUPTED = "disrupted"       # Broken by life changes
    ABANDONED = "abandoned"       # Deliberately stopped


@dataclass
class HabitContext:
    """Environmental and situational context for habits"""
    location: str
    time_of_day: str
    existing_routine: str
    energy_level: str
    social_context: str
    required_tools: List[str]
    potential_obstacles: List[str]


@dataclass
class HabitAttempt:
    """Single attempt at performing a habit"""
    date: date
    completed: bool
    completion_quality: Optional[int]  # 1-5 scale
    context_notes: str
    obstacles_encountered: List[str]
    duration_minutes: Optional[int]
    user_feedback: str


@dataclass
class Habit:
    """Complete habit definition with realistic tracking"""
    habit_id: str
    name: str
    description: str
    complexity: HabitComplexity
    habit_type: HabitType
    stage: HabitStage
    
    # Behavior specification
    trigger: str                    # What triggers the habit
    behavior: str                   # Exact behavior to perform
    reward: str                     # Natural or designed reward
    
    # Context and design
    context: HabitContext
    minimum_viable_version: str     # Smallest possible version
    ideal_version: str              # Full version when established
    
    # Tracking and progress
    created_date: date
    target_frequency: str           # "daily", "weekdays", "3x per week"
    attempts: List[HabitAttempt]
    
    # Realistic expectations
    estimated_formation_time: int   # Days based on complexity
    current_streak: int
    longest_streak: int
    success_rate_7_days: float
    success_rate_30_days: float
    
    # Failure planning
    common_obstacles: List[str]
    recovery_strategies: List[str]
    restart_triggers: List[str]
    
    # User control
    user_notes: str
    paused: bool = False
    pause_reason: str = ""


class HabitFormationEngine:
    """
    Evidence-based habit formation support with realistic expectations
    
    Helps users design, track, and maintain habits using behavioral science
    while being honest about individual variation and failure rates.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Evidence-based parameters
        self.micro_habit_formation_days = (18, 45)      # Research range
        self.simple_habit_formation_days = (30, 90)     # Research range
        self.moderate_habit_formation_days = (60, 180)  # Research range
        self.complex_habit_formation_days = (120, 254)  # Research range
        
        # Success thresholds
        self.consistency_threshold = 0.8    # 80% consistency for "formed"
        self.minimum_tracking_days = 14     # Minimum before assessing progress
        
        # Database setup
        self.db_path = self.data_dir / 'habits.db'
        self._initialize_database()
        
        # Logging
        self.logger = logging.getLogger(__name__)
    
    def _initialize_database(self):
        """Initialize habit tracking database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                habit_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                complexity TEXT NOT NULL,
                habit_type TEXT NOT NULL,
                stage TEXT NOT NULL,
                trigger_text TEXT NOT NULL,
                behavior TEXT NOT NULL,
                reward TEXT NOT NULL,
                context_data TEXT NOT NULL,
                minimum_version TEXT NOT NULL,
                ideal_version TEXT NOT NULL,
                created_date TEXT NOT NULL,
                target_frequency TEXT NOT NULL,
                estimated_formation_time INTEGER NOT NULL,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                common_obstacles TEXT NOT NULL,
                recovery_strategies TEXT NOT NULL,
                restart_triggers TEXT NOT NULL,
                user_notes TEXT DEFAULT '',
                paused INTEGER DEFAULT 0,
                pause_reason TEXT DEFAULT ''
            )
        ''')
        
        # Habit attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_attempts (
                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id TEXT NOT NULL,
                date TEXT NOT NULL,
                completed INTEGER NOT NULL,
                completion_quality INTEGER,
                context_notes TEXT DEFAULT '',
                obstacles_encountered TEXT DEFAULT '[]',
                duration_minutes INTEGER,
                user_feedback TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (habit_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def design_micro_habit(self, desired_behavior: str, existing_routine: str, user_context: Dict[str, Any]) -> Habit:
        """
        Design a micro habit using the "tiny habits" method
        
        Args:
            desired_behavior: What the user wants to do
            existing_routine: Strong existing habit to anchor to
            user_context: User's environment and constraints
            
        Returns:
            Designed micro habit with realistic expectations
        """
        habit_id = f"micro_{desired_behavior.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}"
        
        # Create minimal viable version (under 2 minutes)
        minimal_version = self._create_minimal_version(desired_behavior)
        
        # Design trigger using habit stacking
        trigger = f"After I {existing_routine}, I will {minimal_version}"
        
        # Natural reward identification
        reward = self._identify_natural_reward(minimal_version, user_context)
        
        # Context setup
        context = HabitContext(
            location=user_context.get('preferred_location', 'home'),
            time_of_day=user_context.get('preferred_time', 'morning'),
            existing_routine=existing_routine,
            energy_level=user_context.get('typical_energy', 'medium'),
            social_context=user_context.get('social_setting', 'alone'),
            required_tools=user_context.get('required_tools', []),
            potential_obstacles=user_context.get('known_obstacles', [])
        )
        
        # Realistic formation time (18-45 days for micro habits)
        estimated_days = self._estimate_formation_time(HabitComplexity.MICRO, user_context)
        
        habit = Habit(
            habit_id=habit_id,
            name=f"Micro: {desired_behavior}",
            description=f"Tiny version of {desired_behavior} to build consistency",
            complexity=HabitComplexity.MICRO,
            habit_type=HabitType.HABIT_STACKING,
            stage=HabitStage.DESIGNED,
            trigger=trigger,
            behavior=minimal_version,
            reward=reward,
            context=context,
            minimum_viable_version=minimal_version,
            ideal_version=desired_behavior,
            created_date=date.today(),
            target_frequency="daily",
            attempts=[],
            estimated_formation_time=estimated_days,
            current_streak=0,
            longest_streak=0,
            success_rate_7_days=0.0,
            success_rate_30_days=0.0,
            common_obstacles=user_context.get('known_obstacles', []),
            recovery_strategies=self._design_recovery_strategies(minimal_version),
            restart_triggers=self._design_restart_triggers(existing_routine),
            user_notes=""
        )
        
        return habit
    
    def design_implementation_intention(self, goal_behavior: str, user_context: Dict[str, Any]) -> Habit:
        """
        Design an implementation intention habit (if-then planning)
        
        Args:
            goal_behavior: Behavior user wants to implement
            user_context: User's situation and constraints
            
        Returns:
            Implementation intention habit
        """
        habit_id = f"intention_{goal_behavior.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}"
        
        # Create if-then trigger
        situation = user_context.get('trigger_situation', 'when I start work')
        trigger = f"If {situation}, then I will {goal_behavior}"
        
        # Assess complexity
        complexity = self._assess_behavior_complexity(goal_behavior)
        
        context = HabitContext(
            location=user_context.get('location', 'workplace'),
            time_of_day=user_context.get('time', 'start of workday'),
            existing_routine=user_context.get('existing_routine', 'none'),
            energy_level=user_context.get('energy_level', 'high'),
            social_context=user_context.get('social_context', 'work environment'),
            required_tools=user_context.get('tools', []),
            potential_obstacles=user_context.get('obstacles', [])
        )
        
        # Scale behavior to complexity
        if complexity in [HabitComplexity.MODERATE, HabitComplexity.COMPLEX]:
            minimal_version = self._create_minimal_version(goal_behavior)
        else:
            minimal_version = goal_behavior
        
        estimated_days = self._estimate_formation_time(complexity, user_context)
        
        habit = Habit(
            habit_id=habit_id,
            name=f"If-Then: {goal_behavior}",
            description=f"Implementation intention for {goal_behavior}",
            complexity=complexity,
            habit_type=HabitType.IMPLEMENTATION_INTENTION,
            stage=HabitStage.DESIGNED,
            trigger=trigger,
            behavior=minimal_version,
            reward=self._identify_natural_reward(goal_behavior, user_context),
            context=context,
            minimum_viable_version=minimal_version,
            ideal_version=goal_behavior,
            created_date=date.today(),
            target_frequency=user_context.get('frequency', 'daily'),
            attempts=[],
            estimated_formation_time=estimated_days,
            current_streak=0,
            longest_streak=0,
            success_rate_7_days=0.0,
            success_rate_30_days=0.0,
            common_obstacles=user_context.get('obstacles', []),
            recovery_strategies=self._design_recovery_strategies(goal_behavior),
            restart_triggers=self._design_restart_triggers(situation),
            user_notes=""
        )
        
        return habit
    
    def design_environment_habit(self, behavior: str, environment_cues: Dict[str, str]) -> Habit:
        """
        Design a habit triggered by environmental cues
        
        Args:
            behavior: Target behavior
            environment_cues: Environmental triggers and modifications
            
        Returns:
            Environment-based habit
        """
        habit_id = f"env_{behavior.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}"
        
        # Create environmental trigger
        cue = environment_cues.get('primary_cue', 'visual reminder')
        trigger = f"When I see/encounter {cue}, I will {behavior}"
        
        complexity = self._assess_behavior_complexity(behavior)
        minimal_version = self._create_minimal_version(behavior) if complexity != HabitComplexity.MICRO else behavior
        
        context = HabitContext(
            location=environment_cues.get('location', 'home'),
            time_of_day='any',
            existing_routine='environmental trigger',
            energy_level='variable',
            social_context=environment_cues.get('social_context', 'any'),
            required_tools=environment_cues.get('required_tools', []),
            potential_obstacles=['environmental cue not visible', 'cue becomes invisible over time']
        )
        
        estimated_days = self._estimate_formation_time(complexity, {'obstacles': context.potential_obstacles})
        
        habit = Habit(
            habit_id=habit_id,
            name=f"Environment: {behavior}",
            description=f"Environment-triggered {behavior}",
            complexity=complexity,
            habit_type=HabitType.ENVIRONMENT_DESIGN,
            stage=HabitStage.DESIGNED,
            trigger=trigger,
            behavior=minimal_version,
            reward=self._identify_natural_reward(behavior, environment_cues),
            context=context,
            minimum_viable_version=minimal_version,
            ideal_version=behavior,
            created_date=date.today(),
            target_frequency=environment_cues.get('frequency', 'when triggered'),
            attempts=[],
            estimated_formation_time=estimated_days,
            current_streak=0,
            longest_streak=0,
            success_rate_7_days=0.0,
            success_rate_30_days=0.0,
            common_obstacles=context.potential_obstacles,
            recovery_strategies=[
                'Make environmental cue more visible',
                'Add backup environmental cues',
                'Reset environmental design'
            ],
            restart_triggers=[
                'Redesign environmental cue',
                'Change location of cue',
                'Add social accountability'
            ],
            user_notes=""
        )
        
        return habit
    
    def _create_minimal_version(self, behavior: str) -> str:
        """Create the smallest possible version of a behavior"""
        behavior_lower = behavior.lower()
        
        # Common behavior patterns and their minimal versions
        minimal_mappings = {
            'exercise': 'do 1 push-up',
            'workout': 'put on workout clothes',
            'meditate': 'take 3 deep breaths',
            'read': 'read 1 paragraph',
            'write': 'write 1 sentence',
            'journal': 'write today\'s date',
            'plan': 'write down 1 task',
            'organize': 'put 1 thing in its place',
            'study': 'open study materials',
            'practice': 'practice for 2 minutes',
            'stretch': 'do 1 stretch',
            'walk': 'walk to the front door',
            'drink water': 'take 1 sip of water',
            'eat healthy': 'eat 1 piece of fruit',
            'clean': 'clean 1 small area'
        }
        
        # Check for direct matches
        for key, minimal in minimal_mappings.items():
            if key in behavior_lower:
                return minimal
        
        # Generic fallback: make it 2 minutes or less
        if 'minutes' in behavior_lower:
            return behavior.replace('minutes', '2 minutes')
        elif 'hour' in behavior_lower:
            return behavior.replace('hour', '2 minutes')
        else:
            return f"Do {behavior} for 2 minutes"
    
    def _assess_behavior_complexity(self, behavior: str) -> HabitComplexity:
        """Assess the complexity of a behavior"""
        behavior_lower = behavior.lower()
        
        # Micro habits (very simple, <2 minutes)
        micro_indicators = ['sip', 'one', '1', 'put on', 'open', 'write down', 'take', 'breathe']
        if any(indicator in behavior_lower for indicator in micro_indicators):
            return HabitComplexity.MICRO
        
        # Complex habits (multiple steps, >45 minutes)
        complex_indicators = ['workout routine', 'full', 'complete', 'hour', 'routine', 'session']
        if any(indicator in behavior_lower for indicator in complex_indicators):
            return HabitComplexity.COMPLEX
        
        # Moderate habits (15-45 minutes)
        moderate_indicators = ['exercise', 'meditate', 'study', 'practice', 'plan']
        if any(indicator in behavior_lower for indicator in moderate_indicators):
            return HabitComplexity.MODERATE
        
        # Default to simple
        return HabitComplexity.SIMPLE
    
    def _estimate_formation_time(self, complexity: HabitComplexity, user_context: Dict[str, Any]) -> int:
        """Estimate realistic habit formation time based on research"""
        base_ranges = {
            HabitComplexity.MICRO: self.micro_habit_formation_days,
            HabitComplexity.SIMPLE: self.simple_habit_formation_days,
            HabitComplexity.MODERATE: self.moderate_habit_formation_days,
            HabitComplexity.COMPLEX: self.complex_habit_formation_days
        }
        
        min_days, max_days = base_ranges[complexity]
        
        # Adjust based on user context
        obstacles = len(user_context.get('obstacles', []))
        if obstacles > 3:
            # More obstacles = longer formation time
            return int(min_days + (max_days - min_days) * 0.8)
        elif obstacles < 2:
            # Fewer obstacles = shorter formation time
            return int(min_days + (max_days - min_days) * 0.3)
        else:
            # Average case
            return int(min_days + (max_days - min_days) * 0.5)
    
    def _identify_natural_reward(self, behavior: str, context: Dict[str, Any]) -> str:
        """Identify natural rewards for behaviors"""
        behavior_lower = behavior.lower()
        
        reward_mappings = {
            'exercise': 'feeling energized and accomplished',
            'meditate': 'feeling calm and centered',
            'read': 'learning something new',
            'write': 'expressing thoughts clearly',
            'organize': 'feeling more in control',
            'plan': 'feeling prepared and confident',
            'stretch': 'feeling more flexible and relaxed',
            'water': 'feeling hydrated and refreshed',
            'healthy': 'feeling nourished and energetic'
        }
        
        for key, reward in reward_mappings.items():
            if key in behavior_lower:
                return reward
        
        return 'sense of accomplishment'
    
    def _design_recovery_strategies(self, behavior: str) -> List[str]:
        """Design strategies for recovering from habit lapses"""
        return [
            'Start with an even smaller version of the behavior',
            'Focus on just getting back to the routine location',
            'Do the trigger without the full behavior',
            'Remind yourself that lapses are normal and expected',
            'Don\'t try to "make up" for missed days',
            'Just restart tomorrow without guilt'
        ]
    
    def _design_restart_triggers(self, original_trigger: str) -> List[str]:
        """Design triggers for restarting after lapses"""
        return [
            f'When I notice I\'ve missed {original_trigger}',
            'At the end of each week during review',
            'When I feel disappointed about the lapse',
            'First thing the next morning',
            'During my daily planning time'
        ]
    
    def save_habit(self, habit: Habit) -> bool:
        """Save habit to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO habits 
                (habit_id, name, description, complexity, habit_type, stage,
                 trigger_text, behavior, reward, context_data, minimum_version,
                 ideal_version, created_date, target_frequency, estimated_formation_time,
                 current_streak, longest_streak, common_obstacles, recovery_strategies,
                 restart_triggers, user_notes, paused, pause_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                habit.habit_id, habit.name, habit.description, habit.complexity.value,
                habit.habit_type.value, habit.stage.value, habit.trigger, habit.behavior,
                habit.reward, json.dumps(asdict(habit.context)), habit.minimum_viable_version,
                habit.ideal_version, habit.created_date.isoformat(), habit.target_frequency,
                habit.estimated_formation_time, habit.current_streak, habit.longest_streak,
                json.dumps(habit.common_obstacles), json.dumps(habit.recovery_strategies),
                json.dumps(habit.restart_triggers), habit.user_notes, habit.paused,
                habit.pause_reason
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Saved habit: {habit.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save habit: {e}")
            return False
    
    def record_habit_attempt(self, habit_id: str, completed: bool, 
                           quality: Optional[int] = None, notes: str = "",
                           obstacles: List[str] = None, duration: Optional[int] = None) -> bool:
        """Record a habit attempt with realistic tracking"""
        if obstacles is None:
            obstacles = []
        
        attempt_date = date.today()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Record the attempt
            cursor.execute('''
                INSERT INTO habit_attempts 
                (habit_id, date, completed, completion_quality, context_notes,
                 obstacles_encountered, duration_minutes, user_feedback)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                habit_id, attempt_date.isoformat(), completed, quality, notes,
                json.dumps(obstacles), duration, notes
            ))
            
            # Update habit statistics
            self._update_habit_statistics(habit_id, completed, attempt_date)
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Recorded attempt for habit {habit_id}: {'completed' if completed else 'missed'}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to record habit attempt: {e}")
            return False
    
    def _update_habit_statistics(self, habit_id: str, completed: bool, attempt_date: date):
        """Update habit streak and success rate statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent attempts to calculate streaks and success rates
        cursor.execute('''
            SELECT date, completed FROM habit_attempts 
            WHERE habit_id = ? 
            ORDER BY date DESC
            LIMIT 30
        ''', (habit_id,))
        
        recent_attempts = cursor.fetchall()
        
        # Calculate current streak
        current_streak = 0
        for attempt_date_str, attempt_completed in recent_attempts:
            if attempt_completed:
                current_streak += 1
            else:
                break
        
        # Calculate success rates
        if len(recent_attempts) >= 7:
            last_7_attempts = recent_attempts[:7]
            success_rate_7 = sum(1 for _, completed in last_7_attempts if completed) / 7
        else:
            success_rate_7 = 0.0
        
        if len(recent_attempts) >= 30:
            success_rate_30 = sum(1 for _, completed in recent_attempts if completed) / 30
        else:
            success_rate_30 = 0.0
        
        # Update longest streak if necessary
        cursor.execute('SELECT longest_streak FROM habits WHERE habit_id = ?', (habit_id,))
        current_longest = cursor.fetchone()[0]
        longest_streak = max(current_longest, current_streak)
        
        # Update habit record
        cursor.execute('''
            UPDATE habits 
            SET current_streak = ?, longest_streak = ?, 
                success_rate_7_days = ?, success_rate_30_days = ?
            WHERE habit_id = ?
        ''', (current_streak, longest_streak, success_rate_7, success_rate_30, habit_id))
        
        conn.close()
    
    def get_habit_progress(self, habit_id: str) -> Dict[str, Any]:
        """Get comprehensive habit progress with realistic assessment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get habit details
        cursor.execute('SELECT * FROM habits WHERE habit_id = ?', (habit_id,))
        habit_row = cursor.fetchone()
        
        if not habit_row:
            return {'error': 'Habit not found'}
        
        # Get recent attempts
        cursor.execute('''
            SELECT date, completed, completion_quality, obstacles_encountered
            FROM habit_attempts 
            WHERE habit_id = ? 
            ORDER BY date DESC
            LIMIT 30
        ''', (habit_id,))
        
        attempts = cursor.fetchall()
        conn.close()
        
        if not attempts:
            return self._create_early_stage_progress(habit_row)
        
        # Calculate comprehensive progress
        days_tracked = len(attempts)
        successful_days = sum(1 for _, completed, _, _ in attempts if completed)
        success_rate = successful_days / days_tracked if days_tracked > 0 else 0
        
        # Assess formation progress
        estimated_formation_time = habit_row[14]  # estimated_formation_time column
        formation_progress = min(1.0, days_tracked / estimated_formation_time)
        
        # Determine current stage
        current_stage = self._assess_habit_stage(days_tracked, success_rate, formation_progress)
        
        # Generate honest assessment
        progress_assessment = self._generate_progress_assessment(
            days_tracked, success_rate, formation_progress, current_stage
        )
        
        return {
            'habit_id': habit_id,
            'habit_name': habit_row[1],  # name column
            'days_tracked': days_tracked,
            'success_rate': round(success_rate, 2),
            'current_streak': habit_row[15],  # current_streak column
            'longest_streak': habit_row[16],  # longest_streak column
            'formation_progress': round(formation_progress, 2),
            'estimated_days_remaining': max(0, estimated_formation_time - days_tracked),
            'current_stage': current_stage,
            'progress_assessment': progress_assessment,
            'recent_obstacles': self._get_recent_obstacles(attempts),
            'recommendations': self._generate_recommendations(success_rate, current_stage, attempts)
        }
    
    def _create_early_stage_progress(self, habit_row) -> Dict[str, Any]:
        """Create progress report for habits with no attempts yet"""
        return {
            'habit_id': habit_row[0],
            'habit_name': habit_row[1],
            'days_tracked': 0,
            'success_rate': 0.0,
            'current_streak': 0,
            'longest_streak': 0,
            'formation_progress': 0.0,
            'estimated_days_remaining': habit_row[14],
            'current_stage': 'designed',
            'progress_assessment': 'Habit designed but not yet started. The first few days are crucial for building momentum.',
            'recent_obstacles': [],
            'recommendations': [
                'Start with the minimum viable version to build consistency',
                'Focus on just showing up for the first week',
                'Don\'t worry about perfection - consistency matters more',
                'Track your attempts to identify patterns'
            ]
        }
    
    def _assess_habit_stage(self, days_tracked: int, success_rate: float, formation_progress: float) -> str:
        """Assess current stage of habit formation"""
        if days_tracked < 14:
            return 'initiating'
        elif days_tracked < 56:  # 8 weeks
            if success_rate >= 0.7:
                return 'developing'
            else:
                return 'struggling'
        elif days_tracked < 140:  # 20 weeks
            if success_rate >= 0.8:
                return 'stabilizing'
            else:
                return 'inconsistent'
        else:
            if success_rate >= 0.85:
                return 'automatic'
            else:
                return 'established_but_inconsistent'
    
    def _generate_progress_assessment(self, days_tracked: int, success_rate: float, 
                                    formation_progress: float, stage: str) -> str:
        """Generate honest progress assessment"""
        assessments = {
            'initiating': f"You're in the early stage ({days_tracked} days). "
                         f"Success rate of {success_rate:.0%} is {'good' if success_rate >= 0.6 else 'below ideal'} for this stage. "
                         f"Focus on consistency over perfection.",
            
            'developing': f"Good progress after {days_tracked} days! "
                         f"{success_rate:.0%} success rate shows you're building momentum. "
                         f"The habit is becoming more natural.",
            
            'struggling': f"After {days_tracked} days, {success_rate:.0%} success rate suggests challenges. "
                         f"This is normal - consider simplifying the habit or addressing obstacles.",
            
            'stabilizing': f"Excellent! {days_tracked} days with {success_rate:.0%} success rate. "
                          f"The habit is becoming well-established. Keep protecting the routine.",
            
            'inconsistent': f"After {days_tracked} days, the habit is partially established but inconsistent. "
                           f"Focus on identifying and removing obstacles.",
            
            'automatic': f"Congratulations! After {days_tracked} days, this habit appears well-formed. "
                        f"{success_rate:.0%} consistency shows it's becoming automatic.",
            
            'established_but_inconsistent': f"The habit is established but shows some inconsistency. "
                                          f"Consider what factors disrupt your routine."
        }
        
        return assessments.get(stage, "Habit progress is being tracked.")
    
    def _get_recent_obstacles(self, attempts: List[Tuple]) -> List[str]:
        """Extract common obstacles from recent attempts"""
        all_obstacles = []
        for _, _, _, obstacles_json in attempts[-10:]:  # Last 10 attempts
            try:
                obstacles = json.loads(obstacles_json)
                all_obstacles.extend(obstacles)
            except (json.JSONDecodeError, TypeError):
                continue
        
        # Count and return most common obstacles
        obstacle_counts = defaultdict(int)
        for obstacle in all_obstacles:
            obstacle_counts[obstacle] += 1
        
        return [obstacle for obstacle, count in obstacle_counts.most_common(3)]
    
    def _generate_recommendations(self, success_rate: float, stage: str, attempts: List[Tuple]) -> List[str]:
        """Generate personalized recommendations based on progress"""
        recommendations = []
        
        if success_rate < 0.5:
            recommendations.extend([
                "Consider making the habit smaller/easier",
                "Review your trigger - is it reliable?",
                "Address the most common obstacles first",
                "Remember: 50% consistency is better than 0%"
            ])
        elif success_rate < 0.7:
            recommendations.extend([
                "You're making progress! Focus on consistency",
                "Identify what makes successful days different",
                "Plan for your most common obstacles",
                "Don't increase difficulty yet - stabilize first"
            ])
        elif success_rate < 0.85:
            recommendations.extend([
                "Strong progress! The habit is taking shape",
                "Consider what helps on your successful days",
                "Protect your routine from disruptions",
                "You might be ready to expand the habit slightly"
            ])
        else:
            recommendations.extend([
                "Excellent consistency! The habit is well-established",
                "Consider expanding to the ideal version",
                "This habit could be a foundation for related habits",
                "Share your success strategy with others"
            ])
        
        return recommendations
    
    def get_habits_summary(self) -> Dict[str, Any]:
        """Get summary of all user habits with honest assessment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT h.habit_id, h.name, h.stage, h.current_streak, h.success_rate_7_days,
                   h.created_date, h.estimated_formation_time, h.paused
            FROM habits h
            ORDER BY h.created_date DESC
        ''')
        
        habits = cursor.fetchall()
        conn.close()
        
        summary = {
            'total_habits': len(habits),
            'active_habits': len([h for h in habits if not h[7]]),  # not paused
            'habits_by_stage': defaultdict(int),
            'average_success_rate': 0.0,
            'longest_current_streak': 0,
            'habits_detail': []
        }
        
        success_rates = []
        for habit in habits:
            habit_id, name, stage, streak, success_rate_7, created_date, estimated_time, paused = habit
            
            summary['habits_by_stage'][stage] += 1
            summary['longest_current_streak'] = max(summary['longest_current_streak'], streak)
            
            if success_rate_7 > 0:
                success_rates.append(success_rate_7)
            
            days_since_created = (date.today() - date.fromisoformat(created_date)).days
            formation_progress = min(1.0, days_since_created / estimated_time)
            
            summary['habits_detail'].append({
                'habit_id': habit_id,
                'name': name,
                'stage': stage,
                'current_streak': streak,
                'success_rate_7_days': round(success_rate_7, 2),
                'formation_progress': round(formation_progress, 2),
                'days_tracked': days_since_created,
                'paused': bool(paused),
                'status': self._get_habit_status(success_rate_7, formation_progress, bool(paused))
            })
        
        if success_rates:
            summary['average_success_rate'] = round(statistics.mean(success_rates), 2)
        
        return summary
    
    def _get_habit_status(self, success_rate: float, formation_progress: float, paused: bool) -> str:
        """Get simple status for habit"""
        if paused:
            return "paused"
        elif success_rate >= 0.8:
            return "strong"
        elif success_rate >= 0.6:
            return "developing"
        elif success_rate >= 0.3:
            return "struggling"
        else:
            return "needs_attention"


# Example usage
if __name__ == "__main__":
    # Example usage
    engine = HabitFormationEngine('./data')
    
    # Design a micro habit
    habit = engine.design_micro_habit(
        desired_behavior="read for 30 minutes",
        existing_routine="drink my morning coffee",
        user_context={
            'preferred_location': 'living room',
            'preferred_time': 'morning',
            'known_obstacles': ['phone distractions', 'running late'],
            'required_tools': ['book', 'bookmark']
        }
    )
    
    print(f"Designed habit: {habit.name}")
    print(f"Trigger: {habit.trigger}")
    print(f"Minimal version: {habit.minimum_viable_version}")
    print(f"Estimated formation time: {habit.estimated_formation_time} days")
    
    # Save and track
    engine.save_habit(habit)
    engine.record_habit_attempt(habit.habit_id, completed=True, quality=4, notes="Felt good!")

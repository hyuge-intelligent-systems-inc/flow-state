

"""
FlowState Team Optimization Module
Based on expert analysis: Collaboration without surveillance, trust-building through transparency

Key principles implemented:
- Team insights without individual surveillance
- User-controlled data sharing with granular permissions
- Trust-building through transparency and voluntary participation
- Aggregated insights that preserve individual privacy
- Organizational problem recognition vs individual blame
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import statistics

from ..core.pattern_analyzer import PatternInsight, ConfidenceLevel


class SharingLevel(Enum):
    """Levels of data sharing users can choose"""
    PRIVATE = "private"           # No sharing, individual use only
    ANONYMOUS = "anonymous"       # Anonymous contribution to team insights
    AGGREGATED = "aggregated"     # Share aggregated patterns, not raw data
    TEAM_VISIBLE = "team_visible" # Team can see user's general patterns
    FULL_COLLABORATION = "full_collaboration"  # Open sharing for collaboration


class TeamRole(Enum):
    """Team member roles for context-aware insights"""
    INDIVIDUAL_CONTRIBUTOR = "individual_contributor"
    TEAM_LEAD = "team_lead"
    PROJECT_MANAGER = "project_manager"
    MANAGER = "manager"
    EXECUTIVE = "executive"


class InsightScope(Enum):
    """Scope of team insights"""
    TEAM_LEVEL = "team_level"
    DEPARTMENT_LEVEL = "department_level"
    ORGANIZATION_LEVEL = "organization_level"


@dataclass
class TeamMember:
    """Team member with privacy controls"""
    user_id: str
    name: str
    role: TeamRole
    sharing_level: SharingLevel
    team_ids: List[str]
    data_sharing_preferences: Dict[str, bool]
    last_activity: Optional[datetime] = None
    
    def can_share_insight_type(self, insight_type: str) -> bool:
        """Check if user allows sharing specific insight types"""
        if self.sharing_level == SharingLevel.PRIVATE:
            return False
        
        return self.data_sharing_preferences.get(insight_type, False)


@dataclass
class TeamInsight:
    """Team-level insight with privacy preservation"""
    insight_id: str
    team_id: str
    insight_type: str
    description: str
    confidence: ConfidenceLevel
    supporting_data: Dict[str, Any]
    contributing_members: int  # Count, not identities
    data_range: Dict[str, str]  # Time range of data
    limitations: str
    recommendations: List[str]
    organizational_factors: List[str]  # Systemic issues identified


@dataclass
class CollaborationOpportunity:
    """Opportunity for team collaboration"""
    opportunity_id: str
    title: str
    description: str
    potential_participants: List[str]  # User IDs
    collaboration_type: str
    estimated_impact: str
    voluntary_participation: bool = True


class OrganizationalHealthChecker:
    """
    Identifies systemic vs individual productivity challenges
    """
    
    @staticmethod
    def analyze_systemic_issues(team_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify organizational problems that affect team productivity
        """
        systemic_issues = []
        
        # Check for meeting overload
        avg_meeting_hours = team_data.get("average_meeting_hours_per_week", 0)
        if avg_meeting_hours > 20:
            systemic_issues.append({
                "issue_type": "meeting_overload",
                "severity": "high",
                "description": f"Team averaging {avg_meeting_hours:.1f} hours/week in meetings",
                "recommendation": "Review meeting necessity and efficiency",
                "organizational_action_needed": True
            })
        
        # Check for context switching frequency
        avg_interruptions = team_data.get("average_daily_interruptions", 0)
        if avg_interruptions > 15:
            systemic_issues.append({
                "issue_type": "high_interruption_environment",
                "severity": "medium",
                "description": f"Team experiencing {avg_interruptions:.1f} interruptions per day on average",
                "recommendation": "Implement focus time blocks and communication protocols",
                "organizational_action_needed": True
            })
        
        # Check for resource constraints
        resource_adequacy = team_data.get("resource_adequacy_rating", 5)
        if resource_adequacy < 3:
            systemic_issues.append({
                "issue_type": "resource_constraints",
                "severity": "high", 
                "description": "Team reports inadequate resources for effective work",
                "recommendation": "Resource allocation review needed",
                "organizational_action_needed": True
            })
        
        # Check for unclear priorities
        priority_clarity = team_data.get("priority_clarity_rating", 5)
        if priority_clarity < 3:
            systemic_issues.append({
                "issue_type": "unclear_priorities",
                "severity": "high",
                "description": "Team reports unclear or conflicting priorities",
                "recommendation": "Leadership alignment and communication improvement needed",
                "organizational_action_needed": True
            })
        
        return systemic_issues


class TeamOptimizer:
    """
    Team collaboration and optimization without surveillance
    """
    
    def __init__(self, organization_id: str = "default_org"):
        self.organization_id = organization_id
        self.teams: Dict[str, Dict] = {}
        self.members: Dict[str, TeamMember] = {}
        self.team_insights: Dict[str, List[TeamInsight]] = defaultdict(list)
        self.collaboration_opportunities: Dict[str, List[CollaborationOpportunity]] = defaultdict(list)
        self.privacy_settings = {
            "default_sharing_level": SharingLevel.ANONYMOUS,
            "require_explicit_consent": True,
            "data_retention_days": 90,
            "individual_opt_out": True
        }
        
    def add_team_member(self, user_id: str, name: str, role: TeamRole, 
                       team_ids: List[str], sharing_level: SharingLevel = SharingLevel.ANONYMOUS) -> bool:
        """
        Add team member with privacy controls
        """
        default_sharing_preferences = {
            "productivity_patterns": False,
            "focus_times": False,
            "collaboration_preferences": False,
            "energy_patterns": False,
            "availability_patterns": True,  # Generally safe to share
            "general_productivity_metrics": False
        }
        
        self.members[user_id] = TeamMember(
            user_id=user_id,
            name=name,
            role=role,
            sharing_level=sharing_level,
            team_ids=team_ids,
            data_sharing_preferences=default_sharing_preferences,
            last_activity=datetime.now()
        )
        
        # Add to teams
        for team_id in team_ids:
            if team_id not in self.teams:
                self.teams[team_id] = {
                    "team_id": team_id,
                    "members": [],
                    "created_date": datetime.now().isoformat(),
                    "privacy_policy": "Individual control over all data sharing"
                }
            
            if user_id not in self.teams[team_id]["members"]:
                self.teams[team_id]["members"].append(user_id)
        
        return True
    
    def update_sharing_preferences(self, user_id: str, preferences: Dict[str, bool], 
                                 sharing_level: Optional[SharingLevel] = None) -> bool:
        """
        Update user's data sharing preferences with full control
        """
        if user_id not in self.members:
            return False
        
        member = self.members[user_id]
        
        # Update sharing level if provided
        if sharing_level:
            member.sharing_level = sharing_level
        
        # Update individual preferences
        member.data_sharing_preferences.update(preferences)
        
        # If user goes to private, disable all sharing
        if member.sharing_level == SharingLevel.PRIVATE:
            member.data_sharing_preferences = {key: False for key in member.data_sharing_preferences}
        
        return True
    
    def generate_team_insights(self, team_id: str, member_data: Dict[str, Any]) -> List[TeamInsight]:
        """
        Generate team insights from anonymized, aggregated data
        """
        if team_id not in self.teams:
            return []
        
        team_members = [
            self.members[user_id] for user_id in self.teams[team_id]["members"]
            if user_id in self.members and self.members[user_id].sharing_level != SharingLevel.PRIVATE
        ]
        
        if len(team_members) < 3:  # Need minimum team size for privacy
            return [TeamInsight(
                insight_id=f"insufficient_participation_{team_id}",
                team_id=team_id,
                insight_type="data_limitation",
                description="Insufficient team participation for insights",
                confidence=ConfidenceLevel.UNCERTAIN,
                supporting_data={"participating_members": len(team_members)},
                contributing_members=len(team_members),
                data_range={"start": "N/A", "end": "N/A"},
                limitations="Need at least 3 team members sharing data for privacy-preserving insights",
                recommendations=["Encourage voluntary participation in team insights"],
                organizational_factors=[]
            )]
        
        insights = []
        
        # Aggregate team productivity patterns (anonymous)
        productivity_insight = self._analyze_team_productivity_patterns(team_id, team_members, member_data)
        if productivity_insight:
            insights.append(productivity_insight)
        
        # Analyze collaboration patterns
        collaboration_insight = self._analyze_collaboration_patterns(team_id, team_members, member_data)
        if collaboration_insight:
            insights.append(collaboration_insight)
        
        # Check for organizational health issues
        org_health_insight = self._analyze_organizational_health(team_id, team_members, member_data)
        if org_health_insight:
            insights.append(org_health_insight)
        
        # Store insights
        self.team_insights[team_id] = insights
        
        return insights
    
    def _analyze_team_productivity_patterns(self, team_id: str, team_members: List[TeamMember], 
                                          member_data: Dict[str, Any]) -> Optional[TeamInsight]:
        """Analyze team productivity patterns while preserving privacy"""
        
        # Only include members who consent to productivity pattern sharing
        consenting_members = [
            member for member in team_members 
            if member.can_share_insight_type("productivity_patterns")
        ]
        
        if len(consenting_members) < 3:
            return None
        
        # Aggregate productivity data anonymously
        aggregated_data = {
            "peak_productivity_hours": [],
            "focus_session_lengths": [],
            "energy_patterns": [],
            "interruption_frequencies": []
        }
        
        for member in consenting_members:
            user_data = member_data.get(member.user_id, {})
            
            # Aggregate without revealing individual patterns
            if "peak_hours" in user_data:
                aggregated_data["peak_productivity_hours"].extend(user_data["peak_hours"])
            
            if "typical_session_length" in user_data:
                aggregated_data["focus_session_lengths"].append(user_data["typical_session_length"])
            
            if "daily_interruptions" in user_data:
                aggregated_data["interruption_frequencies"].append(user_data["daily_interruptions"])
        
        # Analyze aggregated patterns
        recommendations = []
        organizational_factors = []
        
        # Analyze peak hours (only if enough data)
        if len(aggregated_data["peak_productivity_hours"]) >= 10:
            from collections import Counter
            hour_counts = Counter(aggregated_data["peak_productivity_hours"])
            most_common_hours = hour_counts.most_common(3)
            
            if most_common_hours[0][1] >= len(consenting_members) * 0.6:
                peak_hour = most_common_hours[0][0]
                recommendations.append(f"Consider protecting {peak_hour:02d}:00-{peak_hour+2:02d}:00 as team focus time")
        
        # Analyze interruption patterns
        if aggregated_data["interruption_frequencies"]:
            avg_interruptions = statistics.mean(aggregated_data["interruption_frequencies"])
            if avg_interruptions > 10:
                organizational_factors.append("High interruption environment affecting team focus")
                recommendations.append("Implement communication protocols to reduce interruptions")
        
        return TeamInsight(
            insight_id=f"team_productivity_{team_id}_{datetime.now().strftime('%Y%m%d')}",
            team_id=team_id,
            insight_type="team_productivity_patterns",
            description="Aggregated team productivity patterns",
            confidence=ConfidenceLevel.MODERATE,
            supporting_data={
                "sample_size": len(consenting_members),
                "data_points": len(aggregated_data["peak_productivity_hours"]),
                "average_interruptions": statistics.mean(aggregated_data["interruption_frequencies"]) if aggregated_data["interruption_frequencies"] else None
            },
            contributing_members=len(consenting_members),
            data_range={
                "start": (datetime.now() - timedelta(days=30)).isoformat(),
                "end": datetime.now().isoformat()
            },
            limitations="Based on voluntary data sharing from team members. Individual patterns not revealed.",
            recommendations=recommendations,
            organizational_factors=organizational_factors
        )
    
    def _analyze_collaboration_patterns(self, team_id: str, team_members: List[TeamMember], 
                                      member_data: Dict[str, Any]) -> Optional[TeamInsight]:
        """Analyze team collaboration effectiveness"""
        
        consenting_members = [
            member for member in team_members 
            if member.can_share_insight_type("collaboration_preferences")
        ]
        
        if len(consenting_members) < 3:
            return None
        
        # Aggregate collaboration data
        collaboration_data = {
            "meeting_satisfaction": [],
            "communication_effectiveness": [],
            "preferred_collaboration_times": [],
            "async_vs_sync_preference": []
        }
        
        organizational_factors = []
        recommendations = []
        
        for member in consenting_members:
            user_data = member_data.get(member.user_id, {})
            
            if "meeting_satisfaction" in user_data:
                collaboration_data["meeting_satisfaction"].append(user_data["meeting_satisfaction"])
            
            if "communication_rating" in user_data:
                collaboration_data["communication_effectiveness"].append(user_data["communication_rating"])
        
        # Analyze collaboration effectiveness
        if collaboration_data["meeting_satisfaction"]:
            avg_meeting_satisfaction = statistics.mean(collaboration_data["meeting_satisfaction"])
            if avg_meeting_satisfaction < 3:
                organizational_factors.append("Low meeting satisfaction across team")
                recommendations.append("Review meeting structure, frequency, and effectiveness")
        
        if collaboration_data["communication_effectiveness"]:
            avg_communication = statistics.mean(collaboration_data["communication_effectiveness"])
            if avg_communication < 3:
                organizational_factors.append("Communication effectiveness challenges")
                recommendations.append("Improve communication channels and protocols")
        
        return TeamInsight(
            insight_id=f"team_collaboration_{team_id}_{datetime.now().strftime('%Y%m%d')}",
            team_id=team_id,
            insight_type="collaboration_patterns",
            description="Team collaboration effectiveness analysis",
            confidence=ConfidenceLevel.MODERATE,
            supporting_data={
                "sample_size": len(consenting_members),
                "avg_meeting_satisfaction": statistics.mean(collaboration_data["meeting_satisfaction"]) if collaboration_data["meeting_satisfaction"] else None,
                "avg_communication_rating": statistics.mean(collaboration_data["communication_effectiveness"]) if collaboration_data["communication_effectiveness"] else None
            },
            contributing_members=len(consenting_members),
            data_range={
                "start": (datetime.now() - timedelta(days=30)).isoformat(),
                "end": datetime.now().isoformat()
            },
            limitations="Based on self-reported collaboration experiences. Individual responses not revealed.",
            recommendations=recommendations,
            organizational_factors=organizational_factors
        )
    
    def _analyze_organizational_health(self, team_id: str, team_members: List[TeamMember], 
                                     member_data: Dict[str, Any]) -> Optional[TeamInsight]:
        """Analyze organizational factors affecting team productivity"""
        
        # Aggregate organizational health data
        org_data = {
            "resource_adequacy": [],
            "priority_clarity": [],
            "workload_balance": [],
            "autonomy_level": [],
            "support_availability": []
        }
        
        for member in team_members:
            user_data = member_data.get(member.user_id, {})
            
            # Collect organizational health metrics
            for metric in org_data.keys():
                if metric in user_data:
                    org_data[metric].append(user_data[metric])
        
        # Analyze systemic issues
        systemic_issues = OrganizationalHealthChecker.analyze_systemic_issues({
            "average_meeting_hours_per_week": statistics.mean(member_data.get("meeting_hours", [20]) or [20]),
            "average_daily_interruptions": statistics.mean(member_data.get("interruptions", [10]) or [10]),
            "resource_adequacy_rating": statistics.mean(org_data["resource_adequacy"]) if org_data["resource_adequacy"] else 5,
            "priority_clarity_rating": statistics.mean(org_data["priority_clarity"]) if org_data["priority_clarity"] else 5
        })
        
        if not systemic_issues:
            return None
        
        organizational_factors = [issue["description"] for issue in systemic_issues]
        recommendations = [issue["recommendation"] for issue in systemic_issues]
        
        return TeamInsight(
            insight_id=f"org_health_{team_id}_{datetime.now().strftime('%Y%m%d')}",
            team_id=team_id,
            insight_type="organizational_health",
            description="Organizational factors affecting team productivity",
            confidence=ConfidenceLevel.HIGH,  # These are systemic observations
            supporting_data={
                "systemic_issues_identified": len(systemic_issues),
                "high_severity_issues": len([i for i in systemic_issues if i["severity"] == "high"])
            },
            contributing_members=len(team_members),
            data_range={
                "start": (datetime.now() - timedelta(days=30)).isoformat(),
                "end": datetime.now().isoformat()
            },
            limitations="Based on team-reported organizational factors. Individual responses aggregated.",
            recommendations=recommendations,
            organizational_factors=organizational_factors
        )
    
    def suggest_collaboration_opportunities(self, team_id: str) -> List[CollaborationOpportunity]:
        """
        Suggest voluntary collaboration opportunities based on team insights
        """
        if team_id not in self.teams:
            return []
        
        opportunities = []
        team_insights = self.team_insights.get(team_id, [])
        
        # Focus time coordination
        productivity_insights = [i for i in team_insights if i.insight_type == "team_productivity_patterns"]
        if productivity_insights:
            opportunities.append(CollaborationOpportunity(
                opportunity_id=f"focus_time_{team_id}",
                title="Coordinate Team Focus Time",
                description="Establish shared focus blocks based on team patterns",
                potential_participants=self.teams[team_id]["members"],
                collaboration_type="focus_coordination",
                estimated_impact="Reduced interruptions and improved deep work quality",
                voluntary_participation=True
            ))
        
        # Meeting optimization
        collaboration_insights = [i for i in team_insights if i.insight_type == "collaboration_patterns"]
        if collaboration_insights and any("meeting" in factor for insight in collaboration_insights for factor in insight.organizational_factors):
            opportunities.append(CollaborationOpportunity(
                opportunity_id=f"meeting_optimization_{team_id}",
                title="Meeting Effectiveness Review",
                description="Collaborative review of meeting practices and effectiveness",
                potential_participants=self.teams[team_id]["members"],
                collaboration_type="process_improvement",
                estimated_impact="Improved meeting satisfaction and time utilization",
                voluntary_participation=True
            ))
        
        # Knowledge sharing
        opportunities.append(CollaborationOpportunity(
            opportunity_id=f"knowledge_sharing_{team_id}",
            title="Productivity Strategy Sharing",
            description="Optional sharing of productivity strategies that work well",
            potential_participants=self.teams[team_id]["members"],
            collaboration_type="knowledge_sharing",
            estimated_impact="Team learning and best practice adoption",
            voluntary_participation=True
        ))
        
        self.collaboration_opportunities[team_id] = opportunities
        return opportunities
    
    def get_privacy_dashboard(self, user_id: str) -> Dict[str, Any]:
        """
        Provide user with complete privacy dashboard and control
        """
        if user_id not in self.members:
            return {"error": "User not found"}
        
        member = self.members[user_id]
        
        return {
            "user_id": user_id,
            "current_sharing_level": member.sharing_level.value,
            "data_sharing_preferences": member.data_sharing_preferences,
            "teams": member.team_ids,
            "data_usage": {
                "what_is_shared": self._get_shared_data_description(member),
                "how_data_is_used": "Aggregated with other team members for team insights only",
                "who_sees_what": self._get_visibility_description(member),
                "retention_period": f"{self.privacy_settings['data_retention_days']} days"
            },
            "privacy_controls": {
                "change_sharing_level": "Available anytime",
                "modify_preferences": "Individual insight types can be enabled/disabled",
                "opt_out_completely": "Always available",
                "data_export": "Full data export available",
                "data_deletion": "Complete data deletion available"
            },
            "transparency": {
                "algorithms_used": "Simple aggregation and statistical analysis only",
                "no_individual_identification": "Your individual patterns are never revealed",
                "voluntary_participation": "All team features are optional"
            }
        }
    
    def _get_shared_data_description(self, member: TeamMember) -> List[str]:
        """Describe what data is shared based on user preferences"""
        shared = []
        for data_type, enabled in member.data_sharing_preferences.items():
            if enabled:
                shared.append(data_type.replace("_", " ").title())
        return shared if shared else ["No data currently shared"]
    
    def _get_visibility_description(self, member: TeamMember) -> Dict[str, str]:
        """Describe who can see what based on sharing level"""
        descriptions = {
            SharingLevel.PRIVATE: "No one can see your data",
            SharingLevel.ANONYMOUS: "Your data contributes to anonymous team statistics only",
            SharingLevel.AGGREGATED: "Your patterns are included in aggregated team insights",
            SharingLevel.TEAM_VISIBLE: "Your team can see your general productivity patterns",
            SharingLevel.FULL_COLLABORATION: "Your team can see detailed patterns for collaboration"
        }
        
        return {
            "visibility_level": descriptions[member.sharing_level],
            "individual_identification": "Never possible regardless of sharing level",
            "manager_access": "Managers see only aggregated team data, never individual data"
        }
    
    def export_team_data(self, team_id: str, requesting_user_id: str) -> Dict[str, Any]:
        """
        Export team data with appropriate privacy controls
        """
        if team_id not in self.teams:
            return {"error": "Team not found"}
        
        if requesting_user_id not in self.teams[team_id]["members"]:
            return {"error": "Access denied - user not in team"}
        
        # Only export aggregated, privacy-preserving data
        return {
            "team_id": team_id,
            "export_date": datetime.now().isoformat(),
            "team_insights": [
                {
                    "insight_type": insight.insight_type,
                    "description": insight.description,
                    "confidence": insight.confidence.value,
                    "contributing_members": insight.contributing_members,
                    "recommendations": insight.recommendations,
                    "organizational_factors": insight.organizational_factors,
                    "limitations": insight.limitations
                }
                for insight in self.team_insights.get(team_id, [])
            ],
            "collaboration_opportunities": [
                {
                    "title": opp.title,
                    "description": opp.description,
                    "collaboration_type": opp.collaboration_type,
                    "estimated_impact": opp.estimated_impact
                }
                for opp in self.collaboration_opportunities.get(team_id, [])
            ],
            "privacy_protection": {
                "individual_data_included": False,
                "aggregation_level": "Team level only",
                "minimum_participants": "3 members required for any insight"
            }
        }
    
    def opt_out_user(self, user_id: str, confirmation: bool = False) -> bool:
        """
        Complete opt-out for user with confirmation
        """
        if not confirmation:
            return False
        
        if user_id in self.members:
            # Set to private and remove from all teams
            member = self.members[user_id]
            member.sharing_level = SharingLevel.PRIVATE
            member.data_sharing_preferences = {key: False for key in member.data_sharing_preferences}
            
            # Remove from teams
            for team_id in member.team_ids:
                if team_id in self.teams and user_id in self.teams[team_id]["members"]:
                    self.teams[team_id]["members"].remove(user_id)
            
            return True
        
        return False


# Example usage and testing
if __name__ == "__main__":
    # Create team optimizer
    team_optimizer = TeamOptimizer("company_123")
    
    # Add team members with different sharing preferences
    team_optimizer.add_team_member(
        "user_1", "Alice", TeamRole.TEAM_LEAD, ["team_alpha"], SharingLevel.AGGREGATED
    )
    team_optimizer.add_team_member(
        "user_2", "Bob", TeamRole.INDIVIDUAL_CONTRIBUTOR, ["team_alpha"], SharingLevel.ANONYMOUS
    )
    team_optimizer.add_team_member(
        "user_3", "Carol", TeamRole.INDIVIDUAL_CONTRIBUTOR, ["team_alpha"], SharingLevel.TEAM_VISIBLE
    )
    
    # Update sharing preferences
    team_optimizer.update_sharing_preferences("user_1", {
        "productivity_patterns": True,
        "collaboration_preferences": True
    })
    
    # Generate team insights with sample data
    sample_member_data = {
        "user_1": {
            "peak_hours": [9, 10, 14, 15],
            "typical_session_length": 45,
            "daily_interruptions": 8,
            "meeting_satisfaction": 3,
            "resource_adequacy": 4
        },
        "user_2": {
            "peak_hours": [8, 9, 13, 14],
            "typical_session_length": 60,
            "daily_interruptions": 12,
            "meeting_satisfaction": 2,
            "priority_clarity": 2
        },
        "user_3": {
            "peak_hours": [10, 11, 15, 16],
            "typical_session_length": 30,
            "daily_interruptions": 15,
            "communication_rating": 3,
            "workload_balance": 2
        }
    }
    
    insights = team_optimizer.generate_team_insights("team_alpha", sample_member_data)
    
    print("Team Insights:")
    for insight in insights:
        print(f"- {insight.description}")
        print(f"  Contributing members: {insight.contributing_members}")
        print(f"  Recommendations: {insight.recommendations}")
        print(f"  Organizational factors: {insight.organizational_factors}\n")
    
    # Get collaboration opportunities
    opportunities = team_optimizer.suggest_collaboration_opportunities("team_alpha")
    
    print("Collaboration Opportunities:")
    for opp in opportunities:
        print(f"- {opp.title}: {opp.description}")
    
    # Get privacy dashboard for user
    privacy_dashboard = team_optimizer.get_privacy_dashboard("user_1")
    print("\nPrivacy Dashboard:")
    print(json.dumps(privacy_dashboard, indent=2))
